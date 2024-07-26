#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

content = '''
cmake_minimum_required(VERSION 3.16 FATAL_ERROR)

project(CMakeTest LANGUAGES NONE)

set(CMAKE_HOSTC_COMPILER_LIST {compiler})

include(cmake/DetermineHOSTCCompiler.cmake)

find_host_binutils(C)

include(CMakePrintHelpers)
cmake_print_variables(CMAKE_HOST_AR)
cmake_print_variables(CMAKE_HOST_RANLIB)
'''

def test_unknown_host_compiler(testing):
    testing.write("CMakeLists.txt", content.format(compiler="unknown"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'The CMAKE_HOSTC_COMPILER:\n\n    unknown\n\n  \n\n   is not a full path and was not found in the PATH.' in testing.configure_internal(options).stderr

def test_find_binutils_of_cc_compiler(testing):
    testing.write("CMakeLists.txt", content.format(compiler="cc"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'CMAKE_HOST_AR="/usr/bin/ar"' in testing.configure_internal(options).stdout
    assert 'CMAKE_HOST_RANLIB="/usr/bin/ranlib"' in testing.configure_internal(options).stdout

def test_find_binutils_of_gcc_compiler(testing):
    testing.write("CMakeLists.txt", content.format(compiler="gcc"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'CMAKE_HOST_AR="/usr/bin/ar"' in testing.configure_internal(options).stdout
    assert 'CMAKE_HOST_RANLIB="/usr/bin/ranlib"' in testing.configure_internal(options).stdout

def test_find_binutils_of_clang_compiler(testing):
    testing.write("CMakeLists.txt", content.format(compiler="clang"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'CMAKE_HOST_AR="/usr/bin/ar"' in testing.configure_internal(options).stdout
    assert 'CMAKE_HOST_RANLIB="/usr/bin/ranlib"' in testing.configure_internal(options).stdout

def test_find_binutils_of_clang_compiler(testing):
    testing.write("CMakeLists.txt", content.format(compiler="i686-w64-mingw32-gcc"))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'CMAKE_HOST_AR="/usr/bin/i686-w64-mingw32-ar"' in testing.configure_internal(options).stdout
    assert 'CMAKE_HOST_RANLIB="/usr/bin/i686-w64-mingw32-ranlib"' in testing.configure_internal(options).stdout
