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
parse_host_compiler_abi_info(C {path})
message(STATUS "CMAKE_HOSTC_COMPILER_ABI: ${{CMAKE_HOSTC_COMPILER_ABI}}")
'''

def test_parse_unknown_file(testing):
    testing.write("CMakeLists.txt", content.format(path="unknown.file"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'CMAKE_HOSTC_COMPILER_ABI: \n' in testing.configure_internal(options).stdout

def test_parse_missing_abi_info(testing):
    testing.write("CMakeLists.txt", content.format(path="test.bin"))
    testing.write("test.bin", "INFO:a[]\nINFO:b[]\n")
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'CMAKE_HOSTC_COMPILER_ABI: \n' in testing.configure_internal(options).stdout

def test_parse_abi_info(testing):
    testing.write("CMakeLists.txt", content.format(path="test.bin"))
    testing.write("test.bin", "INFO:a[]\nINFO:b[]\nINFO:abi[hello]\n")
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'CMAKE_HOSTC_COMPILER_ABI: hello\n' in testing.configure_internal(options).stdout
