# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

if(NOT CMAKE_TESTING_ENABLED)
  return()
endif()

add_host_test(unity_test
  SOURCES ../external/unity/unity.c ../src/calc.c unity_test_main.c
  INCLUDE_DIRECTORIES ../external/unity ../src
  COMPILE_OPTIONS -DUNITY_FIXTURE_NO_EXTRAS -DUNITY_INCLUDE_DOUBLE
)

unity_fixture_add_tests(unity_fixture_test
  SOURCES ../external/unity/unity.c ../external/unity/unity_fixture.c ../src/calc.c unity_fixture_test_main.c
  INCLUDE_DIRECTORIES ../external/unity ../src
  COMPILE_OPTIONS -DUNITY_FIXTURE_NO_EXTRAS -DUNITY_INCLUDE_DOUBLE
)
