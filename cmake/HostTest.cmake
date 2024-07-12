# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

include_guard(GLOBAL)

set(_HOSTA_BASE_DIR "${CMAKE_CURRENT_LIST_DIR}")
if(NOT _HOSTA_BUILD_TARGET)
  set(_HOSTA_BUILD_TARGET build-test)
endif()

if(CMAKE_TESTING_ENABLED)
  include(CMakeParseArguments)
  include(${_HOSTA_BASE_DIR}/DetermineHOSTCCompiler.cmake)
  include(${_HOSTA_BASE_DIR}/HostBuild.cmake)

  add_custom_target(${_HOSTA_BUILD_TARGET})
endif(CMAKE_TESTING_ENABLED)

function(add_host_test TARGET)
  # Assume that enable_testing() is called
  if(CMAKE_TESTING_ENABLED)
    set(options DISABLED)
    set(oneValueArgs PREFIX SUFFIX)
    set(multiValueArgs SOURCES OBJECTS INCLUDE_DIRECTORIES COMPILE_OPTIONS LINK_OPTIONS DEPENDS EXTRA_ARGS)
    cmake_parse_arguments(BUILD "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

    if(BUILD_DISABLED)
      return()
    endif()

    add_host_executable(C ${TARGET} _output
      PREFIX "${BUILD_PREFIX}"
      SUFFIX "${BUILD_SUFFIX}"
      SOURCES "${BUILD_SOURCES}"
      OBJECTS "${BUILD_OBJECTS}"
      INCLUDE_DIRECTORIES "${BUILD_INCLUDE_DIRECTORIES}"
      COMPILE_OPTIONS "${BUILD_COMPILE_OPTIONS}" -ftest-coverage -fprofile-arcs -O0 -g
      LINK_OPTIONS "${BUILD_LINK_OPTIONS}" -fprofile-arcs
      DEPENDS "${BUILD_DEPENDS}"
    )

    add_dependencies(${_HOSTA_BUILD_TARGET} ${TARGET})
    add_test(NAME ${TARGET} COMMAND ${_output} ${BUILD_EXTRA_ARGS})
  endif(CMAKE_TESTING_ENABLED)
endfunction(add_host_test)

function(unity_fixture_add_tests TARGET)
  # Assume that enable_testing() is called
  if(CMAKE_TESTING_ENABLED)
    set(options DISABLED)
    set(oneValueArgs PREFIX SUFFIX)
    set(multiValueArgs SOURCES OBJECTS INCLUDE_DIRECTORIES COMPILE_OPTIONS LINK_OPTIONS DEPENDS EXTRA_ARGS)
    cmake_parse_arguments(BUILD "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

    if(BUILD_DISABLED)
      return()
    endif()

    add_host_executable(C ${TARGET} _output
      PREFIX "${BUILD_PREFIX}"
      SUFFIX "${BUILD_SUFFIX}"
      SOURCES "${BUILD_SOURCES}"
      OBJECTS "${BUILD_OBJECTS}"
      INCLUDE_DIRECTORIES "${BUILD_INCLUDE_DIRECTORIES}"
      COMPILE_OPTIONS "${BUILD_COMPILE_OPTIONS}" -ftest-coverage -fprofile-arcs -O0 -g
      LINK_OPTIONS "${BUILD_LINK_OPTIONS}" -fprofile-arcs
      DEPENDS "${BUILD_DEPENDS}"
    )

    add_dependencies(${_HOSTA_BUILD_TARGET} ${TARGET})

    set(unity_test_name_regex ".*\\([ \r\n\t]*([A-Za-z_0-9]+)[ \r\n\t]*,[ \r\n\t]*([A-Za-z_0-9]+)[ \r\n\t]*\\).*")
    set(unity_test_type_regex "([^A-Za-z_0-9](IGNORE_)?TEST)")

    foreach(source IN LISTS BUILD_SOURCES)
      file(READ "${source}" contents)
      string(REGEX MATCHALL "${unity_test_type_regex}[ \r\n\t]*\\(([A-Za-z_0-9 ,\r\n\t]+)\\)" found_tests "${contents}")
      foreach(hit ${found_tests})
        string(STRIP ${hit} hit)
        string(REGEX REPLACE ${unity_test_name_regex} "\\1.\\2" unity_test_name ${hit})
        string(REGEX REPLACE ${unity_test_name_regex} "\\1" unity_test_group ${hit})
        string(REGEX REPLACE ${unity_test_name_regex} "\\2" unity_test_case ${hit})

        set(ctest_test_name ${TARGET}.${unity_test_name})
        add_test(NAME ${ctest_test_name} COMMAND ${_output} -g ${unity_test_group} -n ${unity_test_case} -v ${BUILD_EXTRA_ARGS})

        # Make sure ignored unity tests get disabled in CTest
        if(hit MATCHES "(^|\\.)IGNORE_")
          set_tests_properties(${ctest_test_name} PROPERTIES DISABLED TRUE)
        else()
          set_tests_properties(${ctest_test_name} PROPERTIES SKIP_REGULAR_EXPRESSION "0 Tests")
        endif()
      endforeach()
    endforeach()
  endif(CMAKE_TESTING_ENABLED)
endfunction(unity_fixture_add_tests)
