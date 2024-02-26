# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

cmake_minimum_required(VERSION 3.10 FATAL_ERROR)

add_unittest(unittest
  SOURCES src/calc.c test/test_main.c test/unity.c
  INCLUDE_DIRECTORIES ${CMAKE_CURRENT_LIST_DIR}/src
)
