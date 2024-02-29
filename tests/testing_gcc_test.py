#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

def test_test_targets_work(testing_gcc):
    testing_gcc.cmake("build-test").check_returncode()
    testing_gcc.cmake("test").check_returncode()

def test_ctest_works(testing_gcc):
    testing_gcc.cmake("build-test")
    assert "unittest_unittest ................   Passed" in testing_gcc.ctest().stdout

def test_gcovr_works(testing_gcc):
    testing_gcc.cmake("build-test")
    testing_gcc.ctest()
    assert "sample/test/test_main.c                       15      15   100%" in testing_gcc.gcovr().stdout

def test_host_compiler_info(testing_gcc):
    compiler_info = testing_gcc.read("CMakeFiles/3.16.3/CMakeHOSTCCompiler.cmake")
    assert 'set(CMAKE_HOSTC_COMPILER "/usr/bin/gcc")' in compiler_info
    assert 'set(CMAKE_HOSTC_COMPILER_WORKS TRUE)' in compiler_info
    assert 'set(CMAKE_HOSTC_ABI_COMPILED TRUE)' in compiler_info
    assert 'set(CMAKE_HOSTC_COMPILER_ABI "ELF")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_INCLUDE_DIRECTORIES "/usr/lib/gcc/x86_64-linux-gnu/9/include;/usr/local/include;/usr/include/x86_64-linux-gnu;/usr/include")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_LIBRARIES "gcc;gcc_s;c;gcc;gcc_s")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_DIRECTORIES "/usr/lib/gcc/x86_64-linux-gnu/9;/usr/lib/x86_64-linux-gnu;/usr/lib;/lib/x86_64-linux-gnu;/lib")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_FRAMEWORK_DIRECTORIES "")' in compiler_info
