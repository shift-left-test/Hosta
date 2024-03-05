# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

include_guard(GLOBAL)

include(CMakeParseArguments)

function(load_host_compiler_preferences lang)
  # Set internal directory path if missing
  if(NOT CMAKE_PLATFORM_INFO_DIR)
    set(CMAKE_PLATFORM_INFO_DIR ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/${CMAKE_VERSION})
  endif()

  include(${CMAKE_PLATFORM_INFO_DIR}/CMakeHOST${lang}Compiler.cmake OPTIONAL)
endfunction()

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
endfunction()

function(find_host_compiler lang)
  include(CMakeDetermineCompiler)
  _cmake_find_compiler(HOST${lang})
  mark_as_advanced(CMAKE_HOST${lang}_COMPILER)
endfunction()

function(try_host_compile lang)
  set(oneValueArgs SOURCE TARGET WORKING_DIRECTORY RESULT_VARIABLE OUTPUT_VARIABLE)
  set(multiValueArgs COMPILE_OPTIONS)

  cmake_parse_arguments(BUILD "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

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
endfunction()

function(parse_host_compiler_abi_info lang bin)
  file(STRINGS "${bin}" ABI_STRINGS REGEX "INFO:[A-Za-z0-9_]+\\[[^]]*\\]")
  foreach(info ${ABI_STRINGS})
    if("${info}" MATCHES "INFO:abi\\[([^]]*)\\]")
      set(CMAKE_HOST${lang}_COMPILER_ABI "${CMAKE_MATCH_1}" PARENT_SCOPE)
      break()
    endif()
  endforeach()
endfunction()

function(parse_host_implicit_include_info lang text)
  include(CMakeParseImplicitIncludeInfo)

  set(implicit_incdirs "")

  cmake_parse_implicit_include_info("${text}" HOST${lang} implicit_incdirs log rv)

  file(APPEND ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeOutput.log
    "Parsed HOST${lang} implicit include dir info from above output: rv=${rv}\n${log}\n\n")

  set(CMAKE_HOST${lang}_IMPLICIT_INCLUDE_DIRECTORIES "${implicit_incdirs}" PARENT_SCOPE)
endfunction()

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
endfunction()
