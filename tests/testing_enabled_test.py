#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

PARAM_MINGW = pytest.mark.parametrize("mingw_enabled", [True, False])
PARAM_GENERATORS = pytest.mark.parametrize("generator", ["Unix Makefiles", "Ninja"])
PARAM_COMPILERS = pytest.mark.parametrize("compiler_list", ["cc", "gcc", "clang", "i686-w64-mingw32-gcc"])

@PARAM_MINGW
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_build_target_works(testing, mingw_enabled, generator, compiler_list):
    testing.prepare(mingw_enabled=mingw_enabled, generator=generator, compiler_list=compiler_list)
    testing.cmake("all").check_returncode()

@PARAM_MINGW
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_test_targets_work(testing, mingw_enabled, generator, compiler_list):
    testing.prepare(mingw_enabled=mingw_enabled, generator=generator, compiler_list=compiler_list)
    testing.cmake("build-test").check_returncode()
    if compiler_list not in ["i686-w64-mingw32-gcc"]:
        testing.ctest().check_returncode()

@PARAM_MINGW
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_test_targets_work(testing, mingw_enabled, generator, compiler_list):
    testing.prepare(mingw_enabled=mingw_enabled, generator=generator, compiler_list=compiler_list)
    testing.cmake("build-test").check_returncode()
    assert testing.exists("sample/CMakeFiles/unittest.dir/src/calc.c.o")
    assert testing.exists("sample/CMakeFiles/unittest.dir/test/test_main.c.o")

@PARAM_MINGW
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_link_works(testing, mingw_enabled, generator, compiler_list):
    testing.prepare(mingw_enabled=mingw_enabled, generator=generator, compiler_list=compiler_list)
    testing.cmake("build-test").check_returncode()
    assert testing.exists("sample/unittest.out")

@PARAM_MINGW
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_no_output_interference(testing, mingw_enabled, generator, compiler_list):
    testing.prepare(build="", mingw_enabled=mingw_enabled, generator=generator, compiler_list=compiler_list)
    testing.cmake("build-test").check_returncode()
    testing.prepare(build="temp", mingw_enabled=mingw_enabled, generator=generator, compiler_list=compiler_list)
    testing.cmake("build-test").check_returncode()

@PARAM_MINGW
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_ctest_works(testing, mingw_enabled, generator, compiler_list):
    testing.prepare(mingw_enabled=mingw_enabled, generator=generator, compiler_list=compiler_list)
    testing.cmake("build-test")
    if compiler_list not in ["i686-w64-mingw32-gcc"]:
        assert "unittest .........................   Passed" in testing.ctest().stdout

@PARAM_MINGW
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_gcovr_works(testing, mingw_enabled, generator, compiler_list):
    testing.prepare(mingw_enabled=mingw_enabled, generator=generator, compiler_list=compiler_list)
    testing.cmake("build-test")
    if compiler_list not in ["clang", "i686-w64-mingw32-gcc"]:
        testing.ctest()
        assert "sample/test/test_main.c                       15      15   100%" in testing.gcovr().stdout

@PARAM_MINGW
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_no_changes_no_rebuilds(testing, mingw_enabled, generator, compiler_list):
    testing.prepare(mingw_enabled=mingw_enabled, generator=generator, compiler_list=compiler_list)
    testing.cmake("build-test").stdout
    assert "Linking HOSTC executable unittest.out" not in testing.cmake("build-test").stdout

@PARAM_MINGW
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_updating_source_file_rebuilds(testing, mingw_enabled, generator, compiler_list):
    testing.prepare(mingw_enabled=mingw_enabled, generator=generator, compiler_list=compiler_list)
    testing.cmake("build-test").stdout
    testing.touch("sample/src/calc.c")
    assert "Linking HOSTC executable unittest.out" in testing.cmake("build-test").stdout

@PARAM_MINGW
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_updating_header_file_rebuilds(testing, mingw_enabled, generator, compiler_list):
    testing.prepare(mingw_enabled=mingw_enabled, generator=generator, compiler_list=compiler_list)
    testing.cmake("build-test").stdout
    testing.touch("sample/src/calc.h")
    assert "Linking HOSTC executable unittest.out" in testing.cmake("build-test").stdout
