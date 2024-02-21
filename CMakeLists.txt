# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

cmake_minimum_required(VERSION 3.16 FATAL_ERROR)

project(host-unittest LANGUAGES NONE)

set(CMAKE_EXECUTABLE_SUFFIX .out)

option(WITH_TEST "Enable unit testing" OFF)

if(WITH_TEST)
  enable_testing()
endif()

list(APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)
include(unittest)

add_subdirectory(src)
