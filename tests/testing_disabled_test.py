#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

def test_build_target_works(testing_disabled):
    testing_disabled.cmake("all").check_returncode()

def test_build_compiler_info_available(testing_disabled):
    assert testing_disabled.exists("CMakeFiles/3.16.3/CMakeCCompiler.cmake")

def test_test_targets_not_available(testing_disabled):
    assert "make: *** No rule to make target 'build-test'" in testing_disabled.cmake("build-test").stderr
    assert "make: *** No rule to make target 'test'" in testing_disabled.ctest().stderr

def test_test_compiler_info_not_available(testing_disabled):
    assert not testing_disabled.exists("CMakeFiles/3.16.3/CMakeHOSTCCompiler.cmake")
