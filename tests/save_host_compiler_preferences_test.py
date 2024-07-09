#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

content = '''
cmake_minimum_required(VERSION 3.16 FATAL_ERROR)

project(CMakeTest LANGUAGES NONE)

include(cmake/HostCompilerUtilities.cmake)

set(CMAKE_HOSTX_COMPILER "hello")

set(CMAKE_HOSTX90_STANDARD_COMPILE_OPTION "x90")
set(CMAKE_HOSTX26_EXTENSION_COMPILE_OPTION "x26")
set(CMAKE_HOSTX27_STANDARD_COMPILE_OPTION "x27")

save_host_compiler_preferences(X)
'''

def test_save_file(testing):
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    testing.configure_internal(options)
    assert 'set(CMAKE_HOSTX_COMPILER "hello")' in testing.read("CMakeFiles/3.16.3/CMakeHOSTXCompiler.cmake")

def test_valid_language_standard_versions(testing):
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    testing.configure_internal(options)
    assert 'set(CMAKE_HOSTX90_STANDARD_COMPILE_OPTION "x90")' in testing.read("CMakeFiles/3.16.3/CMakeHOSTXCompiler.cmake")
    assert 'set(CMAKE_HOSTX26_EXTENSION_COMPILE_OPTION "x26")' in testing.read("CMakeFiles/3.16.3/CMakeHOSTXCompiler.cmake")

def test_invalid_language_standard_versions(testing):
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    testing.configure_internal(options)
    assert 'set(CMAKE_HOSTX27_STANDARD_COMPILE_OPTION "x27")' not in testing.read("CMakeFiles/3.16.3/CMakeHOSTXCompiler.cmake")
