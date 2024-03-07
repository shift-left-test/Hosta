# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

cmake_minimum_required(VERSION 3.10 FATAL_ERROR)

add_executable(calc src/calc.c src/main.c)

add_host_test(unittest
  SOURCES src/calc.c test/test_main.c test/unity.c
  INCLUDE_DIRECTORIES ${CMAKE_CURRENT_LIST_DIR}/src ${CMAKE_CURRENT_LIST_DIR}/test
)
