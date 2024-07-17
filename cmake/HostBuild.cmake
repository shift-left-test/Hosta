# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

include_guard(GLOBAL)

include(CMakeParseArguments)

# Set host target prefix
if(NOT _HOST_TARGET_PREFIX)
  set(_HOST_TARGET_PREFIX "HOST-")
endif()

function(add_host_dependencies TARGET)
  # Replace the host namespace with the relevant target prefix
  string(REGEX REPLACE "^Host::(.*)" "${_HOST_TARGET_PREFIX}\\1" TARGET "${TARGET}")
  list(TRANSFORM ARGN REPLACE "^Host::(.*)" "${_HOST_TARGET_PREFIX}\\1" OUTPUT_VARIABLE DEPENDENCIES)
  add_dependencies("${TARGET}" "${DEPENDENCIES}")
endfunction(add_host_dependencies)

function(add_host_custom_target TARGET)
  set(multiValueArgs DEPENDS)
  cmake_parse_arguments(ARG "" "" "${multiValueArgs}" ${ARGN})

  if(NOT ARG_DEPENDS)
    return()
  endif()

  # Replace the host namespace with the relevant target prefix
  string(REGEX REPLACE "^Host::(.*)" "${_HOST_TARGET_PREFIX}\\1" TARGET "${TARGET}")
  list(TRANSFORM ARG_DEPENDS REPLACE "^Host::(.*)" "${_HOST_TARGET_PREFIX}\\1" OUTPUT_VARIABLE DEPENDENCIES)
  add_custom_target("${TARGET}" DEPENDS "${DEPENDENCIES}")
endfunction(add_host_custom_target)

