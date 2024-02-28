# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

cmake_minimum_required(VERSION 3.10 FATAL_ERROR)

option(WITH_MINGW "Enable mingw cross toolchain" ON)
option(WITH_TEST "Enable unit testing" ON)

if(WITH_MINGW)
  # the name of the target operating system
  set(CMAKE_SYSTEM_NAME Windows)

  # which compilers to use for C and C++
  set(CMAKE_C_COMPILER   i686-w64-mingw32-gcc)
  set(CMAKE_CXX_COMPILER i686-w64-mingw32-g++)

  # where is the target environment located
  set(CMAKE_FIND_ROOT_PATH  /usr/i686-w64-mingw32)

  # adjust the default behavior of the FIND_XXX() commands:
  # search programs in the host environment
  set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)

  # search headers and libraries in the target environment
  set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
  set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
endif()

project(host-unittest LANGUAGES C)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_EXECUTABLE_SUFFIX .out)

if(WITH_TEST)
  enable_testing()
endif()

list(APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)
include(unittest)

add_subdirectory(sample)
