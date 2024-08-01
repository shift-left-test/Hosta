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

get_host_target_names(OUTPUT "{target}")
cmake_print_variables(OUTPUT)
'''

def test_empty_target_name(testing):
    testing.write("CMakeLists.txt", content.format(target=""))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'OUTPUT=""' in testing.configure_internal(options).stdout

def test_target_name_with_unknown_namespace(testing):
    testing.write("CMakeLists.txt", content.format(target="ABC::hello;ABC::world"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'OUTPUT="ABC::hello;ABC::world"' in testing.configure_internal(options).stdout

def test_target_name_with_long_unknown_namespace(testing):
    testing.write("CMakeLists.txt", content.format(target="ABC::Host::hello;ABC::Host::world"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'OUTPUT="ABC::Host::hello;ABC::Host::world"' in testing.configure_internal(options).stdout

def test_plain_target_name(testing):
    testing.write("CMakeLists.txt", content.format(target="hello;world"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'OUTPUT="hello;world"' in testing.configure_internal(options).stdout

def test_target_name_with_host_namespace(testing):
    testing.write("CMakeLists.txt", content.format(target="Host::hello;Host::world"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'OUTPUT="HOST-hello;HOST-world"' in testing.configure_internal(options).stdout

def test_target_name_with_nested_host_namespace(testing):
    testing.write("CMakeLists.txt", content.format(target="Host::Host::hello;Host::Host::world"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'OUTPUT="HOST-Host::hello;HOST-Host::world"' in testing.configure_internal(options).stdout
