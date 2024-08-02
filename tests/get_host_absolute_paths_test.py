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

get_host_absolute_paths(PATHS "{paths}")
cmake_print_variables(PATHS)
'''

def test_empty_path(testing):
    testing.write("CMakeLists.txt", content.format(paths=""))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'PATHS=""' in testing.configure_internal(options).stdout

def test_one_path(testing):
    testing.write("CMakeLists.txt", content.format(paths="first"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert f'PATHS="{testing.workspace}/first"' in testing.configure_internal(options).stdout

def test_multiple_paths(testing):
    testing.write("CMakeLists.txt", content.format(paths="first;second"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert f'PATHS="{testing.workspace}/first;{testing.workspace}/second"' in testing.configure_internal(options).stdout
