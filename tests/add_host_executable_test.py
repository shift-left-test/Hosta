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
  {exe_args}
)

if(WITH_LIB)
add_host_library(world STATIC
  {lib_args}
)
endif()
'''

def test_no_source(testing):
    testing.write("CMakeLists.txt", content.format(exe_args='SOURCES ""', lib_args=''))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'No SOURCES given to target: hello' in testing.configure_internal(options).stderr

def test_unknown_source(testing):
    testing.write("CMakeLists.txt", content.format(exe_args='SOURCES "unknown.c"', lib_args=''))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'Cannot find source file:\n\n    unknown.c' in testing.configure_internal(options).stderr

def test_standalone_source(testing):
    testing.write("main.c", "#include <stdio.h> \n int main() { return 0; }")
    testing.write("CMakeLists.txt", content.format(exe_args='SOURCES "main.c"', lib_args=''))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    testing.configure_internal(options).check_returncode()
    testing.cmake("host-targets").check_returncode()

def test_link_library(testing):
    testing.write("main.c", '#include "world.h" \n int main() { world(); return 0; }')
    testing.write("world/world.h", "void world();")
    testing.write("world/world.c", '#include "world.h" \n void world() { }')
    testing.write("CMakeLists.txt", content.format(exe_args='SOURCES "main.c" LINK_LIBRARIES "Host::world"',
                                                   lib_args='SOURCES "world/world.c" INCLUDE_DIRECTORIES "${CMAKE_CURRENT_LIST_DIR}/world"'))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace} -DWITH_LIB=True']
    testing.configure_internal(options).check_returncode()
    testing.cmake("host-targets").check_returncode()
