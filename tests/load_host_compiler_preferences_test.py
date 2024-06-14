#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

content = '''
cmake_minimum_required(VERSION 3.16 FATAL_ERROR)

project(CMakeTest)

include(cmake/HostCompilerUtilities.cmake)

load_host_compiler_preferences(X)

message(STATUS "load_host_compiler_preferences(X): ${DATA}")
'''

def test_unknown_file(testing):
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    testing.configure_internal(options)
    assert "load_host_compiler_preferences(X): hello" not in testing.configure_internal(options).stdout

def test_load_file(testing):
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    testing.configure_internal(options)
    testing.write("build/CMakeFiles/3.16.3/CMakeHOSTXCompiler.cmake", 'set(DATA "hello")\n')
    assert "load_host_compiler_preferences(X): hello" in testing.configure_internal(options).stdout
