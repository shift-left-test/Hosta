# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

include_guard(GLOBAL)

# Set the directory of the current file
if(NOT _HOSTA_BASE_DIR)
  set(_HOSTA_BASE_DIR "${CMAKE_CURRENT_LIST_DIR}")
endif()

include(CMakeParseArguments)
include(${_HOSTA_BASE_DIR}/DetermineHOSTCCompiler.cmake)
include(${_HOSTA_BASE_DIR}/HostBuild.cmake)

function(add_host_test TARGET)
  # Assume that enable_testing() is called
  if(NOT CMAKE_TESTING_ENABLED)
    return()
  endif()

  set(multiValueArgs EXTRA_ARGS)
  cmake_parse_arguments(ARG "" "" "${multiValueArgs}" ${ARGN})

  # Remove the host namespace prefix if exists
  string(REGEX REPLACE "^${CMAKE_HOST_NAMESPACE_PREFIX}(.*)" "\\1" TARGET "${TARGET}")

  get_host_target_properties(${CMAKE_HOST_NAMESPACE_PREFIX}${TARGET} TARGET_FILE _output)

  add_test(NAME ${TARGET} COMMAND ${_output} ${ARG_EXTRA_ARGS})
endfunction(add_host_test)

function(unity_fixture_add_host_tests TARGET)
  # Assume that enable_testing() is called
  if(NOT CMAKE_TESTING_ENABLED)
    return()
  endif()

  set(multiValueArgs EXTRA_ARGS)
  cmake_parse_arguments(ARG "" "" "${multiValueArgs}" ${ARGN})

  # Remove the host namespace prefix if exists
  string(REGEX REPLACE "^${CMAKE_HOST_NAMESPACE_PREFIX}(.*)" "\\1" TARGET "${TARGET}")

  get_host_target_properties(${CMAKE_HOST_NAMESPACE_PREFIX}${TARGET}
    TARGET_FILE _output
    SOURCES _sources
    SOURCE_DIR _source_dir
  )

  # Convert relative source paths to absolute ones
  unset(sources)
  foreach(source IN LISTS _sources)
    if(IS_ABSOLUTE "${source}")
      list(APPEND sources "${source}")
    else()
      list(APPEND sources "${_source_dir}/${source}")
    endif()
  endforeach()

  # Add tests with CTest by scanning source code for Unity test macros
  set(unity_test_name_regex ".*\\([ \r\n\t]*([A-Za-z_0-9]+)[ \r\n\t]*,[ \r\n\t]*([A-Za-z_0-9]+)[ \r\n\t]*\\).*")
  set(unity_test_type_regex "([^A-Za-z_0-9](IGNORE_)?TEST)")

  foreach(source IN LISTS sources)
    file(READ "${source}" contents)
    string(REGEX MATCHALL "${unity_test_type_regex}[ \r\n\t]*\\(([A-Za-z_0-9 ,\r\n\t]+)\\)" found_tests "${contents}")
    foreach(hit ${found_tests})
      string(STRIP ${hit} hit)
      string(REGEX REPLACE ${unity_test_name_regex} "\\1.\\2" unity_test_name ${hit})
      string(REGEX REPLACE ${unity_test_name_regex} "\\1" unity_test_group ${hit})
      string(REGEX REPLACE ${unity_test_name_regex} "\\2" unity_test_case ${hit})

      set(ctest_test_name ${TARGET}.${unity_test_name})
      add_test(NAME ${ctest_test_name} COMMAND ${_output} -g ${unity_test_group} -n ${unity_test_case} -v ${ARG_EXTRA_ARGS})

      # Make sure ignored unity tests get disabled in CTest
      if(hit MATCHES "(^|\\.)IGNORE_")
        set_tests_properties(${ctest_test_name} PROPERTIES DISABLED TRUE)
      else()
        set_tests_properties(${ctest_test_name} PROPERTIES SKIP_REGULAR_EXPRESSION "0 Tests")
      endif()
    endforeach()
  endforeach()
endfunction(unity_fixture_add_host_tests)
