unity_fixture_add_tests(no_unity_fixture_test
  SOURCES ../src/calc.c no_unity_fixture_test.c ${PROJECT_SOURCE_DIR}/sample/unity/unity.c
  INCLUDE_DIRECTORIES ../src ../unity
  COMPILE_OPTIONS ${HOST_COMPILE_OPTIONS} -DUNITY_FIXTURE_NO_EXTRAS=OFF -DUNITY_INCLUDE_DOUBLE=ON
  LINK_OPTIONS ${HOST_LINK_OPTIONS}
)

unity_fixture_add_tests(unity_fixture_test
  SOURCES ../src/calc.c unity_fixture_test.c ${PROJECT_SOURCE_DIR}/sample/unity/unity.c ${PROJECT_SOURCE_DIR}/sample/unity/unity_fixture.c
  INCLUDE_DIRECTORIES ../src ../unity
  COMPILE_OPTIONS ${HOST_COMPILE_OPTIONS} -DUNITY_FIXTURE_NO_EXTRAS=OFF -DUNITY_INCLUDE_DOUBLE=ON
  LINK_OPTIONS ${HOST_LINK_OPTIONS}
)
