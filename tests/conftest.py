#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import os
import pytest
import shutil
import subprocess


class CMakeFixture(object):
    def __init__(self, workspace, testing_enabled=True, mingw_enabled=True, generator="Unix Makefiles", compiler_list=None):
        self.workspace = workspace
        self.testing_enabled = testing_enabled
        self.mingw_enabled = mingw_enabled
        self.generator = generator
        self.compiler_list = compiler_list
        self.prepare()

    def execute(self, command):
        if isinstance(command, list):
            command = " ".join(command)
        return subprocess.run(command, capture_output=True, shell=True, encoding="UTF-8")

    def prepare(self, build="build"):
        self.build = os.path.join(self.workspace, build)

        # Remove existing files
        shutil.rmtree(f'{self.workspace}/CMakeLists.txt', ignore_errors=True)
        shutil.rmtree(f'{self.workspace}/cmake', ignore_errors=True)
        shutil.rmtree(f'{self.workspace}/sample', ignore_errors=True)

        # Copy source files to workspace
        shutil.copy2("CMakeLists.txt", f'{self.workspace}/CMakeLists.txt')
        shutil.copytree("cmake", f'{self.workspace}/cmake')
        shutil.copytree("sample", f'{self.workspace}/sample')

        command = [
            f'cmake -S {self.workspace} -B {self.build}',
            f'-G "{self.generator}"',
            f'-DWITH_TEST={self.testing_enabled}',
            f'-DWITH_MINGW={self.mingw_enabled}',
            f'-DCMAKE_HOSTC_COMPILER_LIST="{self.compiler_list}"' if self.compiler_list else ''
        ]
        self.execute(command).check_returncode()

    def cmake(self, name=None):
        command = [f'cmake --build {self.build}', f'--target {name}' if name else '']
        return self.execute(command)

    def ctest(self, args=None):
        command = [f'cmake --build {self.build}', f'--target test', f'-- ARGS="{args}"' if args else '']
        return self.execute(command)

    def gcovr(self):
        return self.execute(f'gcovr --root {self.workspace}')

    def exists(self, path):
        return os.path.exists(os.path.join(self.build, path))

    def read(self, path):
        with open(os.path.join(self.build, path), "r") as f:
            return f.read()


@pytest.fixture
def testing_disabled(request, tmpdir_factory):
    directory = str(tmpdir_factory.mktemp("testing_disabled"))
    def cleanup():
        shutil.rmtree(directory)
    request.addfinalizer(cleanup)
    return CMakeFixture(directory, testing_enabled=False)

@pytest.fixture
def testing_cc(request, tmpdir_factory):
    directory = str(tmpdir_factory.mktemp("workspace"))
    def cleanup():
        shutil.rmtree(directory)
    request.addfinalizer(cleanup)
    return CMakeFixture(directory, testing_enabled=True)

@pytest.fixture
def testing_gcc(request, tmpdir_factory):
    directory = str(tmpdir_factory.mktemp("workspace"))
    def cleanup():
        shutil.rmtree(directory)
    request.addfinalizer(cleanup)
    return CMakeFixture(directory, testing_enabled=True, compiler_list="gcc")

@pytest.fixture
def testing_clang(request, tmpdir_factory):
    directory = str(tmpdir_factory.mktemp("workspace"))
    def cleanup():
        shutil.rmtree(directory)
    request.addfinalizer(cleanup)
    return CMakeFixture(directory, testing_enabled=True, compiler_list="clang")

@pytest.fixture
def testing_mingw(request, tmpdir_factory):
    directory = str(tmpdir_factory.mktemp("workspace"))
    def cleanup():
        shutil.rmtree(directory)
    request.addfinalizer(cleanup)
    return CMakeFixture(directory, testing_enabled=True, compiler_list="i686-w64-mingw32-gcc")
