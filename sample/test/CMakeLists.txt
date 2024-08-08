# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

add_host_library(coverage INTERFACE
  COMPILE_OPTIONS PUBLIC -ftest-coverage -fprofile-arcs -O0 -g
  LINK_OPTIONS PUBLIC -fprofile-arcs
)

add_host_executable(unity_test
  SOURCES ../src/calc.c unity_test_main.c
  INCLUDE_DIRECTORIES PRIVATE ../src
  LINK_LIBRARIES PRIVATE Host::unity Host::fff Host::coverage
)

add_host_test(Host::unity_test)

add_host_executable(unity_fixture_test
  SOURCES ../src/calc.c unity_fixture_test_main.c
  INCLUDE_DIRECTORIES PRIVATE ../src
  LINK_LIBRARIES PRIVATE Host::unity Host::unity-fixture Host::fff Host::coverage
)

unity_fixture_add_host_tests(Host::unity_fixture_test)
