add_host_test(disabled_test
  DISABLED
  SOURCES ../unity_test_main.c ${PROJECT_SOURCE_DIR}/unity/unity.c
  INCLUDE_DIRECTORIES ../unity
)
