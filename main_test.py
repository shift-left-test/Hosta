#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest
import shutil
import subprocess

def test_ctest(request, tmpdir_factory):
    build_dir = str(tmpdir_factory.mktemp("build"))

    def cleanup():
        shutil.rmtree(build_dir)

    request.addfinalizer(cleanup)

    assert 0 == subprocess.check_call(f"cmake -S . -B {build_dir}", shell=True)
    assert 0 == subprocess.check_call(f"cmake --build {build_dir}", shell=True)
    assert 0 == subprocess.check_call(f"cmake --build {build_dir} --target test", shell=True)
