add_host_library(gtest STATIC
  SOURCES gtest-all.cc
  INCLUDE_DIRECTORIES PUBLIC ${CMAKE_CURRENT_LIST_DIR}
  COMPILE_OPTIONS PUBLIC -DGTEST_HAS_PTHREAD=0
)
