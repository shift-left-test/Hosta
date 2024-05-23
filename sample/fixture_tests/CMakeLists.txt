if(CMAKE_TESTING_ENABLED)
  do_host_compile(C unity_o
    SOURCE ${PROJECT_SOURCE_DIR}/sample/unity/unity.c
    TARGET unity
    INCLUDE_DIRECTORIES ../unity
    COMPILE_OPTIONS -DUNITY_FIXTURE_NO_EXTRAS=OFF -DUNITY_INCLUDE_DOUBLE=ON
  )

  do_host_compile(C unity_fixture_o
    SOURCE ${PROJECT_SOURCE_DIR}/sample/unity/unity_fixture.c
    TARGET unity
    INCLUDE_DIRECTORIES ../unity
    COMPILE_OPTIONS -DUNITY_FIXTURE_NO_EXTRAS=OFF -DUNITY_INCLUDE_DOUBLE=ON
  )
endif()

unity_fixture_add_tests(no_unity_fixture_test
  SOURCES ../src/calc.c no_unity_fixture_test.c
  OBJECTS "${unity_o}"
  INCLUDE_DIRECTORIES ../src ../unity
  COMPILE_OPTIONS ${HOST_COMPILE_OPTIONS} -DUNITY_FIXTURE_NO_EXTRAS=OFF -DUNITY_INCLUDE_DOUBLE=ON
  LINK_OPTIONS ${HOST_LINK_OPTIONS}
)

unity_fixture_add_tests(unity_fixture_test
  SOURCES ../src/calc.c unity_fixture_test.c
  OBJECTS "${unity_o}" "${unity_fixture_o}"
  INCLUDE_DIRECTORIES ../src ../unity
  COMPILE_OPTIONS ${HOST_COMPILE_OPTIONS} -DUNITY_FIXTURE_NO_EXTRAS=OFF -DUNITY_INCLUDE_DOUBLE=ON
  LINK_OPTIONS ${HOST_LINK_OPTIONS}
)
