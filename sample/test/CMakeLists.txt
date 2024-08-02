# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

add_host_executable(unity_test
  SOURCES ../src/calc.c unity_test_main.c
  INCLUDE_DIRECTORIES PRIVATE ../src
  COMPILE_OPTIONS PRIVATE -ftest-coverage -fprofile-arcs -O0 -g
  LINK_OPTIONS PRIVATE -fprofile-arcs
  LINK_LIBRARIES PRIVATE Host::unity
)

add_host_test(Host::unity_test)

add_host_executable(unity_fixture_test
  SOURCES ../src/calc.c unity_fixture_test_main.c
  INCLUDE_DIRECTORIES PRIVATE ../src
  COMPILE_OPTIONS PRIVATE -ftest-coverage -fprofile-arcs -O0 -g
  LINK_OPTIONS PRIVATE -fprofile-arcs
  LINK_LIBRARIES PRIVATE Host::unity Host::unity-fixture
)

unity_fixture_add_host_tests(Host::unity_fixture_test)
