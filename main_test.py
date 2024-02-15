#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest
import shutil
import subprocess

@pytest.fixture(scope="session")
def build_dir(request, tmpdir_factory):
    directory = str(tmpdir_factory.mktemp("build"))
    def cleanup():
        shutil.rmtree(directory)
    request.addfinalizer(cleanup)
    subprocess.check_call(f"cmake -S . -B {directory}", shell=True)
    subprocess.check_call(f"cmake --build {directory} --target build-test", shell=True)
    return directory

@pytest.fixture(scope="session")
def compiler_info(build_dir):
    with open(f"{build_dir}/CMakeFiles/3.16.3/CMakeHOSTCCompiler.cmake", "r") as f:
        return f.read()


def test_ctest(build_dir):
    output = subprocess.check_output(f"cmake --build {build_dir} --target test", shell=True, encoding="UTF-8")
    assert "unittest_unittest ................   Passed" in output

def test_gcovr(build_dir):
    subprocess.check_call(f"cmake --build {build_dir} --target test", shell=True)
    output = subprocess.check_output(f"gcovr .", shell=True, encoding="UTF-8")
    assert "src/test_main.c                               19      19   100%" in output

def test_compiler_info(compiler_info):
    assert 'set(CMAKE_HOSTC_COMPILER "/usr/bin/cc")' in compiler_info
    assert 'set(CMAKE_HOSTC_COMPILER_WORKS TRUE)' in compiler_info
    assert 'set(CMAKE_HOSTC_COMPILER_ABI "ELF")' in compiler_info
