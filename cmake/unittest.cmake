# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

include_guard(GLOBAL)

# Assume that enable_testing() is called
if(CMAKE_TESTING_ENABLED)
  message(STATUS "Unit testing: ENABLED")
  add_custom_target(build-test)
endif(CMAKE_TESTING_ENABLED)

function(add_unittest TARGET)
  # Assume that enable_testing() is called
  if(CMAKE_TESTING_ENABLED)
    include(HostTestUtilities)
    include(CMakeParseArguments)

    set(multiValueArgs SOURCES INCLUDE_DIRECTORIES COMPILE_OPTIONS)
    cmake_parse_arguments(BUILD "" "" "${multiValueArgs}" ${ARGN})

    # Compile source files
    foreach(_source IN LISTS BUILD_SOURCES)
      do_host_compile(C _output
        SOURCE "${_source}"
        TARGET "${TARGET}"
        INCLUDE_DIRECTORIES "${BUILD_INCLUDE_DIRECTORIES}"
        COMPILE_OPTIONS "${BUILD_COMPILE_OPTIONS}" --coverage
      )
      list(APPEND _objects ${_output})
    endforeach()

    # Link object files
    do_host_link(C ${TARGET} _output
      OBJECTS "${_objects}"
      LINK_OPTIONS --coverage
      LINK_LIBRARIES gcov
    )

    add_custom_target(${TARGET} DEPENDS ${_output})
    add_dependencies(build-test ${TARGET})
    add_test(NAME ${TARGET} COMMAND ${_output})

  endif(CMAKE_TESTING_ENABLED)
endfunction(add_unittest)
