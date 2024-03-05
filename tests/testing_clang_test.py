#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

def test_build_target_works(testing_clang):
    testing_clang.cmake("all").check_returncode()

def test_test_targets_work(testing_clang):
    testing_clang.cmake("build-test").check_returncode()
    testing_clang.ctest().check_returncode()

def test_compile_works(testing_clang):
    testing_clang.cmake("build-test").check_returncode()
    assert testing_clang.exists("sample/CMakeFiles/unittest.dir/src/calc.c.o")
    assert testing_clang.exists("sample/CMakeFiles/unittest.dir/test/test_main.c.o")

def test_link_works(testing_clang):
    testing_clang.cmake("build-test").check_returncode()
    assert testing_clang.exists("sample/unittest.out")

def test_no_output_interference(testing_clang):
    testing_clang.prepare("")
    testing_clang.cmake("build-test").check_returncode()
    testing_clang.prepare("temp")
    testing_clang.cmake("build-test").check_returncode()

def test_ctest_works(testing_clang):
    testing_clang.cmake("build-test")
    assert "unittest .........................   Passed" in testing_clang.ctest().stdout

@pytest.mark.skip(reason="gcovr not working properly")
def test_gcovr_works(testing_clang):
    testing_clang.cmake("build-test")
    testing_clang.ctest()
    assert "sample/test/test_main.c                       15      15   100%" in testing_clang.gcovr().stdout

def test_host_compiler_info(testing_clang):
    compiler_info = testing_clang.read("CMakeFiles/3.16.3/CMakeHOSTCCompiler.cmake")
    assert 'set(CMAKE_HOSTC_COMPILER "/usr/bin/clang")' in compiler_info
    assert 'set(CMAKE_HOSTC_COMPILER_WORKS TRUE)' in compiler_info
    assert 'set(CMAKE_HOSTC_ABI_COMPILED TRUE)' in compiler_info
    assert 'set(CMAKE_HOSTC_COMPILER_ABI "ELF")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_INCLUDE_DIRECTORIES "/usr/local/include;/usr/lib/llvm-10/lib/clang/10.0.1/include;/usr/include/x86_64-linux-gnu;/usr/include")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_LIBRARIES "gcc;gcc_s;c;gcc;gcc_s")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_DIRECTORIES "/usr/lib/gcc/x86_64-linux-gnu/9;/usr/lib/x86_64-linux-gnu;/usr/lib64;/lib/x86_64-linux-gnu;/lib64;/usr/lib;/usr/lib/llvm-10/lib;/lib")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_FRAMEWORK_DIRECTORIES "")' in compiler_info
