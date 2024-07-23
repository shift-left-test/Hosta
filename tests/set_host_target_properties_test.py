#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

content = '''
cmake_minimum_required(VERSION 3.16 FATAL_ERROR)

project(CMakeTest LANGUAGES NONE)

include(CMakePrintHelpers)
include(cmake/HostBuild.cmake)

add_custom_target(hello COMMAND echo "hello")

set_host_target_properties({target}
  TYPE "A"
  TARGET_FILE "B"
  SOURCES "C"
  INTERFACE_INCLUDE_DIRECTORIES "D"
  INTERFACE_COMPILE_OPTIONS "E"
  INTERFACE_LINK_OPTIONS "F"
)

get_host_target_properties(hello
  NAME name
  TYPE type
  TARGET_FILE target_file
  SOURCES sources
  INTERFACE_INCLUDE_DIRECTORIES include_directories
  INTERFACE_COMPILE_OPTIONS compile_options
  INTERFACE_LINK_OPTIONS link_options
)

cmake_print_variables(name type target_file sources include_directories compile_options link_options)
'''

def test_unknown_target_name(testing):
    testing.write("CMakeLists.txt", content.format(target="unknown"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'set_host_target_property() called with non-existent target "unknown".' in testing.configure_internal(options).stderr

def test_get_set_properties(testing):
    testing.write("CMakeLists.txt", content.format(target="hello"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    stdout = testing.configure_internal(options).stdout
    assert 'name="hello"' in stdout
    assert 'type="A"' in stdout
    assert 'target_file="B"' in stdout
    assert 'sources="C"' in stdout
    assert 'include_directories="D"' in stdout
    assert 'compile_options="E"' in stdout
    assert 'link_options="F"' in stdout
