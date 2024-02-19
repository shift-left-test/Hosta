# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

include(CMakeTestCompilerCommon)

# Test if the host compiler can compile the most basic of programs.
# If not, a fatal error is set and stops processing commands.
if(NOT CMAKE_HOSTC_COMPILER_WORKS)
  PrintTestCompilerStatus("HOSTC" "")

  file(REMOVE ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeTmp/testHOSTCCompiler)
  file(WRITE ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeTmp/testHOSTCCompiler.c
    "#ifdef __cplusplus\n"
    "# error \"The CMAKE_HOSTC_COMPILER is set to a C++ compiler\"\n"
    "#endif\n"
    "#if defined(__CLASSIC_C__)\n"
    "int main(argc, argv)\n"
    "  int argc;\n"
    "  char* argv[];\n"
    "#else\n"
    "int main(int argc, char* argv[])\n"
    "#endif\n"
    "{ (void)argv; return argc-1;}\n"
  )
  execute_process(COMMAND ${CMAKE_HOSTC_COMPILER} -o testHOSTCCompiler testHOSTCCompiler.c
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeTmp
    RESULT_VARIABLE __CMAKE_HOSTC_COMPILER_WORKS_STATUS
    OUTPUT_VARIABLE __CMAKE_HOSTC_COMPILER_WORKS_OUTPUT
    ERROR_QUIET
  )
  if(__CMAKE_HOSTC_COMPILER_WORKS_STATUS EQUAL 0)
    set(CMAKE_HOSTC_COMPILER_WORKS TRUE)
  endif()
endif()

if(NOT CMAKE_HOSTC_COMPILER_WORKS)
  PrintTestCompilerStatus("HOSTC" " -- broken")
  file(APPEND ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeError.log
    "Determining if the HOSTC compiler works failed with "
    "the following output:\n${__CMAKE_HOSTC_COMPILER_WORKS_OUTPUT}\n\n")
  string(REPLACE "\n" "\n  " _output "${__CMAKE_HOSTC_COMPILER_WORKS_OUTPUT}")
  message(FATAL_ERROR "The HOSTC compiler\n  \"${CMAKE_HOSTC_COMPILER}\"\n"
    "is not able to compile a simple test program.\nIt fails "
    "with the following output:\n  ${_output}\n\n"
    "CMake will not be able to correctly generate this project."
  )
else()
  PrintTestCompilerStatus("HOSTC" " -- works")
  file(APPEND ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeOutput.log
    "Determining if the HOSTC compiler works passed with "
    "the following output:\n${__CMAKE_HOSTC_COMPILER_OUTPUT}\n\n")

  # Try to identify the ABI
  set(BIN "${CMAKE_PLATFORM_INFO_DIR}/CMakeDetermineCompilerABI_HOSTC.bin")
  file(REMOVE "${BIN}")
  execute_process(
    COMMAND ${CMAKE_HOSTC_COMPILER} -v -o "${BIN}" ${CMAKE_ROOT}/Modules/CMakeCCompilerABI.c
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeTmp
    RESULT_VARIABLE __CMAKE_HOSTC_COMPILER_ABI_STATUS
    OUTPUT_VARIABLE __CMAKE_HOSTC_COMPILER_ABI_OUTPUT
    ERROR_VARIABLE __CMAKE_HOSTC_COMPILER_ABI_OUTPUT
    ERROR_QUIET
  )
  if(__CMAKE_HOSTC_COMPILER_ABI_STATUS EQUAL 0)
    message(STATUS "Detecting HOSTC compiler ABI info - done")
    file(APPEND ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeOutput.log
      "Detecting HOSTC compiler ABI info compiled with the following output:\n${__CMAKE_HOSTC_COMPILER_ABI_OUTPUT}\n\n")

    file(STRINGS "${BIN}" ABI_STRINGS REGEX "INFO:[A-Za-z0-9_]+\\[[^]]*\\]")
    foreach(info ${ABI_STRINGS})
      if("${info}" MATCHES "INFO:abi\\[([^]]*)\\]")
        set(CMAKE_HOSTC_COMPILER_ABI "${CMAKE_MATCH_1}")
        break()
      endif()
    endforeach()

    # Parse implicit include directories
    include(CMakeParseImplicitIncludeInfo)
    set(implicit_incdirs "")
    cmake_parse_implicit_include_info("${__CMAKE_HOSTC_COMPILER_ABI_OUTPUT}" HOSTC implicit_incdirs log rv)
    file(APPEND ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeOutput.log
      "Parsed HOSTC implicit include dir info from above output: rv=${rv}\n${log}\n\n")
    set(CMAKE_HOSTC_IMPLICIT_INCLUDE_DIRECTORIES "${implicit_incdirs}")

    # Parse implicit linker information
    include(CMakeParseImplicitLinkInfo)
    set(implicit_libs "")
    set(implicit_dirs "")
    set(implicit_fwks "")
    CMAKE_PARSE_IMPLICIT_LINK_INFO("${__CMAKE_HOSTC_COMPILER_ABI_OUTPUT}" implicit_libs implicit_dirs implict_fwks log
      "${CMAKE_HOSTC_IMPLICIT_OBJECT_REGEX}")
    file(APPEND ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeOutput.log
      "Parsed HOSTC implicit link information from above output:\n${log}\n\n")
    set(CMAKE_HOSTC_IMPLICIT_LINK_LIBRARIES "${implicit_libs}")
    set(CMAKE_HOSTC_IMPLICIT_LINK_DIRECTORIES "${implicit_dirs}")
    set(CMAKE_HOSTC_IMPLICIT_FRAMEWORK_DIRECTORIES "${implicit_fwks}")

  else()
    message(STATUS "Detecting HOSTC compiler ABI info - failed")
    file(APPEND ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}CMakeError.log
      "Detecting HOSTC compiler ABI info failed to compile with the following output:\n${__CMAKE_HOSTC_COMPILER_ABI_OUTPUT}\n\n")
  endif()

endif()

unset(__CMAKE_HOSTC_COMPILER_WORKS_STATUS)
unset(__CMAKE_HOSTC_COMPILER_WORKS_OUTPUT)
unset(__CMAKE_HOSTC_COMPILER_ABI_STATUS)
unset(__CMAKE_HOSTC_COMPILER_ABI_OUTPUT)
