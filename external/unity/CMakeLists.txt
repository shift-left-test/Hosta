# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

add_library(unity unity.c)
target_include_directories(unity PUBLIC ${CMAKE_CURRENT_LIST_DIR})
