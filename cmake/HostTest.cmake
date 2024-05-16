# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

include_guard(GLOBAL)

if(CMAKE_TESTING_ENABLED)
  include(DetermineHOSTCCompiler)
  add_custom_target(build-test)
endif(CMAKE_TESTING_ENABLED)

function(add_host_test TARGET)
  # Assume that enable_testing() is called
  if(CMAKE_TESTING_ENABLED)
    include(CMakeParseArguments)
    include(HostTestUtilities)

    set(options DISABLED)
    set(multiValueArgs SOURCES INCLUDE_DIRECTORIES COMPILE_OPTIONS LINK_OPTIONS DEPENDS)
    cmake_parse_arguments(BUILD "${options}" "" "${multiValueArgs}" ${ARGN})

    if(BUILD_DISABLED)
      return()
    endif()

    # Compile source files
    foreach(_source IN LISTS BUILD_SOURCES)
      do_host_compile(C _output
        SOURCE "${_source}"
        TARGET "${TARGET}"
        INCLUDE_DIRECTORIES "${BUILD_INCLUDE_DIRECTORIES}"
        COMPILE_OPTIONS "${BUILD_COMPILE_OPTIONS}" -ftest-coverage -fprofile-arcs -O0 -g
        DEPENDS "${BUILD_DEPENDS}"
      )
      list(APPEND _objects ${_output})
    endforeach()

    # Link object files
    do_host_link(C ${TARGET} _output
      OBJECTS "${_objects}"
      LINK_OPTIONS "${BUILD_LINK_OPTIONS}" -fprofile-arcs
      DEPENDS "${BUILD_DEPENDS}"
    )

    add_custom_target(${TARGET} DEPENDS ${_output})
    add_dependencies(build-test ${TARGET})
    add_test(NAME ${TARGET} COMMAND ${_output})

  endif(CMAKE_TESTING_ENABLED)
endfunction(add_host_test)
