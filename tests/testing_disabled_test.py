#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

PARAM_MINGW = pytest.mark.parametrize("cross_toolchain", [True, False])
PARAM_GENERATORS = pytest.mark.parametrize("generator", ["Unix Makefiles", "Ninja"])
PARAM_COMPILERS = pytest.mark.parametrize("compiler_list", ["cc", "gcc", "clang", "i686-w64-mingw32-gcc"])

@PARAM_MINGW
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_build_target_works(testing, cross_toolchain, generator, compiler_list):
    testing.configure(testing_enabled=False, cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list).check_returncode()
    testing.cmake("all").check_returncode()

@PARAM_MINGW
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_build_compiler_info_available(testing, cross_toolchain, generator, compiler_list):
    testing.configure(testing_enabled=False, cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list).check_returncode()
    assert testing.exists("CMakeFiles/3.16.3/CMakeCCompiler.cmake")

@PARAM_MINGW
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_test_targets_not_available(testing, cross_toolchain, generator, compiler_list):
    testing.configure(testing_enabled=False, cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("host-targets").check_returncode()
    assert "No test configuration file found!" in testing.ctest().stderr

@PARAM_MINGW
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_test_compiler_info_available(testing, cross_toolchain, generator, compiler_list):
    testing.configure(testing_enabled=False, cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    assert testing.exists("CMakeFiles/3.16.3-hosta.internal/CMakeHOSTCCompiler.cmake")
