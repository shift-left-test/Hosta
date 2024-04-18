add_host_test(unittest2
  SOURCES ../src/calc.c test2_main.c ${PROJECT_SOURCE_DIR}/sample/unity/unity.c
  INCLUDE_DIRECTORIES ${CMAKE_CURRENT_LIST_DIR}/../src ../unity
  COMPILE_OPTIONS ${HOST_COMPILE_OPTIONS}
)
