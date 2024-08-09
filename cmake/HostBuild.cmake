# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

include_guard(GLOBAL)

set(HOSTA_MAJOR_VERSION 1)
set(HOSTA_MINOR_VERSION 0)
set(HOSTA_PATCH_VERSION 0)
set(HOSTA_VERSION ${HOSTA_MAJOR_VERSION}.${HOSTA_MINOR_VERSION}.${HOSTA_PATCH_VERSION})

# Set the directory of the current file
if(NOT _HOSTA_BASE_DIR)
  set(_HOSTA_BASE_DIR "${CMAKE_CURRENT_LIST_DIR}")
endif()

include(CMakeParseArguments)
include(${_HOSTA_BASE_DIR}/DetermineHOSTCCompiler.cmake)

# Set default host build target name
if(NOT CMAKE_HOST_BUILD_TARGET)
  set(CMAKE_HOST_BUILD_TARGET "host-targets")
endif()

# Set default host build target
add_custom_target(${CMAKE_HOST_BUILD_TARGET})

# Set host namespace prefix
set(CMAKE_HOST_NAMESPACE_PREFIX "Host::")

# Set host target prefix
set(CMAKE_HOST_TARGET_PREFIX "HOST-")

# Remove the host namespace prefix if exists
function(remove_host_namespace_prefix OUTPUT INPUT)
  unset(_result)
  string(REGEX REPLACE "^${CMAKE_HOST_NAMESPACE_PREFIX}(.*)" "\\1" _result "${INPUT}")
  set(${OUTPUT} ${_result} PARENT_SCOPE)
endfunction(remove_host_namespace_prefix)

# Replace the host namespace with the relevant prefix for host target
function(get_host_target_name OUTPUT INPUT)
  unset(_result)
  string(REGEX REPLACE "^${CMAKE_HOST_NAMESPACE_PREFIX}(.*)" "${CMAKE_HOST_TARGET_PREFIX}\\1" _result "${INPUT}")
  set(${OUTPUT} ${_result} PARENT_SCOPE)
endfunction(get_host_target_name)

function(get_host_target_names OUTPUT INPUT)
  unset(_result)
  foreach(arg IN LISTS INPUT)
    get_host_target_name(_target "${arg}")
    list(APPEND _result "${_target}")
  endforeach()
  set(${OUTPUT} ${_result} PARENT_SCOPE)
endfunction(get_host_target_names)

# Define custom target properties
define_property(TARGET PROPERTY HOST_TYPE
  BRIEF_DOCS "Type of the host target"
  FULL_DOCS "Type of the host target"
)

define_property(TARGET PROPERTY HOST_NAME
  BRIEF_DOCS "Name of the host target"
  FULL_DOCS "Name of the host target"
)

define_property(TARGET PROPERTY HOST_SOURCES
  BRIEF_DOCS "List of sources files for host targets"
  FULL_DOCS "List of source files for host targets"
)

define_property(TARGET PROPERTY HOST_INTERFACE_INCLUDE_DIRECTORIES
  BRIEF_DOCS "List of include directories for host targets"
  FULL_DOCS "List of include_directories for host targets"
)

define_property(TARGET PROPERTY HOST_INTERFACE_COMPILE_OPTIONS
  BRIEF_DOCS "List of compile options for host targets"
  FULL_DOCS "List of compile options for host targets"
)

define_property(TARGET PROPERTY HOST_INTERFACE_LINK_OPTIONS
  BRIEF_DOCS "List of link options for host targets"
  FULL_DOCS "List of link optiosn for host targets"
)

function(get_host_target_property VARIABLE TARGET PROPERTY)
  get_host_target_name(TARGET "${TARGET}")

  if(NOT TARGET ${TARGET})
    message(FATAL_ERROR "get_host_target_property() called with non-existent target \"${TARGET}\".\n")
  endif()

  # Try fetching host properties first
  unset(_result)
  get_target_property(_result "${TARGET}" "HOST_${PROPERTY}")
  if(NOT _result)
    get_target_property(_result "${TARGET}" "${PROPERTY}")
  endif()
  if(_result)
    set(${VARIABLE} ${_result} PARENT_SCOPE)
  endif()
