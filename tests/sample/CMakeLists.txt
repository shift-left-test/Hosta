# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

cmake_minimum_required(VERSION 3.16 FATAL_ERROR)

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
