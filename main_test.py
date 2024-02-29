#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import os
import pytest
import shutil
import subprocess

def execute(command):
    return subprocess.run(command, capture_output=True, shell=True, encoding="UTF-8")

def read_compiler_info(directory):
    f = open(f"{directory}/CMakeFiles/3.16.3/CMakeHOSTCCompiler.cmake", "r")
    return f.read()

@pytest.fixture
def cmake_fixture(request, tmpdir_factory):
    directory = str(tmpdir_factory.mktemp("build"))
    def cleanup():
        shutil.rmtree(directory)
    request.addfinalizer(cleanup)
    def _execute_fixture(testing_enabled=True, mingw_enabled=True, generator="Unix Makefiles", compiler_list=None):
        command = [
            f'cmake -S . -B {directory}',
            f'-G "{generator}"',
            f'-DWITH_TEST={testing_enabled}',
            f'-DWITH_MINGW={mingw_enabled}',
            f'-DCMAKE_HOSTC_COMPILER_LIST="{compiler_list}"' if compiler_list else '',
        ]
        execute(" ".join(command)).check_returncode()
        return lambda target: execute(f"cmake --build {directory} --target {target}"), directory
    return _execute_fixture

def test_disabled(cmake_fixture):
    run, directory = cmake_fixture(testing_enabled=False)
    assert "make: *** No rule to make target 'build-test'" in run("build-test").stderr
    assert "make: *** No rule to make target 'test'" in run("test").stderr
    assert not os.path.exists(f"{directory}/CMakeFiles/3.16.3/CMakeHOSTCCompiler.cmake")

def test_build_test_target(cmake_fixture):
    run, _ = cmake_fixture()
    run("build-test").check_returncode()

def test_ctest(cmake_fixture):
    run, _ = cmake_fixture()
    run("build-test").check_returncode()
    assert "unittest_unittest ................   Passed" in run("test").stdout

def test_gcovr(cmake_fixture):
    run, _ = cmake_fixture()
    run("build-test").check_returncode()
    run("test").check_returncode()
    assert "sample/test/test_main.c                       15      15   100%" in execute(f"gcovr .").stdout

def test_compiler_info(cmake_fixture):
    _, directory = cmake_fixture()
    compiler_info = read_compiler_info(directory)
    assert 'set(CMAKE_HOSTC_COMPILER "/usr/bin/cc")' in compiler_info
    assert 'set(CMAKE_HOSTC_COMPILER_WORKS TRUE)' in compiler_info
    assert 'set(CMAKE_HOSTC_ABI_COMPILED TRUE)' in compiler_info
    assert 'set(CMAKE_HOSTC_COMPILER_ABI "ELF")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_INCLUDE_DIRECTORIES "/usr/lib/gcc/x86_64-linux-gnu/9/include;/usr/local/include;/usr/include/x86_64-linux-gnu;/usr/include")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_LIBRARIES "gcc;gcc_s;c;gcc;gcc_s")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_DIRECTORIES "/usr/lib/gcc/x86_64-linux-gnu/9;/usr/lib/x86_64-linux-gnu;/usr/lib;/lib/x86_64-linux-gnu;/lib")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_FRAMEWORK_DIRECTORIES "")' in compiler_info

def test_custom_compiler_list(cmake_fixture):
    _, directory = cmake_fixture(compiler_list="clang")
    compiler_info = read_compiler_info(directory)
    assert 'set(CMAKE_HOSTC_COMPILER "/usr/bin/clang")' in compiler_info
