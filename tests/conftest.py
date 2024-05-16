#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

from pathlib import Path
import os
import pytest
import shutil
import subprocess

class CMakeFixture(object):
    def __init__(self, workspace):
        self.workspace = workspace

    def execute(self, command):
        if isinstance(command, list):
            command = " ".join(command)
        return subprocess.run(command, capture_output=True, shell=True, encoding="UTF-8")

    def prepare(self, build="build", testing_enabled=True, cross_toolchain=True, generator="Unix Makefiles", compiler_list=None, debug_enabled=False, libm_enabled=False, standard=None, extensions=None):
        self.build = os.path.join(self.workspace, build)
        self.testing_enabled = testing_enabled
        self.cross_toolchain = cross_toolchain
        self.generator = generator
        self.compiler_list = compiler_list
        self.debug_enabled = debug_enabled
        self.libm_enabled = libm_enabled
        self.standard = standard
        self.extensions = extensions

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
            f'-DWITH_HOST_TEST={self.testing_enabled}',
            f'-DWITH_CROSS_TOOLCHAIN={self.cross_toolchain}',
            f'-DCMAKE_HOSTC_COMPILER_LIST="{self.compiler_list}"' if self.compiler_list else '',
            f'-DWITH_DEBUG_SYMBOL={self.debug_enabled}',
            f'-DWITH_LIBM={self.libm_enabled}',
            f'-DCMAKE_HOSTC_STANDARD={self.standard}' if self.standard is not None else '',
            f'-DCMAKE_HOSTC_EXTENSIONS={self.extensions}' if self.extensions is not None else '',
        ]
        return self.execute(command)

    def cmake(self, name=None, verbose=False):
        command = [f'cmake --build {self.build}', f'--target {name}' if name else '', f'--verbose' if verbose else '']
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

    def touch(self, path):
        Path(os.path.join(self.workspace, path)).touch()

@pytest.fixture
def testing(request, tmpdir_factory):
    directory = str(tmpdir_factory.mktemp("workspace"))
    def cleanup():
        shutil.rmtree(directory)
    request.addfinalizer(cleanup)
    return CMakeFixture(directory)

@pytest.fixture
def testing_disabled(testing):
    testing.prepare(testing_enabled=False)
    return testing

@pytest.fixture
def testing_cc(testing):
    testing.prepare()
    return testing

@pytest.fixture
def testing_gcc(testing):
    testing.prepare(compiler_list="gcc")
    return testing

@pytest.fixture
def testing_clang(testing):
    testing.prepare(compiler_list="clang")
    return testing

@pytest.fixture
def testing_mingw(testing):
    testing.prepare(compiler_list="i686-w64-mingw32-gcc")
    return testing
