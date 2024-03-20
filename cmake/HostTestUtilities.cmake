# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

include_guard(GLOBAL)

include(CMakeParseArguments)

macro(load_host_compiler_preferences lang)
  include(${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/${CMAKE_VERSION}/CMakeHOST${lang}Compiler.cmake OPTIONAL)
endmacro(load_host_compiler_preferences)

function(save_host_compiler_preferences lang)
  # Set internal directory path if missing
  if(NOT CMAKE_PLATFORM_INFO_DIR)
    set(CMAKE_PLATFORM_INFO_DIR ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/${CMAKE_VERSION})
  endif()

  file(WRITE ${CMAKE_PLATFORM_INFO_DIR}/CMakeHOST${lang}Compiler.cmake.in
    "set(CMAKE_HOST${lang}_COMPILER \"@CMAKE_HOST${lang}_COMPILER@\")\n"
    "set(CMAKE_HOST${lang}_COMPILER_WORKS @CMAKE_HOST${lang}_COMPILER_WORKS@)\n"
    "set(CMAKE_HOST${lang}_ABI_COMPILED @CMAKE_HOST${lang}_ABI_COMPILED@)\n"
    "set(CMAKE_HOST${lang}_COMPILER_ABI \"@CMAKE_HOST${lang}_COMPILER_ABI@\")\n"
    "set(CMAKE_HOST${lang}_IMPLICIT_INCLUDE_DIRECTORIES \"@CMAKE_HOST${lang}_IMPLICIT_INCLUDE_DIRECTORIES@\")\n"
    "set(CMAKE_HOST${lang}_IMPLICIT_LINK_LIBRARIES \"@CMAKE_HOST${lang}_IMPLICIT_LINK_LIBRARIES@\")\n"
    "set(CMAKE_HOST${lang}_IMPLICIT_LINK_DIRECTORIES \"@CMAKE_HOST${lang}_IMPLICIT_LINK_DIRECTORIES@\")\n"
    "set(CMAKE_HOST${lang}_IMPLICIT_LINK_FRAMEWORK_DIRECTORIES \"@CMAKE_HOST${lang}_IMPLICIT_LINK_FRAMEWORK_DIRECTORIES@\")\n"
  )

  configure_file(
    ${CMAKE_PLATFORM_INFO_DIR}/CMakeHOST${lang}Compiler.cmake.in
    ${CMAKE_PLATFORM_INFO_DIR}/CMakeHOST${lang}Compiler.cmake
    @ONLY
  )
endfunction(save_host_compiler_preferences)

function(find_host_compiler lang)
  include(CMakeDetermineCompiler)
  _cmake_find_compiler(HOST${lang})
  mark_as_advanced(CMAKE_HOST${lang}_COMPILER)
endfunction(find_host_compiler)

function(try_host_compile lang)
  set(oneValueArgs SOURCE TARGET WORKING_DIRECTORY RESULT_VARIABLE OUTPUT_VARIABLE)
  set(multiValueArgs COMPILE_OPTIONS)

  cmake_parse_arguments(BUILD "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  file(MAKE_DIRECTORY ${BUILD_WORKING_DIRECTORY})
  file(REMOVE ${BUILD_TARGET})

  execute_process(
    COMMAND ${CMAKE_HOST${lang}_COMPILER} ${BUILD_COMPILE_OPTIONS} ${BUILD_SOURCE} -o ${BUILD_TARGET}
    WORKING_DIRECTORY ${BUILD_WORKING_DIRECTORY}
    RESULT_VARIABLE RESULT
    OUTPUT_VARIABLE OUTPUT
    ERROR_VARIABLE OUTPUT
    ERROR_QUIET
  )

  if(RESULT EQUAL 0)
    set(${BUILD_RESULT_VARIABLE} TRUE PARENT_SCOPE)
  endif()

  set(${BUILD_OUTPUT_VARIABLE} ${OUTPUT} PARENT_SCOPE)
endfunction(try_host_compile)

function(parse_host_compiler_abi_info lang bin)
  file(STRINGS "${bin}" ABI_STRINGS REGEX "INFO:[A-Za-z0-9_]+\\[[^]]*\\]")
  foreach(info ${ABI_STRINGS})
    if("${info}" MATCHES "INFO:abi\\[([^]]*)\\]")
      set(CMAKE_HOST${lang}_COMPILER_ABI "${CMAKE_MATCH_1}" PARENT_SCOPE)
      break()
    endif()
  endforeach()
endfunction(parse_host_compiler_abi_info)

function(parse_host_implicit_include_info lang text)
  include(CMakeParseImplicitIncludeInfo)

  set(implicit_incdirs "")

  cmake_parse_implicit_include_info("${text}" HOST${lang} implicit_incdirs log rv)

  file(APPEND ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeOutput.log
    "Parsed HOST${lang} implicit include dir info from above output: rv=${rv}\n${log}\n\n")

  set(CMAKE_HOST${lang}_IMPLICIT_INCLUDE_DIRECTORIES "${implicit_incdirs}" PARENT_SCOPE)
endfunction(parse_host_implicit_include_info)

function(parse_host_implicit_link_info lang text)
  include(CMakeParseImplicitLinkInfo)

  set(implicit_libs "")
  set(implicit_dirs "")
  set(implicit_fwks "")

  CMAKE_PARSE_IMPLICIT_LINK_INFO("${text}" implicit_libs implicit_dirs implicit_fwks log "${CMAKE_HOST${lang}_IMPLICIT_OBJECT_REGEX}")

  file(APPEND ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeOutput.log
    "Parsed HOST${lang} implicit link information from above output:\n${log}\n\n"
  )

  set(CMAKE_HOST${lang}_IMPLICIT_LINK_LIBRARIES "${implicit_libs}" PARENT_SCOPE)
  set(CMAKE_HOST${lang}_IMPLICIT_LINK_DIRECTORIES "${implicit_dirs}" PARENT_SCOPE)
  set(CMAKE_HOST${lang}_IMPLICIT_FRAMEWORK_DIRECTORIES "${implicit_fwks}" PARENT_SCOPE)
endfunction(parse_host_implicit_link_info)

function(join_list OUTPUT)
  set(oneValueArgs PREPEND APPEND)
  set(multiValueArgs INPUT)
  cmake_parse_arguments(ARG "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  if(ARG_INPUT)
    set(ITEMS "${ARG_INPUT}")
  else()
    set(ITEMS "${${OUTPUT}}")
  endif()

  if(ARG_PREPEND)
    list(TRANSFORM ITEMS PREPEND "${ARG_PREPEND}")
  endif()

  if(ARG_APPEND)
    list(TRANSFORM ITEMS APPEND "${ARG_APPEND}")
  endif()

  separate_arguments(ITEMS UNIX_COMMAND "${ITEMS}")

  set(${OUTPUT} "${ITEMS}" PARENT_SCOPE)
endfunction(join_list)

function(do_host_compile lang OUTPUT)
  include(DetermineHOST${lang}Compiler)

  set(oneValueArgs SOURCE TARGET)
  set(multiValueArgs INCLUDE_DIRECTORIES COMPILE_OPTIONS)
  cmake_parse_arguments(BUILD "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  # FIXME: compute the standard option properly
  if(DEFINED CMAKE_HOST${lang}_STANDARD)
    if(NOT DEFINED CMAKE_HOST${lang}_EXTENSIONS OR CMAKE_HOST${lang}_EXTENSIONS)
      list(PREPEND BUILD_COMPILE_OPTIONS "-std=gnu${CMAKE_HOST${lang}_STANDARD}")
    else()
      list(PREPEND BUILD_COMPILE_OPTIONS "-std=c${CMAKE_HOST${lang}_STANDARD}")
    endif()
  endif()

  # FIXME: "-isystem" needs to be set properly
  join_list(BUILD_IMPLICIT_INCLUDE_DIRECTORIES INPUT "${CMAKE_HOST${lang}_IMPLICIT_INCLUDE_DIRECTORIES}" PREPEND "-isystem")
  join_list(BUILD_INCLUDE_DIRECTORIES PREPEND "${CMAKE_INCLUDE_FLAG_C}")
  join_list(BUILD_COMPILE_OPTIONS)

  # Set path to the output file
  set(_absolute_output "${CMAKE_CURRENT_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/${BUILD_TARGET}.dir/${BUILD_SOURCE}.o")
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
    string(REPLACE "\\" "" _output "${_output}")
    string(REPLACE "\n" "" _output "${_output}")
    separate_arguments(BUILD_FILE_DEPENDENCIES UNIX_COMMAND "${_output}")
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
    DEPENDS ${BUILD_FILE_DEPENDENCIES}
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
