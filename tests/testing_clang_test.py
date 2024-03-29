#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

def test_host_compiler_info(testing_clang):
    compiler_info = testing_clang.read("CMakeFiles/3.16.3/CMakeHOSTCCompiler.cmake")
    assert 'set(CMAKE_HOSTC_COMPILER "/usr/bin/clang")' in compiler_info
    assert 'set(CMAKE_HOSTC_COMPILER_ID "Clang")' in compiler_info
    assert 'set(CMAKE_HOSTC_COMPILER_VERSION "10.0.0")' in compiler_info
    assert 'set(CMAKE_HOSTC_COMPILER_WORKS TRUE)' in compiler_info
    assert 'set(CMAKE_HOSTC_STANDARD_COMPUTED_DEFAULT "11")' in compiler_info
    assert 'set(CMAKE_HOSTC_PLATFORM_ID "Linux")' in compiler_info
    assert 'set(CMAKE_HOSTC_ABI_COMPILED TRUE)' in compiler_info
    assert 'set(CMAKE_HOSTC_COMPILER_ABI "ELF")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_INCLUDE_DIRECTORIES "/usr/local/include;/usr/lib/llvm-10/lib/clang/10.0.0/include;/usr/include/x86_64-linux-gnu;/usr/include")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_LIBRARIES "gcc;gcc_s;c;gcc;gcc_s")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_DIRECTORIES "/usr/lib/gcc/x86_64-linux-gnu/9;/usr/lib/x86_64-linux-gnu;/usr/lib64;/lib/x86_64-linux-gnu;/lib64;/usr/lib;/usr/lib/llvm-10/lib;/lib")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_FRAMEWORK_DIRECTORIES "")' in compiler_info
