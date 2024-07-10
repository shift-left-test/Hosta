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
    def __init__(self, rootdir, workspace):
        self.rootdir = rootdir
        self.workspace = workspace
        self.build = os.path.join(workspace, "build")

    def execute(self, command):
        if isinstance(command, list):
            command = " ".join(command)
        return subprocess.run(command, capture_output=True, shell=True, encoding="UTF-8")

    def configure_internal(self, options=[]):
        self.copytree("cmake", "cmake")
        command = [f'cmake -S {self.workspace} -B {self.build}']
        return self.execute(command + options)

    def configure(self, build="build", testing_enabled=True, cross_toolchain=True, generator="Unix Makefiles", compiler_list=None, debug_enabled=False, libm_enabled=False, standard=None, extensions=None, extra_options=[]):
        self.build = os.path.join(self.workspace, build)
        self.testing_enabled = testing_enabled
        self.cross_toolchain = cross_toolchain
        self.generator = generator
        self.compiler_list = compiler_list
        self.debug_enabled = debug_enabled
        self.libm_enabled = libm_enabled
        self.standard = standard
        self.extensions = extensions

        # Copy source files to workspace
        self.copytree("tests/project", "")

        options = [
            f'-G "{self.generator}"',
            f'-DWITH_HOST_TEST={self.testing_enabled}',
            f'-DWITH_CROSS_TOOLCHAIN={self.cross_toolchain}',
            f'-DCMAKE_HOSTC_COMPILER_LIST="{self.compiler_list}"' if self.compiler_list else '',
            f'-DWITH_DEBUG_SYMBOL={self.debug_enabled}',
            f'-DWITH_LIBM={self.libm_enabled}',
            f'-DCMAKE_HOSTC_STANDARD={self.standard}' if self.standard is not None else '',
            f'-DCMAKE_HOSTC_EXTENSIONS={self.extensions}' if self.extensions is not None else '',
        ] + extra_options
        return self.configure_internal(options)

    def cmake(self, name=None, verbose=False):
        command = [f'cmake --build {self.build}', f'--target {name}' if name else '', f'--verbose' if verbose else '']
        return self.execute(command)

    def ctest(self, args=None):
        pwd = os.getcwd()
        os.chdir(self.build)
        try:
            command = ['ctest', args if args else '']
            output = self.execute(command)
        finally:
            os.chdir(pwd)
        return output

    def gcovr(self):
        return self.execute(f'gcovr --root {self.workspace}')

    def exists(self, path):
        return os.path.exists(os.path.join(self.build, path))

    def read(self, path):
        with open(os.path.join(self.build, path), "r") as f:
            return f.read()

    def write(self, path, content):
        filePath = os.path.join(self.workspace, path)
        os.makedirs(os.path.dirname(filePath), exist_ok=True)
        with open(filePath, "w") as f:
            if isinstance(content, list):
                f.writelines(content)
            else:
                f.write(content)

    def touch(self, path):
        Path(os.path.join(self.workspace, path)).touch()

    def copy(self, source, destination):
        shutil.copy2(f'{self.root}/{source}', f'{self.workspace}/{destination}')

    def copytree(self, source, destination):
        shutil.copytree(f'{self.rootdir}/{source}', f'{self.workspace}/{destination}', dirs_exist_ok=True)

    def mkdirs(self, path):
        os.makedirs(f'{self.workspace}/{path}', exist_ok=True)

    def rmtree(self, path):

        shutil.rmtree(f'{self.workspace}/{path}', ignore_errors=True)

@pytest.fixture
def testing(request, tmpdir_factory):
    directory = str(tmpdir_factory.mktemp("workspace"))
    def cleanup():
        shutil.rmtree(directory)
    request.addfinalizer(cleanup)
    return CMakeFixture(request.config.rootdir, directory)

@pytest.fixture
def testing_disabled(testing):
    testing.configure(testing_enabled=False)
    return testing

@pytest.fixture
def testing_cc(testing):
    testing.configure()
    return testing

@pytest.fixture
def testing_gcc(testing):
    testing.configure(compiler_list="gcc")
    return testing

@pytest.fixture
def testing_clang(testing):
    testing.configure(compiler_list="clang")
    return testing

@pytest.fixture
def testing_mingw(testing):
    testing.configure(compiler_list="i686-w64-mingw32-gcc")
    return testing