function(stringify_list OUTPUT)
  set(options ABSOLUTE)
  set(oneValueArgs PREPEND APPEND)
  set(multiValueArgs INPUT)
  cmake_parse_arguments(ARG "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  if(ARG_INPUT)
    set(ITEMS "${ARG_INPUT}")
  else()
    set(ITEMS "${${OUTPUT}}")
  endif()

  if(ARG_ABSOLUTE)
    unset(_items)
    foreach(_item ${ITEMS})
      if(NOT IS_ABSOLUTE "${_item}")
        get_filename_component(_item "${_item}" ABSOLUTE)
      endif()
      list(APPEND _items "${_item}")
    endforeach()
    set(ITEMS "${_items}")
  endif()

  if(ARG_PREPEND)
    list(TRANSFORM ITEMS PREPEND "${ARG_PREPEND}")
  endif()

  if(ARG_APPEND)
    list(TRANSFORM ITEMS APPEND "${ARG_APPEND}")
  endif()

  separate_arguments(ITEMS NATIVE_COMMAND "${ITEMS}")

  set(${OUTPUT} "${ITEMS}" PARENT_SCOPE)
endfunction(stringify_list)

function(do_host_compile lang OUTPUT)
  include(${_HOSTA_BASE_DIR}/DetermineHOST${lang}Compiler.cmake)

  set(oneValueArgs SOURCE TARGET)
  set(multiValueArgs INCLUDE_DIRECTORIES COMPILE_OPTIONS DEPENDS)
  cmake_parse_arguments(BUILD "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  # Set standard compile option
  if(DEFINED CMAKE_HOST${lang}_STANDARD)
    if(NOT DEFINED CMAKE_HOST${lang}${CMAKE_HOST${lang}_STANDARD}_STANDARD_COMPILE_OPTION)
      message(FATAL_ERROR "HOST${lang}_STANDARD is set to invalid value '${CMAKE_HOST${lang}_STANDARD}'")
    endif()

    if(NOT DEFINED CMAKE_HOST${lang}_EXTENSIONS OR CMAKE_HOST${lang}_EXTENSIONS)
      list(PREPEND BUILD_COMPILE_OPTIONS "${CMAKE_HOST${lang}${CMAKE_HOST${lang}_STANDARD}_EXTENSION_COMPILE_OPTION}")
    else()
      list(PREPEND BUILD_COMPILE_OPTIONS "${CMAKE_HOST${lang}${CMAKE_HOST${lang}_STANDARD}_STANDARD_COMPILE_OPTION}")
    endif()
  endif()

  stringify_list(BUILD_IMPLICIT_INCLUDE_DIRECTORIES INPUT "${CMAKE_HOST${lang}_IMPLICIT_INCLUDE_DIRECTORIES}" PREPEND "${CMAKE_INCLUDE_SYSTEM_FLAG_HOST${lang}}")
  stringify_list(BUILD_INCLUDE_DIRECTORIES PREPEND "${CMAKE_INCLUDE_FLAG_C}" ABSOLUTE)
  stringify_list(BUILD_COMPILE_OPTIONS)

  # Set path to the output file
  if(IS_ABSOLUTE "${BUILD_SOURCE}")
    file(RELATIVE_PATH BUILD_SOURCE ${CMAKE_CURRENT_SOURCE_DIR} "${BUILD_SOURCE}")
  endif()
  string(REPLACE ".." "__" _build_source "${BUILD_SOURCE}")
  set(_absolute_output "${CMAKE_CURRENT_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/${_HOST_TARGET_PREFIX}${BUILD_TARGET}.dir/${_build_source}.o")
  file(RELATIVE_PATH _relative_output ${CMAKE_CURRENT_BINARY_DIR} "${_absolute_output}")

  # Make sure that the base directory of the object file exists
  get_filename_component(BUILD_DIRECTORY "${_absolute_output}" DIRECTORY)
  file(MAKE_DIRECTORY ${BUILD_DIRECTORY})

  # Resolve absolute path
  get_filename_component(BUILD_SOURCE ${BUILD_SOURCE} ABSOLUTE)

  # Resolve file dependencies
  set(BUILD_COMMAND
    ${CMAKE_HOST${lang}_COMPILER}
    -MM
    ${BUILD_SOURCE}
    ${BUILD_IMPLICIT_INCLUDE_DIRECTORIES}
    ${BUILD_INCLUDE_DIRECTORIES}
    ${BUILD_COMPILE_OPTIONS}
  )
  execute_process(
    COMMAND ${BUILD_COMMAND}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    RESULT_VARIABLE _result
    OUTPUT_VARIABLE _output
    ERROR_QUIET
  )

  if(_result EQUAL 0)
    string(REPLACE " \\" "" _output "${_output}")
    string(REPLACE "\n" "" _output "${_output}")
    separate_arguments(BUILD_FILE_DEPENDENCIES NATIVE_COMMAND "${_output}")
    list(REMOVE_AT BUILD_FILE_DEPENDENCIES 0)
  else()
    set(BUILD_FILE_DEPENDENCIES ${BUILD_SOURCE})
  endif()

  set(BUILD_COMMAND
    ${CMAKE_HOST${lang}_COMPILER}
    ${BUILD_IMPLICIT_INCLUDE_DIRECTORIES}
    ${BUILD_INCLUDE_DIRECTORIES}
    ${BUILD_COMPILE_OPTIONS}
    -o ${_relative_output}
    -c ${BUILD_SOURCE}
  )

  add_custom_command(
    OUTPUT ${_relative_output}
    COMMAND ${BUILD_COMMAND}
    DEPENDS ${BUILD_FILE_DEPENDENCIES} ${BUILD_DEPENDS}
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    COMMENT "Building HOST${lang} object ${_relative_output}"
    VERBATIM
  )

  set(${OUTPUT} ${_absolute_output} PARENT_SCOPE)
endfunction(do_host_compile)

function(do_host_link lang TARGET OUTPUT)
  include(${_HOSTA_BASE_DIR}/DetermineHOST${lang}Compiler.cmake)

  set(oneValueArgs SUFFIX)
  set(multiValueArgs OBJECTS LINK_DIRECTORIES LINK_LIBRARIES LINK_OPTIONS DEPENDS)
  cmake_parse_arguments(BUILD "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  stringify_list(BUILD_OBJECTS)
  stringify_list(BUILD_IMPLICIT_LINK_DIRECTORIES INPUT "${CMAKE_HOST${lang}_IMPLICIT_LINK_DIRECTORIES}" PREPEND "${CMAKE_LIBRARY_PATH_FLAG}")
  stringify_list(BUILD_LINK_DIRECTORIES PREPEND "${CMAKE_LIBRARY_PATH_FLAG}")
  stringify_list(BUILD_IMPLICIT_LINK_LIBRARIES INPUT "${CMAKE_HOST${lang}_IMPLICIT_LINK_LIBRARIES}" PREPEND "${CMAKE_LINK_LIBRARY_FLAG}")
  stringify_list(BUILD_LINK_LIBRARIES PREPEND "${CMAKE_LINK_LIBRARY_FLAG}")
  stringify_list(BUILD_LINK_OPTIONS)

  if(NOT BUILD_SUFFIX)
    set(BUILD_SUFFIX "${CMAKE_HOST${lang}_EXECUTABLE_SUFFIX}")
  endif()

  set(_filename "${TARGET}${BUILD_SUFFIX}")
  set(_output "${CMAKE_CURRENT_BINARY_DIR}/${_filename}")

  set(BUILD_COMMAND
    ${CMAKE_HOST${lang}_COMPILER}
    -o ${_output}
    ${BUILD_OBJECTS}
    ${BUILD_IMPLICIT_LINK_DIRECTORIES}
    ${BUILD_LINK_DIRECTORIES}
    ${BUILD_IMPLICIT_LINK_LIBRARIES}
    ${BUILD_LINK_LIBRARIES}
    ${BUILD_LINK_OPTIONS}
  )

  add_custom_command(
    OUTPUT ${_output}
    COMMAND ${BUILD_COMMAND}
    DEPENDS ${BUILD_OBJECTS} ${BUILD_DEPENDS}
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    COMMENT "Linking HOST${lang} executable ${_filename}"
    VERBATIM
  )

  set(${OUTPUT} ${_output} PARENT_SCOPE)
endfunction(do_host_link)

function(add_host_executable lang TARGET OUTPUT)
  set(oneValueArgs SUFFIX)
  set(multiValueArgs SOURCES OBJECTS INCLUDE_DIRECTORIES COMPILE_OPTIONS LINK_OPTIONS DEPENDS)
  cmake_parse_arguments(BUILD "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  unset(_objects)

  # Compile source files
  foreach(_source IN LISTS BUILD_SOURCES)
    do_host_compile(${lang} _output
      SOURCE "${_source}"
      TARGET "${TARGET}"
      INCLUDE_DIRECTORIES "${BUILD_INCLUDE_DIRECTORIES}"
      COMPILE_OPTIONS "${BUILD_COMPILE_OPTIONS}"
      DEPENDS "${BUILD_DEPENDS}"
    )
    list(APPEND _objects ${_output})
  endforeach()

  # Link object files
  do_host_link(${lang} ${TARGET} _output
    SUFFIX "${BUILD_SUFFIX}"
    OBJECTS "${_objects}" "${BUILD_OBJECTS}"
    LINK_OPTIONS "${BUILD_LINK_OPTIONS}"
    DEPENDS "${BUILD_DEPENDS}"
  )

  add_host_custom_target("Host::${TARGET}" DEPENDS "${_output}")

  set(${OUTPUT} ${_output} PARENT_SCOPE)
endfunction(add_host_executable)
