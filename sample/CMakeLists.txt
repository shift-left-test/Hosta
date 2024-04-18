# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

cmake_minimum_required(VERSION 3.10 FATAL_ERROR)

add_executable(calc src/calc.c src/main.c)

if(WITH_DEBUG_SYMBOL)
  list(APPEND HOST_COMPILE_OPTIONS -g)
endif()

add_custom_target(hello
  COMMAND echo "hello"
)

add_host_test(unittest
  SOURCES src/calc.c test/test_main.c ${CMAKE_CURRENT_LIST_DIR}/unity/unity.c
  INCLUDE_DIRECTORIES ${CMAKE_CURRENT_LIST_DIR}/src ${CMAKE_CURRENT_LIST_DIR}/test ./unity
  COMPILE_OPTIONS ${HOST_COMPILE_OPTIONS}
  DEPENDS hello
)

add_subdirectory(test2)
