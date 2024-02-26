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

@pytest.fixture
def cmake_fixture(request, tmpdir_factory):
    directory = str(tmpdir_factory.mktemp("build"))
    def cleanup():
        shutil.rmtree(directory)
    request.addfinalizer(cleanup)
    def _build_dir(testing_enabled=True, generator="Unix Makefiles"):
        WITH_TEST="ON" if testing_enabled else "OFF"
        execute(f'cmake -S . -B {directory} -DWITH_TEST={WITH_TEST} -G "{generator}"').check_returncode()
        return directory
    return _build_dir

def test_disabled(cmake_fixture):
    directory = cmake_fixture(testing_enabled=False)
    assert "make: *** No rule to make target 'build-test'" in execute(f"cmake --build {directory} --target build-test").stderr
    assert "make: *** No rule to make target 'test'" in execute(f"cmake --build {directory} --target test").stderr
    assert not os.path.exists(f"{directory}/CMakeFiles/3.16.3/CMakeHOSTCCompiler.cmake")

def test_build_test_target(cmake_fixture):
    directory = cmake_fixture()
    execute(f"cmake --build {directory} --target build-test").check_returncode()

def test_ctest(cmake_fixture):
    directory = cmake_fixture()
    execute(f"cmake --build {directory} --target build-test")
    assert "unittest_unittest ................   Passed" in execute(f"cmake --build {directory} --target test").stdout

def test_gcovr(cmake_fixture):
    directory = cmake_fixture()
    execute(f"cmake --build {directory} --target build-test")
    execute(f"cmake --build {directory} --target test").check_returncode()
    assert "sample/test/test_main.c                       15      15   100%" in execute(f"gcovr .").stdout

def test_compiler_info(cmake_fixture):
    directory = cmake_fixture()
    with open(f"{directory}/CMakeFiles/3.16.3/CMakeHOSTCCompiler.cmake", "r") as f:
        compiler_info = f.read()
        assert 'set(CMAKE_HOSTC_COMPILER "/usr/bin/cc")' in compiler_info
        assert 'set(CMAKE_HOSTC_COMPILER_WORKS TRUE)' in compiler_info
        assert 'set(CMAKE_HOSTC_ABI_COMPILED TRUE)' in compiler_info
        assert 'set(CMAKE_HOSTC_COMPILER_ABI "ELF")' in compiler_info
        assert 'set(CMAKE_HOSTC_IMPLICIT_INCLUDE_DIRECTORIES "/usr/lib/gcc/x86_64-linux-gnu/9/include;/usr/local/include;/usr/include/x86_64-linux-gnu;/usr/include")' in compiler_info
        assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_LIBRARIES "gcc;gcc_s;c;gcc;gcc_s")' in compiler_info
        assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_DIRECTORIES "/usr/lib/gcc/x86_64-linux-gnu/9;/usr/lib/x86_64-linux-gnu;/usr/lib;/lib/x86_64-linux-gnu;/lib")' in compiler_info
        assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_FRAMEWORK_DIRECTORIES "")' in compiler_info
