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

add_custom_target({first} COMMAND echo "first")
add_custom_target({second} COMMAND echo "second")

add_host_dependencies({command})
'''

def test_unknown_target_name(testing):
    testing.write("CMakeLists.txt", content.format(first="first", second="second", command="unknown unknown"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'Cannot add target-level dependencies to non-existent target "unknown".' in testing.configure_internal(options).stderr

def test_unknown_depend_name(testing):
    testing.write("CMakeLists.txt", content.format(first="first", second="second", command="first unknown"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'The dependency target "unknown" of target "first" does not exist.' in testing.configure_internal(options).stderr

def test_plain_target_depend_names(testing):
    testing.write("CMakeLists.txt", content.format(first="first", second="second", command="first second"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    testing.configure_internal(options).check_returncode()

def test_host_target_name(testing):
    testing.write("CMakeLists.txt", content.format(first="HOST-first", second="second", command="Host::first second"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    testing.configure_internal(options).check_returncode()

def test_host_depend_name(testing):
    testing.write("CMakeLists.txt", content.format(first="first", second="HOST-second", command="first Host::second"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    testing.configure_internal(options).check_returncode()

def test_host_target_and_depend_name(testing):
    testing.write("CMakeLists.txt", content.format(first="HOST-first", second="HOST-second", command="Host::first Host::second"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    testing.configure_internal(options).check_returncode()

def test_host_namespace_with_plain_target_name(testing):
    testing.write("CMakeLists.txt", content.format(first="first", second="HOST-second", command="Host::first Host::second"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'Cannot add target-level dependencies to non-existent target "HOST-first".' in testing.configure_internal(options).stderr

def test_host_namespace_with_plain_depend_name(testing):
    testing.write("CMakeLists.txt", content.format(first="HOST-first", second="second", command="Host::first Host::second"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'The dependency target "HOST-second" of target "HOST-first" does not exist.' in testing.configure_internal(options).stderr
