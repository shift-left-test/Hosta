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

set(CMAKE_HOSTC_PLATFORM_ID {platform})

set_host_platform_default_options(C)

include(CMakePrintHelpers)
cmake_print_variables(
  CMAKE_HOSTC_OUTPUT_EXTENSION
  CMAKE_HOST_EXECUTABLE_SUFFIX
  CMAKE_HOST_STATIC_LIBRARY_PREFIX
  CMAKE_HOST_STATIC_LIBRARY_SUFFIX
)
'''

def test_unknown_host_platform(testing):
    testing.write("CMakeLists.txt", content.format(platform="unknown"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert "Builds hosted on 'unknown' not supported." in testing.configure_internal(options).stderr

def test_cygwin(testing):
    testing.write("CMakeLists.txt", content.format(platform="CYGWIN"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    stdout = testing.configure_internal(options).stdout
    assert 'CMAKE_HOSTC_OUTPUT_EXTENSION=".obj"' in stdout
    assert 'CMAKE_HOST_EXECUTABLE_SUFFIX=".exe"' in stdout
    assert 'CMAKE_HOST_STATIC_LIBRARY_PREFIX=""' in stdout
    assert 'CMAKE_HOST_STATIC_LIBRARY_SUFFIX=".lib"' in stdout

def test_linux(testing):
    testing.write("CMakeLists.txt", content.format(platform="Linux"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    stdout = testing.configure_internal(options).stdout
    assert 'CMAKE_HOSTC_OUTPUT_EXTENSION=".o"' in stdout
    assert 'CMAKE_HOST_EXECUTABLE_SUFFIX=""' in stdout
    assert 'CMAKE_HOST_STATIC_LIBRARY_PREFIX="lib"' in stdout
    assert 'CMAKE_HOST_STATIC_LIBRARY_SUFFIX=".a"' in stdout

def test_mingw(testing):
    testing.write("CMakeLists.txt", content.format(platform="MinGW"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    stdout = testing.configure_internal(options).stdout
    assert 'CMAKE_HOSTC_OUTPUT_EXTENSION=".obj"' in stdout
    assert 'CMAKE_HOST_EXECUTABLE_SUFFIX=".exe"' in stdout
    assert 'CMAKE_HOST_STATIC_LIBRARY_PREFIX=""' in stdout
    assert 'CMAKE_HOST_STATIC_LIBRARY_SUFFIX=".lib"' in stdout

def test_windows(testing):
    testing.write("CMakeLists.txt", content.format(platform="Windows"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    stdout = testing.configure_internal(options).stdout
    assert 'CMAKE_HOSTC_OUTPUT_EXTENSION=".obj"' in stdout
    assert 'CMAKE_HOST_EXECUTABLE_SUFFIX=".exe"' in stdout
    assert 'CMAKE_HOST_STATIC_LIBRARY_PREFIX=""' in stdout
    assert 'CMAKE_HOST_STATIC_LIBRARY_SUFFIX=".lib"' in stdout
