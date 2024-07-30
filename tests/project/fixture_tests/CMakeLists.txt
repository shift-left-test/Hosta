add_host_executable(no_unity_fixture_test
  SOURCES ../src/calc.c ../test/unity_test_main.c
  INCLUDE_DIRECTORIES ../src
  COMPILE_OPTIONS ${HOST_COMPILE_OPTIONS}
  LINK_OPTIONS ${HOST_LINK_OPTIONS}
  LINK_LIBRARIES Host::unity
)

unity_fixture_add_host_tests(no_unity_fixture_test)

add_host_executable(unity_fixture_test
  SOURCES ../src/calc.c ../test/unity_fixture_test_main.c
  INCLUDE_DIRECTORIES ../src
  COMPILE_OPTIONS ${HOST_COMPILE_OPTIONS}
  LINK_OPTIONS ${HOST_LINK_OPTIONS}
  LINK_LIBRARIES Host::unity Host::unity-fixture
)

unity_fixture_add_host_tests(unity_fixture_test)
