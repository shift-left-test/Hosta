# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

cmake_minimum_required(VERSION 3.16 FATAL_ERROR)

# Set the cross compiler toolchain configuration
set(CMAKE_SYSTEM_NAME Windows)
set(CMAKE_C_COMPILER i686-w64-mingw32-gcc)
set(CMAKE_CXX_COMPILER i686-w64-mingw32-g++)
set(CMAKE_FIND_ROOT_PATH /usr/i686-w64-mingw32)
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)

project(sample LANGUAGES C)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_EXTENSIONS ON)

set(CMAKE_HOSTC_STANDARD 11)
set(CMAKE_HOSTC_EXTENSIONS ON)

include(../cmake/HostTest.cmake)

# Enable CTest
enable_testing()

add_subdirectory(src)
add_subdirectory(test)
add_subdirectory(external/unity)
add_subdirectory(external/fff)
