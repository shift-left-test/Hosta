#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

PARAM_CROSS_TOOLCHAIN = pytest.mark.parametrize("cross_toolchain", [True, False])
PARAM_GENERATORS = pytest.mark.parametrize("generator", ["Unix Makefiles", "Ninja"])
PARAM_COMPILERS = pytest.mark.parametrize("compiler_list", ["cc", "gcc", "clang", "i686-w64-mingw32-gcc"])
PARAM_STANDARD = pytest.mark.parametrize("standard", [None, "11", "invalid"])
PARAM_EXTENSIONS = pytest.mark.parametrize("extensions", [True, False])

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_build_target_works(testing, cross_toolchain, generator, compiler_list):
    testing.prepare(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("all").check_returncode()

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_test_targets_work(testing, cross_toolchain, generator, compiler_list):
    testing.prepare(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("build-test").check_returncode()
    if compiler_list not in ["i686-w64-mingw32-gcc"]:
        testing.ctest().check_returncode()

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_test_targets_work(testing, cross_toolchain, generator, compiler_list):
    testing.prepare(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("build-test").check_returncode()
    assert testing.exists("sample/CMakeFiles/unittest.dir/src/calc.c.o")
    assert testing.exists("sample/CMakeFiles/unittest.dir/test/test_main.c.o")

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_link_works(testing, cross_toolchain, generator, compiler_list):
    testing.prepare(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("build-test").check_returncode()
    assert testing.exists("sample/unittest.out")

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_no_output_interference(testing, cross_toolchain, generator, compiler_list):
    testing.prepare(build="", cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("build-test").check_returncode()
    testing.prepare(build="temp", cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("build-test").check_returncode()

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_ctest_works(testing, cross_toolchain, generator, compiler_list):
    testing.prepare(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("build-test")
    if compiler_list not in ["i686-w64-mingw32-gcc"]:
        assert "unittest .........................   Passed" in testing.ctest().stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_gcovr_works(testing, cross_toolchain, generator, compiler_list):
    testing.prepare(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("build-test")
    if compiler_list not in ["clang", "i686-w64-mingw32-gcc"]:
        testing.ctest()
        assert "sample/test/test_main.c                       15      15   100%" in testing.gcovr().stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_no_changes_no_rebuilds(testing, cross_toolchain, generator, compiler_list):
    testing.prepare(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("build-test")
    assert "Linking HOSTC executable unittest.out" not in testing.cmake("build-test").stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_no_configuration_changes_no_rebuilds(testing, cross_toolchain, generator, compiler_list):
    testing.prepare(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("build-test")
    testing.prepare(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    assert "Linking HOSTC executable unittest.out" not in testing.cmake("build-test").stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_reconfiguration_rebuilds(testing, cross_toolchain, generator, compiler_list):
    testing.prepare(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list, debug_enabled=True)
    testing.cmake("build-test")
    testing.prepare(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list, debug_enabled=False)
    assert "Linking HOSTC executable unittest.out" in testing.cmake("build-test").stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_updating_source_file_rebuilds(testing, cross_toolchain, generator, compiler_list):
    testing.prepare(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("build-test")
    testing.touch("sample/src/calc.c")
    assert "Linking HOSTC executable unittest.out" in testing.cmake("build-test").stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_updating_header_file_rebuilds(testing, cross_toolchain, generator, compiler_list):
    testing.prepare(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("build-test")
    testing.touch("sample/src/calc.h")
    assert "Linking HOSTC executable unittest.out" in testing.cmake("build-test").stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def testing_no_standard_option(testing, cross_toolchain, generator, compiler_list):
    testing.prepare(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list, standard=None)
    assert '-std=' not in testing.cmake("build-test", verbose=True).stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def testing_standard_option(testing, cross_toolchain, generator, compiler_list):
    testing.prepare(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list, standard="11")
    assert '-std=gnu11' in testing.cmake("build-test", verbose=True).stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def testing_invalid_standard_option(testing, cross_toolchain, generator, compiler_list):
    stderr = testing.prepare(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list, standard="12345").stderr
    assert "HOSTC_STANDARD is set to invalid value '12345'" in stderr

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def testing_standard_and_extension_options(testing, cross_toolchain, generator, compiler_list):
    testing.prepare(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list, standard="11", extensions=True)
    assert '-std=gnu11' in testing.cmake("build-test", verbose=True).stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def testing_standard_and_no_extension_options(testing, cross_toolchain, generator, compiler_list):
    testing.prepare(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list, standard="11", extensions=False)
    assert '-std=c11' in testing.cmake("build-test", verbose=True).stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def testing_depends_option(testing, cross_toolchain, generator, compiler_list):
    testing.prepare(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    assert "hello" in testing.cmake("build-test").stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def testing_paths(testing, cross_toolchain, generator, compiler_list):
    testing.prepare(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    stdout = testing.cmake("build-test", verbose=True).stdout
    assert '-o CMakeFiles/unittest.dir/unity/unity.c.o' in stdout  # absolute source path
    assert './unity' not in stdout  # relative include path
    assert testing.exists("sample/test2/CMakeFiles/unittest2.dir/__/src/calc.c.o")  # .. to __
