# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

cmake_minimum_required(VERSION 3.16 FATAL_ERROR)

option(WITH_CROSS_TOOLCHAIN "Enable cross toolchain" ON)
option(WITH_HOST_TEST "Enable host based testing" ON)
option(WITH_DEBUG_SYMBOL "Enable debug symbol" OFF)
option(WITH_LIBM "Enable math library" OFF)

if(WITH_CROSS_TOOLCHAIN)
  # the name of the target operating system
  set(CMAKE_SYSTEM_NAME Windows)

  # which compilers to use for C and C++
  set(CMAKE_C_COMPILER i686-w64-mingw32-gcc)
  set(CMAKE_CXX_COMPILER i686-w64-mingw32-g++)

  # where is the target environment located
  set(CMAKE_FIND_ROOT_PATH /usr/i686-w64-mingw32)

  # adjust the default behavior of the FIND_XXX() commands:
  # search programs in the host environment
  set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)

  # search headers and libraries in the target environment
  set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
  set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
endif()

project(host-test LANGUAGES C)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_HOSTC_EXECUTABLE_SUFFIX .out)

if(WITH_HOST_TEST)
  enable_testing()
endif()

include(cmake/HostTest.cmake)

list(APPEND HOST_COMPILE_OPTIONS -DUNITY_FIXTURE_NO_EXTRAS -DUNITY_INCLUDE_DOUBLE)

if(WITH_DEBUG_SYMBOL)
  list(APPEND HOST_COMPILE_OPTIONS -g)
endif()

if(WITH_LIBM)
  list(APPEND HOST_LINK_OPTIONS -lm)
endif()

add_custom_target(hello
  COMMAND echo "hello"
)

add_host_test(unittest
  SOURCES src/calc.c test/unity_test_main.c ${CMAKE_CURRENT_LIST_DIR}/unity/unity.c
  INCLUDE_DIRECTORIES ${CMAKE_CURRENT_LIST_DIR}/src ${CMAKE_CURRENT_LIST_DIR}/test ./unity
  COMPILE_OPTIONS ${HOST_COMPILE_OPTIONS}
  LINK_OPTIONS ${HOST_LINK_OPTIONS}
  DEPENDS hello
)

add_subdirectory(src)
add_subdirectory(disabled_test)
add_subdirectory(fixture_tests)
add_subdirectory(relative_path_test)
