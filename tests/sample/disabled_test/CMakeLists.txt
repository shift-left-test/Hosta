add_host_test(disabled_test
  DISABLED
  SOURCES ../unity_test_main.c ${PROJECT_SOURCE_DIR}/sample/unity/unity.c
  INCLUDE_DIRECTORIES ../unity
)
