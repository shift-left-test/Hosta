#-*- coding: utf-8 -*-

"""
Copyright (c) 2024 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest

content = '''
cmake_minimum_required(VERSION 3.16 FATAL_ERROR)

project(CMakeTest LANGUAGES NONE)

include(cmake/HostBuild.cmake)

find_host_language(OUTPUT "{sources}")

include(CMakePrintHelpers)
cmake_print_variables(OUTPUT)
'''

def test_default_language(testing):
    testing.write("CMakeLists.txt", content.format(sources=""))
    options = [f'-DCMAKE_BINARY_DIR={testing.workspace}']
    assert 'OUTPUT="C"' in testing.configure_internal(options).stdout
