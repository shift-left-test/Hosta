add_host_executable(relative_path_test
  SOURCES ../src/calc.c ../test/unity_test_main.c
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_LIST_DIR}/../src
  COMPILE_OPTIONS PRIVATE ${HOST_COMPILE_OPTIONS}
  LINK_OPTIONS PRIVATE ${HOST_LINK_OPTIONS}
  LINK_LIBRARIES PRIVATE Host::unity Host::coverage
)

add_host_test(relative_path_test)
