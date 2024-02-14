# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

include_guard(GLOBAL)

include(DetermineHOSTCCompiler)
include(CMakeParseArguments)

# FIXME: Use more general condition
if(WITH_TEST)
  message(STATUS "Unit testing: ENABLED")
  add_custom_target(build-test)
endif()

function(convert_to_absolute_paths PATHS)
  foreach(path ${${PATHS}})
    get_filename_component(abs_path ${path} ABSOLUTE)
    list(APPEND ABS_PATHS ${abs_path})
  endforeach()
  set(${PATHS} ${ABS_PATHS} PARENT_SCOPE)
endfunction()

function(add_unittest BUILD_NAME)
  # FIXME: Use more general condition
  if(NOT WITH_TEST)
    return()
  endif()

  set(multiValueArgs SOURCES INCLUDE_DIRECTORIES CFLAGS COMPILE_OPTIONS LIBRARIES)
  cmake_parse_arguments(BUILD "" "" "${multiValueArgs}" ${ARGN})

  set(TEST_NAME unittest_${BUILD_NAME})

  list(TRANSFORM BUILD_INCLUDE_DIRECTORIES PREPEND -I)
  separate_arguments(BUILD_INCLUDE_DIRECTORIES UNIX_COMMAND "${BUILD_INCLUDE_DIRECTORIES}")
  convert_to_absolute_paths(BUILD_SOURCES)
  separate_arguments(BUILD_SOURCES UNIX_COMMAND "${BUILD_SOURCES}")
  separate_arguments(BUILD_CFLAGS UNIX_COMMAND "${BUILD_CFLAGS}")
  separate_arguments(BUILD_COMPILE_OPTIONS UNIX_COMMAND "${BUILD_COMPILE_OPTIONS}")

  # FIXME: find host compiler information properly
  set(COMMAND
    ${CMAKE_HOSTC_COMPILER}
    -o ${CMAKE_CURRENT_BINARY_DIR}/${TEST_NAME}${CMAKE_EXECUTABLE_SUFFIX}
    ${BUILD_SOURCES}
    ${BUILD_INCLUDE_DIRECTORIES}
    ${BUILD_FLAGS}
    ${BUILD_COMPILE_OPTIONS}
    --coverage
    -L/usr/lib/gcc/x86_64-linux-gnu/9/
    -lgcov
  )

  add_custom_target(${TEST_NAME}
    COMMAND ${COMMAND}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Building a unit test executable: ${TEST_NAME}"
    VERBATIM
  )

  add_dependencies(build-test ${TEST_NAME})

  add_test(NAME ${TEST_NAME} COMMAND ${CMAKE_CURRENT_BINARY_DIR}/${TEST_NAME}${CMAKE_EXECUTABLE_SUFFIX})

endfunction(add_unittest)
