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

add_host_executable(hello
  SOURCES {source}
)
'''

def test_no_source(testing):
    testing.write("CMakeLists.txt", content.format(source=""))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'No SOURCES given to target: hello' in testing.configure_internal(options).stderr

def test_unknown_source(testing):
    testing.write("CMakeLists.txt", content.format(source="unknown.c"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'Cannot find source file:\n\n    unknown.c' in testing.configure_internal(options).stderr
