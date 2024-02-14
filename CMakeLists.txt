# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

cmake_minimum_required(VERSION 3.16 FATAL_ERROR)

project(host-unittest LANGUAGES C)

set(CMAKE_EXECUTABLE_SUFFIX .out)

enable_testing()

list(APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)
include(unittest)

add_subdirectory(src)
