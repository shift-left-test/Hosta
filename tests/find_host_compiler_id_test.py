#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

def test_unknown_host_compiler(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16 FATAL_ERROR)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostCompilerUtilities.cmake)
    include(CMakeTestCompilerCommon)
    set(CMAKE_HOSTC_COMPILER "unknown")
    set(CMAKE_HOSTC_COMPILER_WORKS TRUE)
    find_host_compiler_id(C "-c" "-Aa" "-D__CLASSIC_C__" "--target=arm-arm-none-eabi -mcpu=cortex-m3")
    message(STATUS "CMAKE_HOSTC_COMPILER_ID: ${CMAKE_HOSTC_COMPILER_ID}")
    '''
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'CMAKE_HOSTC_COMPILER_ID: \n' in testing.configure_internal(options).stdout

def test_known_host_compiler(testing):
    content = '''
    cmake_minimum_required(VERSION 3.16 FATAL_ERROR)
    project(CMakeTest LANGUAGES NONE)
    include(cmake/HostCompilerUtilities.cmake)
    include(CMakeTestCompilerCommon)
    set(CMAKE_HOSTC_COMPILER_LIST "clang")
    find_host_compiler(C)
    find_host_compiler_id(C "-c" "-Aa" "-D__CLASSIC_C__" "--target=arm-arm-none-eabi -mcpu=cortex-m3")
    message(STATUS "CMAKE_HOSTC_COMPILER_ID: ${CMAKE_HOSTC_COMPILER_ID}")
    message(STATUS "CMAKE_HOSTC_COMPILER_VERSION: ${CMAKE_HOSTC_COMPILER_VERSION}")
    message(STATUS "CMAKE_HOSTC_PLATFORM_ID: ${CMAKE_HOSTC_PLATFORM_ID}")
    message(STATUS "CMAKE_HOSTC_STANDARD_COMPUTED_DEFAULT: ${CMAKE_HOSTC_STANDARD_COMPUTED_DEFAULT}")
    message(STATUS "CMAKE_HOSTC_VERBOSE_FLAG: ${CMAKE_HOSTC_VERBOSE_FLAG}")
    message(STATUS "CMAKE_INCLUDE_SYSTEM_FLAG_HOSTC: ${CMAKE_INCLUDE_SYSTEM_FLAG_HOSTC}")

    list(APPEND versions 90 98 99 03 11 14 17 20 23 26)
    foreach(version IN LISTS versions)
      message(STATUS "CMAKE_HOSTC${version}_STANDARD_COMPILE_OPTION: ${CMAKE_HOSTC${version}_STANDARD_COMPILE_OPTION}")
      message(STATUS "CMAKE_HOSTC${version}_EXTENSION_COMPILE_OPTION: ${CMAKE_HOSTC${version}_EXTENSION_COMPILE_OPTION}")
    endforeach()
    '''
    testing.write("CMakeLists.txt", content)
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    stdout = testing.configure_internal(options).stdout
    assert 'CMAKE_HOSTC_COMPILER_ID: Clang' in stdout
    assert 'CMAKE_HOSTC_COMPILER_VERSION: 10.0.0' in stdout
    assert 'CMAKE_HOSTC_PLATFORM_ID: Linux' in stdout
    assert 'CMAKE_HOSTC_STANDARD_COMPUTED_DEFAULT: 11' in stdout
    assert 'CMAKE_HOSTC_VERBOSE_FLAG: -v' in stdout
    assert 'CMAKE_INCLUDE_SYSTEM_FLAG_HOSTC: -isystem' in stdout
    assert 'CMAKE_HOSTC90_STANDARD_COMPILE_OPTION: -std=c90' in stdout
    assert 'CMAKE_HOSTC90_EXTENSION_COMPILE_OPTION: -std=gnu90' in stdout
