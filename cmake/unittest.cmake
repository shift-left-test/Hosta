# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

# The compiler configuration was forced by the user.
# Assume the user has configured all compiler information
if(CMAKE_HOSTC_COMPILER_FORCED)
    set(CMAKE_HOSTC_COMPILER_WORKS TRUE)
    return()
endif()

# Load host compiler preferences
include(${CMAKE_PLATFORM_INFO_DIR}/CMakeHOSTCCompiler.cmake OPTIONAL)

if(NOT CMAKE_HOSTC_COMPILER_WORKS)

  # List compilers to try
  include(CMakeDetermineCompiler)
  set(CMAKE_HOSTC_COMPILER_LIST cc gcc clang)
  _cmake_find_compiler(HOSTC)

  mark_as_advanced(CMAKE_HOSTC_COMPILER)

  # Configure variables set in this file for fast reload later on
  file(WRITE ${CMAKE_PLATFORM_INFO_DIR}/CMakeHOSTCCompiler.cmake.in
    "set(CMAKE_HOSTC_COMPILER \"@CMAKE_HOSTC_COMPILER@\")")

  configure_file(
    ${CMAKE_PLATFORM_INFO_DIR}/CMakeHOSTCCompiler.cmake.in
    ${CMAKE_PLATFORM_INFO_DIR}/CMakeHOSTCCompiler.cmake
    @ONLY
  )

endif()
