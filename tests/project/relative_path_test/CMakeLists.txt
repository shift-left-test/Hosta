add_host_executable(relative_path_test
  SOURCES ../calculator/calc.c ../test/unity_test_main.c
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_LIST_DIR}/../calculator
  LINK_LIBRARIES PRIVATE Host::unity Host::coverage Host::hostc_options
)

add_host_test(relative_path_test)
