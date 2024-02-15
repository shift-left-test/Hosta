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
  execute_process(COMMAND ${CMAKE_HOSTC_COMPILER} -E ${CMAKE_ROOT}/Modules/CMakeCompilerABI.h
    RESULT_VARIABLE __CMAKE_HOSTC_COMPILER_ABI_STATUS
    OUTPUT_VARIABLE __CMAKE_HOSTC_COMPILER_ABI_OUTPUT
    ERROR_QUIET
  )
  if(__CMAKE_HOSTC_COMPILER_ABI_STATUS EQUAL 0)
    message(STATUS "Detecting HOSTC compiler ABI info - done")

    string(REGEX MATCHALL "INFO:[A-Za-z0-9_]+\\[[^]]*\\]" ABI_STRINGS "${__CMAKE_HOSTC_COMPILER_ABI_OUTPUT}")
    foreach(info ${ABI_STRINGS})
      if("${info}" MATCHES "INFO:abi\\[\" \"([^]]*)\" \"\\]")
        set(CMAKE_HOSTC_COMPILER_ABI "${CMAKE_MATCH_1}")
        break()
      endif()
    endforeach()
  endif()

endif()

unset(__CMAKE_HOSTC_COMPILER_WORKS_STATUS)
unset(__CMAKE_HOSTC_COMPILER_WORKS_OUTPUT)
unset(__CMAKE_HOSTC_COMPILER_ABI_STATUS)
unset(__CMAKE_HOSTC_COMPILER_ABI_OUTPUT)
