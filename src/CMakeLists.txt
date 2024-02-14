# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

add_executable(unittest test_main.c)
target_link_libraries(unittest PRIVATE unity)

add_test(NAME unittest COMMAND $<TARGET_FILE:unittest>)
