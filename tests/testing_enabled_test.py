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
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("all").check_returncode()

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_test_targets_work(testing, cross_toolchain, generator, compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("host-targets").check_returncode()
    suffix = '.obj' if compiler_list in ["i686-w64-mingw32-gcc"] else '.o'
    assert testing.exists(f"CMakeFiles/HOST-unittest.dir/src/calc.c{suffix}")
    assert testing.exists(f"CMakeFiles/HOST-unittest.dir/test/unity_test_main.c{suffix}")
    if compiler_list not in ["i686-w64-mingw32-gcc"]:
        testing.ctest().check_returncode()

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_link_works(testing, cross_toolchain, generator, compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("host-targets").check_returncode()
    assert testing.exists("unittest") or testing.exists("unittest.exe")

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_no_output_interference(testing, cross_toolchain, generator, compiler_list):
    testing.configure(build="first", cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("host-targets").check_returncode()
    testing.configure(build="second", cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("host-targets").check_returncode()

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_ctest_works(testing, cross_toolchain, generator, compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("host-targets")
    if compiler_list not in ["i686-w64-mingw32-gcc"]:
        assert "unittest .......................................   Passed" in testing.ctest().stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_gcovr_works(testing, cross_toolchain, generator, compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("host-targets")
    if compiler_list not in ["clang", "i686-w64-mingw32-gcc"]:
        testing.ctest()
        assert "src/calc.c                                     8       8   100%" in testing.gcovr().stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_no_changes_no_rebuilds(testing, cross_toolchain, generator, compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("host-targets")
    assert "Linking HOSTC executable unittest" not in testing.cmake("host-targets").stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_no_configuration_changes_no_rebuilds(testing, cross_toolchain, generator, compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("host-targets")
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    assert "Linking HOSTC executable unittest" not in testing.cmake("host-targets").stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_reconfiguration_rebuilds(testing, cross_toolchain, generator, compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list, debug_enabled=True)
    testing.cmake("host-targets")
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list, debug_enabled=False)
    assert "Linking HOSTC executable unittest" in testing.cmake("host-targets").stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_updating_source_file_rebuilds(testing, cross_toolchain, generator, compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("host-targets")
    testing.touch("src/calc.c")
    assert "Linking HOSTC executable unittest" in testing.cmake("host-targets").stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_updating_header_file_rebuilds(testing, cross_toolchain, generator, compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("host-targets")
    testing.touch("src/calc.h")
    assert "Linking HOSTC executable unittest" in testing.cmake("host-targets").stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_no_standard_option(testing, cross_toolchain, generator, compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list, standard=None)
    assert '-std=' not in testing.cmake("host-targets", verbose=True).stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_standard_option(testing, cross_toolchain, generator, compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list, standard="11")
    assert '-std=gnu11' in testing.cmake("host-targets", verbose=True).stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_invalid_standard_option(testing, cross_toolchain, generator, compiler_list):
    stderr = testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list, standard="12345").stderr
    assert "HOSTC_STANDARD is set to invalid value '12345'" in stderr

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_standard_and_extension_options(testing, cross_toolchain, generator, compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list, standard="11", extensions=True)
    assert '-std=gnu11' in testing.cmake("host-targets", verbose=True).stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_standard_and_no_extension_options(testing, cross_toolchain, generator, compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list, standard="11", extensions=False)
    assert '-std=c11' in testing.cmake("host-targets", verbose=True).stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_depends_option(testing, cross_toolchain, generator, compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    assert "hello" in testing.cmake("host-targets").stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_paths(testing, cross_toolchain, generator, compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    stdout = testing.cmake("host-targets", verbose=True).stdout
    if compiler_list in ["i686-w64-mingw32-gcc"]:
        static_library_prefix = ""
        static_library_suffix = ".lib"
        object_extension = ".obj"
    else:
        static_library_prefix = "lib"
        static_library_suffix = ".a"
        object_extension = ".o"

    assert f'-o CMakeFiles/HOST-{static_library_prefix}unity{static_library_suffix}.dir/unity.c{object_extension}' in stdout  # absolute source path
    assert f'{testing.workspace}/unity' in stdout  # relative include path to absolute one
    assert testing.exists(f"relative_path_test/CMakeFiles/HOST-relative_path_test.dir/__/src/calc.c{object_extension}")  # .. to __

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_compile_options(testing, cross_toolchain, generator, compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list, debug_enabled=True)
    assert ' -g' in testing.cmake("host-targets", verbose=True).stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_link_options(testing, cross_toolchain, generator, compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list, libm_enabled=True)
    assert ' -lm' in testing.cmake("host-targets", verbose=True).stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_custom_build_target_conflict_existing_name(testing, cross_toolchain, generator, compiler_list):
    stderr = testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list, extra_options=["-DCMAKE_HOST_BUILD_TARGET=all"]).stderr
    assert 'The target name "all" is reserved' in stderr

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_custom_build_target(testing, cross_toolchain, generator, compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list, extra_options=["-DCMAKE_HOST_BUILD_TARGET=abc"])
    testing.cmake("abc").check_returncode()
    assert testing.exists("unittest") or testing.exists("unittest.exe")

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_unity_fixture_add_host_tests_with_unity_fixture_framework(testing, cross_toolchain, generator, compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("host-targets").check_returncode()
    if compiler_list not in ["i686-w64-mingw32-gcc"]:
        stdout = testing.ctest().stdout
        assert 'no_unity_fixture_test' not in stdout
        assert 'unity_fixture_test.FirstGroup.test_plus' in stdout
        assert 'unity_fixture_test.FirstGroup.test_minus' in stdout
        assert 'unity_fixture_test.SecondGroup.test_multiply' in stdout
        assert 'unity_fixture_test.SecondGroup.test_divide' in stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_unity_fixture_add_host_tests_with_ignored_test(testing, cross_toolchain, generator, compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("host-targets").check_returncode()
    if compiler_list not in ["i686-w64-mingw32-gcc"]:
        assert 'unity_fixture_test.FirstGroup.test_minus .......***Not Run (Disabled)' in testing.ctest().stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_unity_fixture_add_host_tests_with_unused_test(testing, cross_toolchain, generator, compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("host-targets").check_returncode()
    if compiler_list not in ["i686-w64-mingw32-gcc"]:
        assert 'unity_fixture_test.SecondGroup.test_divide .....***Skipped' in testing.ctest().stdout

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_host_interface_library(testing, cross_toolchain, generator, compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("HOST-coverage").check_returncode()

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_host_static_library(testing, cross_toolchain, generator, compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("HOST-unity").check_returncode()

@PARAM_CROSS_TOOLCHAIN
@PARAM_GENERATORS
@PARAM_COMPILERS
def test_host_executable(testing, cross_toolchain, generator, compiler_list):
    testing.configure(cross_toolchain=cross_toolchain, generator=generator, compiler_list=compiler_list)
    testing.cmake("HOST-unittest").check_returncode()
