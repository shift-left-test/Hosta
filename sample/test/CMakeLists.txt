# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

add_host_library(coverage INTERFACE
  COMPILE_OPTIONS PUBLIC -ftest-coverage -fprofile-arcs -O0 -g
  LINK_OPTIONS PUBLIC -fprofile-arcs
)

add_host_executable(unity_test
  SOURCES ../calculator/calc.c unity_test_main.c
  INCLUDE_DIRECTORIES PRIVATE ../calculator
  LINK_LIBRARIES PRIVATE Host::unity Host::fff Host::coverage
)

add_host_test(Host::unity_test)

add_host_executable(unity_fixture_test
  SOURCES ../calculator/calc.c unity_fixture_test_main.c
  INCLUDE_DIRECTORIES PRIVATE ../calculator
  LINK_LIBRARIES PRIVATE Host::unity-fixture Host::unity Host::fff Host::coverage
)

unity_fixture_add_host_tests(Host::unity_fixture_test)

add_host_executable(google_test
  SOURCES ../calculator/calc.c googletest_main.cpp
  INCLUDE_DIRECTORIES PRIVATE ../calculator
  LINK_LIBRARIES PRIVATE Host::gtest Host::coverage
)

gtest_add_host_tests(Host::google_test)
