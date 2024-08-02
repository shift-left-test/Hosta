#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

content = '''
cmake_minimum_required(VERSION 3.16 FATAL_ERROR)

project(CMakeTest LANGUAGES NONE)

include(cmake/HostBuild.cmake)

separate_host_scoped_arguments("{text}" OUTPUT INTERFACE_OUTPUT)

include(CMakePrintHelpers)
cmake_print_variables(OUTPUT INTERFACE_OUTPUT)
'''

def test_unknown_format(testing):
    testing.write("CMakeLists.txt", content.format(text="unknown"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'The function called with invalid arguments' in testing.configure_internal(options).stderr

def test_empty_string(testing):
    testing.write("CMakeLists.txt", content.format(text=""))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'OUTPUT="" ; INTERFACE_OUTPUT=""' in testing.configure_internal(options).stdout

def test_private_empty_value(testing):
    testing.write("CMakeLists.txt", content.format(text="PRIVATE"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'OUTPUT="" ; INTERFACE_OUTPUT=""' in testing.configure_internal(options).stdout

def test_private_one_value(testing):
    testing.write("CMakeLists.txt", content.format(text="PRIVATE;one"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'OUTPUT="one" ; INTERFACE_OUTPUT=""' in testing.configure_internal(options).stdout

def test_private_multi_values(testing):
    testing.write("CMakeLists.txt", content.format(text="PRIVATE;one;two"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'OUTPUT="one;two" ; INTERFACE_OUTPUT=""' in testing.configure_internal(options).stdout

def test_public_empty_value(testing):
    testing.write("CMakeLists.txt", content.format(text="PUBLIC"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'OUTPUT="" ; INTERFACE_OUTPUT=""' in testing.configure_internal(options).stdout

def test_public_one_value(testing):
    testing.write("CMakeLists.txt", content.format(text="PUBLIC;one"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'OUTPUT="one" ; INTERFACE_OUTPUT="one"' in testing.configure_internal(options).stdout

def test_public_multi_values(testing):
    testing.write("CMakeLists.txt", content.format(text="PUBLIC;one;two"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'OUTPUT="one;two" ; INTERFACE_OUTPUT="one;two"' in testing.configure_internal(options).stdout

def test_combined_multi_values(testing):
    testing.write("CMakeLists.txt", content.format(text="PUBLIC;one;two;PRIVATE;three;four;PUBLIC;five;PRIVATE;six"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'OUTPUT="one;two;three;four;five;six" ; INTERFACE_OUTPUT="one;two;five"' in testing.configure_internal(options).stdout
