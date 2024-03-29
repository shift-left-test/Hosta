#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

def test_host_compiler_info(testing_mingw):
    compiler_info = testing_mingw.read("CMakeFiles/3.16.3/CMakeHOSTCCompiler.cmake")
    assert 'set(CMAKE_HOSTC_COMPILER "/usr/bin/i686-w64-mingw32-gcc")' in compiler_info
    assert 'set(CMAKE_HOSTC_COMPILER_ID "GNU")' in compiler_info
    assert 'set(CMAKE_HOSTC_COMPILER_VERSION "9.3.0")' in compiler_info
    assert 'set(CMAKE_HOSTC_COMPILER_WORKS TRUE)' in compiler_info
    assert 'set(CMAKE_HOSTC_STANDARD_COMPUTED_DEFAULT "11")' in compiler_info
    assert 'set(CMAKE_HOSTC_PLATFORM_ID "MinGW")' in compiler_info
    assert 'set(CMAKE_HOSTC_ABI_COMPILED TRUE)' in compiler_info
    assert 'set(CMAKE_HOSTC_COMPILER_ABI "")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_INCLUDE_DIRECTORIES "/usr/lib/gcc/i686-w64-mingw32/9.3-win32/include;/usr/lib/gcc/i686-w64-mingw32/9.3-win32/include-fixed;/usr/i686-w64-mingw32/include")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_LIBRARIES "mingw32;gcc;moldname;mingwex;advapi32;shell32;user32;kernel32;mingw32;gcc;moldname;mingwex")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_DIRECTORIES "/usr/lib/gcc/i686-w64-mingw32/9.3-win32;/usr/i686-w64-mingw32/lib")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_FRAMEWORK_DIRECTORIES "")' in compiler_info
    assert 'set(CMAKE_HOSTC_VERBOSE_FLAG "-v")' in compiler_info
    assert 'set(CMAKE_INCLUDE_SYSTEM_FLAG_HOSTC "-isystem ")' in compiler_info
    assert 'set(CMAKE_HOSTC11_STANDARD_COMPILE_OPTION "-std=c11")' in compiler_info
    assert 'set(CMAKE_HOSTC11_EXTENSION_COMPILE_OPTION "-std=gnu11")' in compiler_info
