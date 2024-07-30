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

remove_host_namespace_prefix(OUTPUT {target})

include(CMakePrintHelpers)
cmake_print_variables(OUTPUT)
'''

def test_empty_target_name(testing):
    testing.write("CMakeLists.txt", content.format(target=""))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'OUTPUT=""' in testing.configure_internal(options).stdout

def test_plain_target_name(testing):
    testing.write("CMakeLists.txt", content.format(target="hello"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'OUTPUT="hello"' in testing.configure_internal(options).stdout

def test_non_host_target_name(testing):
    testing.write("CMakeLists.txt", content.format(target="Target::hello"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'OUTPUT="Target::hello"' in testing.configure_internal(options).stdout

def test_host_target_name(testing):
    testing.write("CMakeLists.txt", content.format(target="Host::hello"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'OUTPUT="hello"' in testing.configure_internal(options).stdout

def test_nested_host_target_name(testing):
    testing.write("CMakeLists.txt", content.format(target="Host::Host::hello"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'OUTPUT="Host::hello"' in testing.configure_internal(options).stdout
