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

def test_testing_disabled(request, tmpdir_factory):
    directory = str(tmpdir_factory.mktemp("build"))
    def cleanup():
        shutil.rmtree(directory)
    request.addfinalizer(cleanup)
    execute(f"cmake -S . -B {directory} -DWITH_TEST=OFF").check_returncode()
    assert "make: *** No rule to make target 'build-test'" in execute(f"cmake --build {directory} --target build-test").stderr
    assert "make: *** No rule to make target 'test'" in execute(f"cmake --build {directory} --target test").stderr
    assert not os.path.exists(f"{directory}/CMakeFiles/3.16.3/CMakeHOSTCCompiler.cmake")

@pytest.fixture(scope="session")
def build_dir(request, tmpdir_factory):
    directory = str(tmpdir_factory.mktemp("build"))
    def cleanup():
        shutil.rmtree(directory)
    request.addfinalizer(cleanup)
    execute(f"cmake -S . -B {directory} -DWITH_TEST=ON").check_returncode()
    execute(f"cmake --build {directory} --target build-test").check_returncode()
    return directory

@pytest.fixture(scope="session")
def compiler_info(build_dir):
    with open(f"{build_dir}/CMakeFiles/3.16.3/CMakeHOSTCCompiler.cmake", "r") as f:
        return f.read()

def test_ctest(build_dir):
    assert "unittest_unittest ................   Passed" in execute(f"cmake --build {build_dir} --target test").stdout

def test_gcovr(build_dir):
    execute(f"cmake --build {build_dir} --target test").check_returncode()
    assert "src/test_main.c                               19      19   100%" in execute(f"gcovr .").stdout

def test_compiler_info(compiler_info):
    assert 'set(CMAKE_HOSTC_COMPILER "/usr/bin/cc")' in compiler_info
    assert 'set(CMAKE_HOSTC_COMPILER_WORKS TRUE)' in compiler_info
    assert 'set(CMAKE_HOSTC_ABI_COMPILED TRUE)' in compiler_info
    assert 'set(CMAKE_HOSTC_COMPILER_ABI "ELF")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_INCLUDE_DIRECTORIES "/usr/lib/gcc/x86_64-linux-gnu/9/include;/usr/local/include;/usr/include/x86_64-linux-gnu;/usr/include")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_LIBRARIES "gcc;gcc_s;c;gcc;gcc_s")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_DIRECTORIES "/usr/lib/gcc/x86_64-linux-gnu/9;/usr/lib/x86_64-linux-gnu;/usr/lib;/lib/x86_64-linux-gnu;/lib")' in compiler_info
    assert 'set(CMAKE_HOSTC_IMPLICIT_LINK_FRAMEWORK_DIRECTORIES "")' in compiler_info
