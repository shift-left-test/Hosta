do_host_compile(C unity_o
  SOURCE ${PROJECT_SOURCE_DIR}/unity/unity.c
  TARGET unity
  INCLUDE_DIRECTORIES ../unity
  COMPILE_OPTIONS ${HOST_COMPILE_OPTIONS}
)

do_host_compile(C unity_fixture_o
  SOURCE ${PROJECT_SOURCE_DIR}/unity/unity_fixture.c
  TARGET unity
  INCLUDE_DIRECTORIES ../unity
  COMPILE_OPTIONS ${HOST_COMPILE_OPTIONS}
)

add_host_executable(C no_unity_fixture_test
  SOURCES ../src/calc.c ../test/unity_test_main.c
  OBJECTS "${unity_o}"
  INCLUDE_DIRECTORIES ../src ../unity
  COMPILE_OPTIONS ${HOST_COMPILE_OPTIONS}
  LINK_OPTIONS ${HOST_LINK_OPTIONS}
)

unity_fixture_add_host_tests(no_unity_fixture_test)

add_host_executable(C unity_fixture_test
  SOURCES ../src/calc.c ../test/unity_fixture_test_main.c
  OBJECTS "${unity_o}" "${unity_fixture_o}"
  INCLUDE_DIRECTORIES ../src ../unity
  COMPILE_OPTIONS ${HOST_COMPILE_OPTIONS}
  LINK_OPTIONS ${HOST_LINK_OPTIONS}
)

unity_fixture_add_host_tests(unity_fixture_test)
