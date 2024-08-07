#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

def test_existing_target(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(hello STATIC SOURCES hello.c)
    add_host_library(hello STATIC SOURCES hello.c)
    '''
    testing.write("hello.c", "void hello() {}")
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'add_custom_target cannot create target "HOST-hello"' in testing.configure_internal(options).stderr

def test_host_namespace_target(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(Host::hello STATIC SOURCES hello.c)
    '''
    testing.write("hello.c", "int hello() { return 0; }")
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    testing.configure_internal(options).check_returncode()
    assert 'Linking HOSTC static library libhello.a' in testing.cmake("host-targets", verbose=True).stdout

def test_unknown_type(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(hello unknown SOURCES hello.c)
    '''
    testing.write("hello.c", "void hello() {}")
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'Unsupported library type: unknown' in testing.configure_internal(options).stderr

def test_static_no_source(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(hello STATIC)
    '''
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'No SOURCES given to target: hello' in testing.configure_internal(options).stderr

def test_static_unknown_source(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(hello STATIC SOURCES unknown.c)
    '''
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'Cannot find source file:\n\n    unknown.c' in testing.configure_internal(options).stderr

def test_static_sources(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(main STATIC SOURCES hello.c world.c)
    '''
    testing.write("hello.c", "void hello() { }")
    testing.write("world.c", "void world() { }")
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    testing.configure_internal(options).check_returncode()
    testing.cmake("host-targets").check_returncode()

def test_static_include_directories(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(hello STATIC SOURCES hello.c INCLUDE_DIRECTORIES PUBLIC first second)
    '''
    testing.write("hello.c", "int hello() { return 0; }")
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    testing.configure_internal(options).check_returncode()
    assert f'-I{testing.workspace}/first -I{testing.workspace}/second' in testing.cmake("host-targets", verbose=True).stdout

def test_static_compile_options(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(hello STATIC SOURCES hello.c COMPILE_OPTIONS PUBLIC -DHELLO)
    '''
    testing.write("hello.c", "int hello() { return 0; }")
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    testing.configure_internal(options).check_returncode()
    assert '-DHELLO' in testing.cmake("host-targets", verbose=True).stdout

def test_static_link_options(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(hello STATIC SOURCES hello.c LINK_OPTIONS PUBLIC -fprofile-arcs -lm)
    '''
    testing.write("hello.c", "int hello() { return 0; }")
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    testing.configure_internal(options).check_returncode()
    testing.cmake("host-targets").check_returncode()

def test_static_rebuild(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(hello STATIC SOURCES hello.c)
    '''
    testing.write("hello.c", "int hello() { return 0; }")
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    testing.configure_internal(options).check_returncode()
    assert 'Linking HOSTC static library' in testing.cmake("host-targets").stdout
    assert not 'Linking HOSTC static library' in testing.cmake("host-targets").stdout

def test_interface_sources(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(hello INTERFACE SOURCES hello.c)
    '''
    testing.write("hello.c", "int hello() { return 0; }")
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'add_host_library INTERFACE requires no source arguments.' in testing.configure_internal(options).stderr

def test_interface_include_directories(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(CMakePrintHelpers)
    include(cmake/HostBuild.cmake)
    add_host_library(hello INTERFACE INCLUDE_DIRECTORIES PRIVATE a PUBLIC b)
    get_host_target_properties(Host::hello
      INCLUDE_DIRECTOIRES A
      INTERFACE_INCLUDE_DIRECTORIES B
    )
    cmake_print_variables(A B)
    '''
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert f'A="" ; B="{testing.workspace}/b"' in testing.configure_internal(options).stdout

def test_interface_compile_options(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(CMakePrintHelpers)
    include(cmake/HostBuild.cmake)
    add_host_library(hello INTERFACE COMPILE_OPTIONS PRIVATE a PUBLIC b)
    get_host_target_properties(Host::hello
      COMPILE_OPTIONS A
      INTERFACE_COMPILE_OPTIONS B
    )
    cmake_print_variables(A B)
    '''
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert f'A="" ; B="b"' in testing.configure_internal(options).stdout

def test_interface_link_options(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(CMakePrintHelpers)
    include(cmake/HostBuild.cmake)
    add_host_library(hello INTERFACE LINK_OPTIONS PRIVATE a PUBLIC b)
    get_host_target_properties(Host::hello
      LINK_OPTIONS A
      INTERFACE_LINK_OPTIONS B
    )
    cmake_print_variables(A B)
    '''
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert f'A="" ; B="b"' in testing.configure_internal(options).stdout

def test_static_rebuild(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostBuild.cmake)
    add_host_library(hello INTERFACE)
    '''
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    testing.configure_internal(options).check_returncode()
    assert 'Scanning dependencies of target HOST-hello' in testing.cmake("host-targets").stdout
    assert not 'Scanning dependencies of target HOST-hello' in testing.cmake("host-targets").stdout
