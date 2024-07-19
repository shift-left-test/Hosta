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

set_host_target_property({target} {key} "{value}")
get_target_property(OUTPUT {target} {key})

cmake_print_variables(OUTPUT)
'''

def test_unknown_target_name(testing):
    testing.write("CMakeLists.txt", content.format(target="unknown", key="HOST_SOURCES", value="abc"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'set_host_target_property() called with non-existent target "unknown".' in testing.configure_internal(options).stderr

def test_set_read_only_property(testing):
    testing.write("CMakeLists.txt", content.format(target="hello", key="NAME", value="abc"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'NAME property is read-only' in testing.configure_internal(options).stderr

def test_set_anonymous_property(testing):
    testing.write("CMakeLists.txt", content.format(target="hello", key="UNKNOWN", value="abc"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'OUTPUT="abc"' in testing.configure_internal(options).stdout

def test_set_property_single_value(testing):
    testing.write("CMakeLists.txt", content.format(target="hello", key="HOST_SOURCES", value="abc"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'OUTPUT="abc"' in testing.configure_internal(options).stdout

def test_set_property_multi_values(testing):
    testing.write("CMakeLists.txt", content.format(target="hello", key="HOST_SOURCES", value="a;b;c"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'OUTPUT="a;b;c"' in testing.configure_internal(options).stdout
