#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

def test_build_target_works(testing_cc):
    testing_cc.cmake("all").check_returncode()

def test_test_targets_work(testing_cc):
    testing_cc.cmake("build-test").check_returncode()
    testing_cc.ctest().check_returncode()

def test_compile_works(testing_cc):
    testing_cc.cmake("build-test").check_returncode()
    assert testing_cc.exists("sample/CMakeFiles/unittest.dir/src/calc.c.o")
    assert testing_cc.exists("sample/CMakeFiles/unittest.dir/test/test_main.c.o")

def test_link_works(testing_cc):
    testing_cc.cmake("build-test").check_returncode()
    assert testing_cc.exists("sample/unittest.out")

def test_no_output_interference(testing_cc):
    testing_cc.prepare("")
    testing_cc.cmake("build-test").check_returncode()
    testing_cc.prepare("temp")
    testing_cc.cmake("build-test").check_returncode()

def test_ctest_works(testing_cc):
    testing_cc.cmake("build-test")
    assert "unittest .........................   Passed" in testing_cc.ctest().stdout

def test_gcovr_works(testing_cc):
    testing_cc.cmake("build-test")
    testing_cc.ctest()
    assert "sample/test/test_main.c                       15      15   100%" in testing_cc.gcovr().stdout

def test_host_compiler_info(testing_cc):
    compiler_info = testing_cc.read("CMakeFiles/3.16.3/CMakeHOSTCCompiler.cmake")
    assert 'set(CMAKE_HOSTC_COMPILER "/usr/bin/cc")' in compiler_info
    assert 'set(CMAKE_HOSTC_COMPILER_WORKS TRUE)' in compiler_info
    assert 'set(CMAKE_HOSTC_ABI_COMPILED TRUE)' in compiler_info
    assert 'set(CMAKE_HOSTC_COMPILER_ABI "ELF")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_INCLUDE_DIRECTORIES "/usr/lib/gcc/x86_64-linux-gnu/9/include;/usr/local/include;/usr/include/x86_64-linux-gnu;/usr/include")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_LIBRARIES "gcc;gcc_s;c;gcc;gcc_s")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_DIRECTORIES "/usr/lib/gcc/x86_64-linux-gnu/9;/usr/lib/x86_64-linux-gnu;/usr/lib;/lib/x86_64-linux-gnu;/lib")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_FRAMEWORK_DIRECTORIES "")' in compiler_info
