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

host_logging_error({messages})
'''

def test_failure(testing):
    testing.write("CMakeLists.txt", content.format(messages='"hello"'))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert testing.configure_internal(options).returncode != 0

def test_messages_on_console(testing):
    testing.write("CMakeLists.txt", content.format(messages='"hello" "world"'))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert '  hello\n\n  world' in testing.configure_internal(options).stderr

def test_messages_on_file(testing):
    testing.write("CMakeLists.txt", content.format(messages='"hello" "world"'))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    testing.configure_internal(options)
    assert 'hello\nworld\n\n' in testing.read("CMakeFiles/CMakeError.log")