endfunction(get_host_target_property)

function(get_host_target_properties TARGET)
  set(oneValueArgs NAME TYPE SOURCE_DIR BINARY_DIR)
  set(multiValueArgs SOURCES INTERFACE_INCLUDE_DIRECTORIES INTERFACE_COMPILE_OPTIONS INTERFACE_LINK_OPTIONS)
  cmake_parse_arguments(ARG "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  set(properties ${oneValueArgs} ${multiValueArgs})
  foreach(property IN LISTS properties)
    if(ARG_${property})
      unset(_result)
      get_host_target_property(_result ${TARGET} ${property})
      set("${ARG_${property}}" ${_result} PARENT_SCOPE)
    endif()
  endforeach()
endfunction(get_host_target_properties)

function(set_host_target_property TARGET PROPERTY VALUE)
  get_host_target_name(TARGET "${TARGET}")

  if(NOT TARGET ${TARGET})
    message(FATAL_ERROR "set_host_target_property() called with non-existent target \"${TARGET}\".\n")
  endif()

  # Try setting host properties first
  unset(_result)
  get_property(_result TARGET "${TARGET}" PROPERTY "HOST_${PROPERTY}" DEFINED)
  if(_result)
    set(PROPERTY "HOST_${PROPERTY}")
  endif()
  set_target_properties(${TARGET} PROPERTIES ${PROPERTY} "${VALUE}")
endfunction(set_host_target_property)

function(set_host_target_properties TARGET)
  set(oneValueArgs NAME TYPE)
  set(multiValueArgs SOURCES INTERFACE_INCLUDE_DIRECTORIES INTERFACE_COMPILE_OPTIONS INTERFACE_LINK_OPTIONS)
  cmake_parse_arguments(ARG "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  set(properties ${oneValueArgs} ${multiValueArgs})
  foreach(property IN LISTS properties)
    if(ARG_${property})
      set_host_target_property("${TARGET}" "${property}" "${ARG_${property}}")
    endif()
  endforeach()
endfunction(set_host_target_properties)

function(add_host_dependencies TARGET DEPENDENCIES)
  get_host_target_name(TARGET "${TARGET}")
  get_host_target_names(DEPENDENCIES "${DEPENDENCIES}")
  add_dependencies(${TARGET} ${DEPENDENCIES})
endfunction(add_host_dependencies)

function(add_host_custom_target TARGET)
  set(multiValueArgs DEPENDS)
  cmake_parse_arguments(ARG "" "" "${multiValueArgs}" ${ARGN})

  get_host_target_name(TARGET "${TARGET}")

  if(ARG_DEPENDS)
    get_host_target_names(DEPENDENCIES "${ARG_DEPENDS}")
    add_custom_target(${TARGET} DEPENDS ${DEPENDENCIES})
  else()
    add_custom_target(${TARGET})
  endif()
endfunction(add_host_custom_target)

function(transform_host_arguments OUTPUT INPUT)
  set(oneValueArgs PREPEND)
  cmake_parse_arguments(ARG "" "${oneValueArgs}" "" ${ARGN})

  set(_result ${INPUT})
  if(ARG_PREPEND)
    list(TRANSFORM _result PREPEND "${ARG_PREPEND}")
  endif()
  set(${OUTPUT} ${_result} PARENT_SCOPE)
endfunction(transform_host_arguments)

function(separate_host_scoped_arguments INPUT OUTPUT INTERFACE_OUTPUT)
  set(_interface_mode FALSE)
  set(_result )
  set(_interface_result )

  if(NOT "${INPUT}" MATCHES "^$|PRIVATE.*|PUBLIC.*")
    host_logging_error("The function called with invalid arguments: '${INPUT}'\nPRIVATE or PUBLIC keywords are required to specify the scope of the arguments.")
  endif()

  while(INPUT)
    list(POP_FRONT INPUT arg)
    if(arg STREQUAL "PRIVATE")
      set(_interface_mode FALSE)
    elseif(arg STREQUAL "PUBLIC")
      set(_interface_mode TRUE)
    else()
      list(APPEND _result "${arg}")
      if(_interface_mode)
        list(APPEND _interface_result "${arg}")
      endif()
    endif()
  endwhile()

  set(${OUTPUT} ${_result} PARENT_SCOPE)
  set(${INTERFACE_OUTPUT} ${_interface_result} PARENT_SCOPE)
endfunction(separate_host_scoped_arguments)

function(get_host_file_dependencies lang OUTPUT)
  set(oneValueArgs SOURCE)
  set(multiValueArgs INCLUDE_DIRECTORIES COMPILE_OPTIONS)
  cmake_parse_arguments(BUILD "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  # Resolve absolute path
  get_filename_component(BUILD_SOURCE ${BUILD_SOURCE} ABSOLUTE)

  # Resolve file dependencies
  set(BUILD_COMMAND
    ${CMAKE_HOST${lang}_COMPILER}
    -MM
    ${BUILD_SOURCE}
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
    separate_arguments(_file_dependencies NATIVE_COMMAND "${_output}")
    list(REMOVE_AT _file_dependencies 0)
  else()
    set(_file_dependencies ${BUILD_SOURCE})
  endif()

  set(${OUTPUT} ${_file_dependencies} PARENT_SCOPE)
endfunction(get_host_file_dependencies)

function(get_host_absolute_paths OUTPUT INPUT)
  unset(_result)
  foreach(_path IN LISTS INPUT)
    get_filename_component(_path "${_path}" ABSOLUTE)
    list(APPEND _result "${_path}")
  endforeach()
  set(${OUTPUT} ${_result} PARENT_SCOPE)
endfunction(get_host_absolute_paths)

function(get_host_standard_compile_option lang OUTPUT)
  if(DEFINED CMAKE_HOST${lang}_STANDARD)
    if(NOT DEFINED CMAKE_HOST${lang}${CMAKE_HOST${lang}_STANDARD}_STANDARD_COMPILE_OPTION)
      host_logging_error("HOST${lang}_STANDARD is set to invalid value '${CMAKE_HOST${lang}_STANDARD}'")
    endif()

    if(NOT DEFINED CMAKE_HOST${lang}_EXTENSIONS OR CMAKE_HOST${lang}_EXTENSIONS)
      set(${OUTPUT} "${CMAKE_HOST${lang}${CMAKE_HOST${lang}_STANDARD}_EXTENSION_COMPILE_OPTION}" PARENT_SCOPE)
    else()
      set(${OUTPUT} "${CMAKE_HOST${lang}${CMAKE_HOST${lang}_STANDARD}_STANDARD_COMPILE_OPTION}" PARENT_SCOPE)
    endif()
  endif()
endfunction(get_host_standard_compile_option)

function(find_host_language OUTPUT SOURCES)
  # TODO: find appropriate language to compile source files
  set(${OUTPUT} C PARENT_SCOPE)
endfunction(find_host_language)

function(do_host_compile lang OUTPUT)
  set(oneValueArgs SOURCE TARGET)
  set(multiValueArgs INCLUDE_DIRECTORIES COMPILE_OPTIONS DEPENDS)
  cmake_parse_arguments(BUILD "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  # Set standard compile option
  get_host_standard_compile_option(${lang} _option)
  list(PREPEND BUILD_COMPILE_OPTIONS "${_option}")

  # Set system include directories
  if(CMAKE_INCLUDE_SYSTEM_FLAG_HOST${lang} MATCHES ".*[ ]+$")
    # Remove trailing whitespaces to prevent arguments from being quoted in command line
    string(STRIP "${CMAKE_INCLUDE_SYSTEM_FLAG_HOST${lang}}" CMAKE_INCLUDE_SYSTEM_FLAG_HOST${lang})
    set(BUILD_IMPLICIT_INCLUDE_DIRECTORIES )
    foreach(dir IN LISTS CMAKE_HOST${lang}_IMPLICIT_INCLUDE_DIRECTORIES)
      list(APPEND BUILD_IMPLICIT_INCLUDE_DIRECTORIES "${CMAKE_INCLUDE_SYSTEM_FLAG_HOST${lang}}")
      list(APPEND BUILD_IMPLICIT_INCLUDE_DIRECTORIES "${dir}")
    endforeach()
  else()
    transform_host_arguments(BUILD_IMPLICIT_INCLUDE_DIRECTORIES "${CMAKE_HOST${lang}_IMPLICIT_INCLUDE_DIRECTORIES}" PREPEND "${CMAKE_INCLUDE_SYSTEM_FLAG_HOST${lang}}")
  endif()

  # Set path to the output file
  if(IS_ABSOLUTE "${BUILD_SOURCE}")
    file(RELATIVE_PATH BUILD_SOURCE ${CMAKE_CURRENT_SOURCE_DIR} "${BUILD_SOURCE}")
  endif()
  string(REPLACE ".." "__" _build_source "${BUILD_SOURCE}")
  set(_absolute_output "${CMAKE_CURRENT_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/${CMAKE_HOST_TARGET_PREFIX}${BUILD_TARGET}.dir/${_build_source}${CMAKE_HOST${lang}_OUTPUT_EXTENSION}")
  file(RELATIVE_PATH _relative_output ${CMAKE_CURRENT_BINARY_DIR} "${_absolute_output}")

  # Make sure that the base directory of the object file exists
  get_filename_component(BUILD_DIRECTORY "${_absolute_output}" DIRECTORY)
  file(MAKE_DIRECTORY ${BUILD_DIRECTORY})

  # Resolve absolute path
  get_filename_component(BUILD_SOURCE ${BUILD_SOURCE} ABSOLUTE)

  # Compile source file
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
    COMMAND_EXPAND_LISTS
    VERBATIM
  )

  set(${OUTPUT} ${_absolute_output} PARENT_SCOPE)
endfunction(do_host_compile)

function(do_host_link lang TARGET OUTPUT)
  set(multiValueArgs OBJECTS LINK_LIBRARIES LINK_OPTIONS DEPENDS)
  cmake_parse_arguments(BUILD "" "" "${multiValueArgs}" ${ARGN})

  # Set object files
  separate_arguments(BUILD_OBJECTS NATIVE_COMMAND "${BUILD_OBJECTS}")

  # Set system library directories
  transform_host_arguments(BUILD_IMPLICIT_LINK_DIRECTORIES "${CMAKE_HOST${lang}_IMPLICIT_LINK_DIRECTORIES}" PREPEND "${CMAKE_LIBRARY_PATH_FLAG}")

  # Set system libraries
  transform_host_arguments(BUILD_IMPLICIT_LINK_LIBRARIES "${CMAKE_HOST${lang}_IMPLICIT_LINK_LIBRARIES}" PREPEND "${CMAKE_LINK_LIBRARY_FLAG}")

  # Set libraries
  transform_host_arguments(BUILD_LINK_LIBRARIES "${BUILD_LINK_LIBRARIES}" PREPEND "${CMAKE_LINK_LIBRARY_FLAG}")

  set(_filename "${TARGET}${CMAKE_HOST_EXECUTABLE_SUFFIX}")
  set(_output "${CMAKE_CURRENT_BINARY_DIR}/${_filename}")

  # Link object files
  set(BUILD_COMMAND
    ${CMAKE_HOST${lang}_COMPILER}
    -o ${_output}
    ${BUILD_OBJECTS}
    ${BUILD_IMPLICIT_LINK_DIRECTORIES}
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
    COMMAND_EXPAND_LISTS
    VERBATIM
  )

  set(${OUTPUT} ${_output} PARENT_SCOPE)
endfunction(do_host_link)

function(add_host_executable TARGET)
  set(multiValueArgs SOURCES INCLUDE_DIRECTORIES COMPILE_OPTIONS LINK_OPTIONS LINK_LIBRARIES DEPENDS)
  cmake_parse_arguments(BUILD "" "" "${multiValueArgs}" ${ARGN})

  # Remove host namespace prefix if exists
  remove_host_namespace_prefix(TARGET "${TARGET}")

  # Set include directories
  separate_host_scoped_arguments("${BUILD_INCLUDE_DIRECTORIES}" BUILD_INCLUDE_DIRECTORIES BUILD_INTERFACE_INCLUDE_DIRECTORIES)
  get_host_absolute_paths(BUILD_INCLUDE_DIRECTORIES "${BUILD_INCLUDE_DIRECTORIES}")
  transform_host_arguments(BUILD_INCLUDE_DIRECTORIES "${BUILD_INCLUDE_DIRECTORIES}" PREPEND "${CMAKE_INCLUDE_FLAG_HOSTC}")

  # Set compile options
  separate_host_scoped_arguments("${BUILD_COMPILE_OPTIONS}" BUILD_COMPILE_OPTIONS BUILD_INTERFACE_COMPILE_OPTIONS)

  # Set link options
  separate_host_scoped_arguments("${BUILD_LINK_OPTIONS}" BUILD_LINK_OPTIONS BUILD_INTERFACE_LINK_OPTIONS)

  # Set link libraries
  separate_host_scoped_arguments("${BUILD_LINK_LIBRARIES}" BUILD_LINK_LIBRARIES BUILD_INTERFACE_LINK_LIBRARIES)
  get_host_target_names(BUILD_LINK_LIBRARIES "${BUILD_LINK_LIBRARIES}")

  # Get interface properties of linking libraries
  unset(_extra_include_directories)
  unset(_extra_compile_options)
  unset(_extra_link_options)
  unset(_extra_dependencies)
  foreach(_lib IN LISTS BUILD_LINK_LIBRARIES)
    list(APPEND _extra_include_directories "$<$<AND:$<BOOL:${_lib}>,$<BOOL:$<TARGET_PROPERTY:${_lib},HOST_INTERFACE_INCLUDE_DIRECTORIES>>>:${CMAKE_INCLUDE_FLAG_HOSTC}$<JOIN:$<TARGET_PROPERTY:${_lib},HOST_INTERFACE_INCLUDE_DIRECTORIES>,$<SEMICOLON>${CMAKE_INCLUDE_FLAG_HOSTC}>>")
    list(APPEND _extra_compile_options "$<$<BOOL:${_lib}>:$<TARGET_PROPERTY:${_lib},HOST_INTERFACE_COMPILE_OPTIONS>>")
    list(APPEND _extra_link_options "$<$<BOOL:${_lib}>:$<TARGET_PROPERTY:${_lib},HOST_INTERFACE_LINK_OPTIONS>>")
    list(APPEND _extra_dependencies "$<$<BOOL:${_lib}>:${CMAKE_HOST_TARGET_PREFIX}$<TARGET_PROPERTY:${_lib},HOST_NAME>>")
  endforeach()

  # Add static library paths as link option
  foreach(_lib IN LISTS BUILD_LINK_LIBRARIES)
    list(APPEND _extra_link_options "$<$<AND:$<BOOL:${_lib}>,$<STREQUAL:$<TARGET_PROPERTY:${_lib},HOST_TYPE>,HOST_STATIC>>:$<TARGET_PROPERTY:${_lib},BINARY_DIR>/${CMAKE_HOST_STATIC_LIBRARY_PREFIX}$<TARGET_PROPERTY:${_lib},HOST_NAME>${CMAKE_HOST_STATIC_LIBRARY_SUFFIX}>")
  endforeach()

  if(NOT BUILD_SOURCES)
    host_logging_error("No SOURCES given to target: ${TARGET}")
  endif()

  find_host_language(lang "${BUILD_SOURCES}")

  # Compile source files
  unset(_objects)

  foreach(_source IN LISTS BUILD_SOURCES)
    # Check if the source file exists
    if(IS_ABSOLUTE "${_source}")
      set(_path "${_source}")
    else()
      set(_path "${CMAKE_CURRENT_SOURCE_DIR}/${_source}")
    endif()
    if(NOT EXISTS "${_path}")
      host_logging_error("Cannot find source file:\n  ${_source}")
    endif()

    # Resolve file dependencies
    get_host_file_dependencies(${lang} _file_dependencies
      SOURCE "${_source}"
      INCLUDE_DIRECTORIES "${BUILD_INCLUDE_DIRECTORIES}"
      COMPILE_OPTIONS "${BUILD_COMPILE_OPTIONS}"
    )

    do_host_compile(${lang} _output
      SOURCE "${_source}"
      TARGET "${TARGET}"
      INCLUDE_DIRECTORIES "${BUILD_INCLUDE_DIRECTORIES}" "${_extra_include_directories}"
      COMPILE_OPTIONS "${BUILD_COMPILE_OPTIONS}" "${_extra_compile_options}"
      DEPENDS "${BUILD_DEPENDS}" "${_file_dependencies}" "${_extra_dependencies}"
    )
    list(APPEND _objects ${_output})
  endforeach()

  # Link object files
  do_host_link(${lang} ${TARGET} _output
    OBJECTS "${_objects}"
    LINK_OPTIONS "${BUILD_LINK_OPTIONS}" "${_extra_link_options}"
    DEPENDS "${BUILD_DEPENDS}" "${_extra_dependencies}"
  )

  add_host_custom_target("${CMAKE_HOST_NAMESPACE_PREFIX}${TARGET}" DEPENDS "${_output}")
  add_host_dependencies("${CMAKE_HOST_BUILD_TARGET}" "${CMAKE_HOST_NAMESPACE_PREFIX}${TARGET}")

  set_host_target_properties(${CMAKE_HOST_NAMESPACE_PREFIX}${TARGET}
    NAME "${TARGET}"
    TYPE "HOST_EXECUTABLE"
    SOURCES "${BUILD_SOURCES}"
  )
endfunction(add_host_executable)

function(add_host_library TARGET TYPE)
  set(multiValueArgs SOURCES INCLUDE_DIRECTORIES COMPILE_OPTIONS LINK_OPTIONS DEPENDS)
  cmake_parse_arguments(BUILD "" "" "${multiValueArgs}" ${ARGN})

  # Remove host namespace prefix if exists
  remove_host_namespace_prefix(TARGET "${TARGET}")

  # Set include directories
  separate_host_scoped_arguments("${BUILD_INCLUDE_DIRECTORIES}" BUILD_INCLUDE_DIRECTORIES BUILD_INTERFACE_INCLUDE_DIRECTORIES)
  get_host_absolute_paths(BUILD_INCLUDE_DIRECTORIES "${BUILD_INCLUDE_DIRECTORIES}")
  transform_host_arguments(BUILD_INCLUDE_DIRECTORIES "${BUILD_INCLUDE_DIRECTORIES}" PREPEND "${CMAKE_INCLUDE_FLAG_HOSTC}")
  get_host_absolute_paths(BUILD_INTERFACE_INCLUDE_DIRECTORIES "${BUILD_INTERFACE_INCLUDE_DIRECTORIES}")

  # Set compile options
  separate_host_scoped_arguments("${BUILD_COMPILE_OPTIONS}" BUILD_COMPILE_OPTIONS BUILD_INTERFACE_COMPILE_OPTIONS)

  # Set link options
  separate_host_scoped_arguments("${BUILD_LINK_OPTIONS}" BUILD_LINK_OPTIONS BUILD_INTERFACE_LINK_OPTIONS)

  set(BUILD_TYPE "HOST_${TYPE}")

  if(BUILD_TYPE STREQUAL "HOST_STATIC")
    if(NOT BUILD_SOURCES)
      host_logging_error("No SOURCES given to target: ${TARGET}")
    endif()

    find_host_language(lang "${BUILD_SOURCES}")

    # Compile source files
    unset(_objects)

    foreach(_source IN LISTS BUILD_SOURCES)
      # Check if the source file exists
      if(IS_ABSOLUTE "${_source}")
        set(_path "${_source}")
      else()
        set(_path "${CMAKE_CURRENT_SOURCE_DIR}/${_source}")
      endif()
      if(NOT EXISTS "${_path}")
        host_logging_error("Cannot find source file:\n  ${_source}")
      endif()

      # Resolve file dependencies
      get_host_file_dependencies(${lang} _file_dependencies
        SOURCE "${_source}"
        INCLUDE_DIRECTORIES "${BUILD_INCLUDE_DIRECTORIES}"
        COMPILE_OPTIONS "${BUILD_COMPILE_OPTIONS}"
      )

      do_host_compile(${lang} _output
        SOURCE "${_source}"
        TARGET "${CMAKE_HOST_STATIC_LIBRARY_PREFIX}${TARGET}${CMAKE_HOST_STATIC_LIBRARY_SUFFIX}"
        INCLUDE_DIRECTORIES "${BUILD_INCLUDE_DIRECTORIES}"
        COMPILE_OPTIONS "${BUILD_COMPILE_OPTIONS}"
        DEPENDS "${BUILD_DEPENDS}"
      )
      list(APPEND _objects ${_output})
    endforeach()

    set(_filename "${CMAKE_HOST_STATIC_LIBRARY_PREFIX}${TARGET}${CMAKE_HOST_STATIC_LIBRARY_SUFFIX}")
    set(_output "${CMAKE_CURRENT_BINARY_DIR}/${_filename}")

    # Archive object files to create a static library
    add_custom_command(
      OUTPUT ${_output}
      COMMAND ${CMAKE_HOST_AR} rc ${_output} ${_objects}
      COMMAND ${CMAKE_HOST_RANLIB} ${_output}
      DEPENDS ${_objects} ${BUILD_DEPENDS}
      WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
      COMMENT "Linking HOST${lang} static library ${_filename}"
      COMMAND_EXPAND_LISTS
      VERBATIM
    )
    add_host_custom_target("${CMAKE_HOST_NAMESPACE_PREFIX}${TARGET}" DEPENDS "${_output}")
  elseif(BUILD_TYPE STREQUAL "HOST_INTERFACE")
    if(BUILD_SOURCES)
      host_logging_error("add_host_library INTERFACE requires no source arguments.")
    endif()
    # Create a phony target for an interface library
    add_host_custom_target("${CMAKE_HOST_NAMESPACE_PREFIX}${TARGET}")
  else()
    host_logging_error("Unsupported library type: ${TYPE}")
  endif()

  add_host_dependencies("${CMAKE_HOST_BUILD_TARGET}" "${CMAKE_HOST_NAMESPACE_PREFIX}${TARGET}")

  set_host_target_properties(${CMAKE_HOST_NAMESPACE_PREFIX}${TARGET}
    NAME "${TARGET}"
    TYPE "${BUILD_TYPE}"
    SOURCES "${BUILD_SOURCES}"
    INTERFACE_INCLUDE_DIRECTORIES "${BUILD_INTERFACE_INCLUDE_DIRECTORIES}"
    INTERFACE_COMPILE_OPTIONS "${BUILD_INTERFACE_COMPILE_OPTIONS}"
    INTERFACE_LINK_OPTIONS "${BUILD_INTERFACE_LINK_OPTIONS}"
  )
endfunction(add_host_library)
