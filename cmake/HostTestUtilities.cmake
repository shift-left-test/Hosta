# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

include_guard(GLOBAL)

include(CMakeParseArguments)

function(join_list OUTPUT)
  set(oneValueArgs INPUT PREPEND APPEND)
  cmake_parse_arguments(ARG "" "${oneValueArgs}" "" ${ARGN})

  if(ARG_INPUT)
    set(ELEMS ${INPUT})
  else()
    set(ELEMS ${${OUTPUT}})
  endif()

  if(ARG_PREPEND)
    list(TRANSFORM ELEMS PREPEND ${ARG_PREPEND})
  endif()

  if(ARG_APPEND)
    list(TRANSFORM ELEMS APPEND ${ARG_APPEND})
  endif()

  separate_arguments(ELEMS UNIX_COMMAND "${ELEMS}")

  set(${OUTPUT} ${ELEMS} PARENT_SCOPE)
endfunction()

function(do_host_compile lang OUTPUT)
  include(DetermineHOST${lang}Compiler)

  set(oneValueArgs SOURCE TARGET)
  set(multiValueArgs INCLUDE_DIRECTORIES COMPILE_OPTIONS)
  cmake_parse_arguments(BUILD "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  # FIXME: "-isystem" needs to be set properly
  join_list(BUILD_IMPLICIT_INCLUDE_DIRECTORIES INPUT "${CMAKE_HOST${lang}_IMPLICIT_INCLUDE_DIRECTORIES}" PREPEND "-isystem")
  join_list(BUILD_INCLUDE_DIRECTORIES PREPEND "${CMAKE_INCLUDE_FLAG_C}") # FIXME: CMAKE_INCLUDE_FLAGS_HOST${lang} ?
  join_list(BUILD_COMPILE_OPTIONS)

  # Set path to the output file
  set(_absolute_output "${CMAKE_CURRENT_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/${BUILD_TARGET}.dir/${BUILD_SOURCE}.o")
  file(RELATIVE_PATH _relative_output ${CMAKE_CURRENT_BINARY_DIR} "${_absolute_output}")

  # Make sure that the base directory of the object file exists
  get_filename_component(BUILD_DIRECTORY "${_absolute_output}" DIRECTORY)
  file(MAKE_DIRECTORY ${BUILD_DIRECTORY})

  # Resolve absolute path
  get_filename_component(BUILD_SOURCE ${BUILD_SOURCE} ABSOLUTE)

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
    DEPENDS ${BUILD_SOURCE}
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    COMMENT "Building HOST${lang} object ${_relative_output}"
    VERBATIM
  )

  set(${OUTPUT} ${_absolute_output} PARENT_SCOPE)
endfunction(do_host_compile)

function(do_host_link lang TARGET OUTPUT)
  include(DetermineHOST${lang}Compiler)

  set(oneValueArgs SUFFIX)
  set(multiValueArgs OBJECTS LINK_DIRECTORIES LINK_LIBRARIES LINK_OPTIONS)
  cmake_parse_arguments(BUILD "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  if(NOT BUILD_SUFFIX)
    set(BUILD_SUFFIX ${CMAKE_EXECUTABLE_SUFFIX})
  endif()

  join_list(BUILD_OBJECTS)
  join_list(BUILD_IMPLICIT_LINK_DIRECTORIES INPUT "${CMAKE_HOST${lang}_IMPLICIT_LINK_DIRECTORIES}" PREPEND "${CMAKE_LIBRARY_PATH_FLAG}")
  join_list(BUILD_LINK_DIRECTORIES PREPEND "${CMAKE_LIBRARY_PATH_FLAG}")
  join_list(BUILD_IMPLICIT_LINK_LIBRARIES INPUT "${CMAKE_HOST${lang}_IMPLICIT_LINK_LIBRARIES}" PREPEND "${CMAKE_LINK_LIBRARY_FLAG}")
  join_list(BUILD_LINK_LIBRARIES PREPEND "${CMAKE_LINK_LIBRARY_FLAG}")
  join_list(BUILD_LINK_OPTIONS)

  set(_output "${TARGET}${BUILD_SUFFIX}")

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
    DEPENDS ${BUILD_OBJECTS}
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    COMMENT "Linking HOST${lang} executable ${_output}"
    VERBATIM
  )

  set(${OUTPUT} ${_output} PARENT_SCOPE)
endfunction(do_host_link)
