# Hosta

> Host based test automation for C

## About

Hosta is a comprehensive solution for building and executing unit tests for C programs using the host build toolchain. It leverages CMake scripts to facilitate the creation of test programs and their execution on the host platform via CTest, even within a cross-build toolchain environment.

## Prerequisites

Ensure the following software packages are installed on your host environment:

- CMake (3.16 or higher)
- C Compiler Toolchain (e.g. GCC, clang)

The following additional packages are required for testing this project:

- build-essential
- docker
- clang
- gcc-mingw-w64
- gcovr
- ninja-build
- pytest3
- pytest3-xdist
- python3

### Docker Setup

To streamline the setup process, you can build a Docker image with the necessary packages using the following commands:

```bash
$ docker build -t host-test-dev .
$ docker run --rm -it -v `pwd`:/test host-test-dev
$ cd /test
```

## Setup Instructions

To integrate Hosta into your project, follow these steps:

Copy the files from the cmake directory to your project's CMake script directory.
Add the following line to your top-level CMakeLists.txt file:

```cmake
include(cmake/HostTest.cmake)
```

## Usage

### Creating an Executable for the Host Platform

To define an executable target for the host platform, use the `add_host_executbale` function:

```cmake
add_host_executable(<target>
  [SOURCES <source>...]
  [INCLUDE_DIRECTORIES <PRIVATE|PUBLIC> <include_directory>...]
  [COMPILE_OPTIONS <PRIVATE|PUBLIC> <compile_option>...]
  [LINK_OPTIONS <PRIVATE|PUBLIC> <link_option>...]
  [LINK_LIBRARIES <PRIVATE|PUBLIC> <library>...]
  [DEPENDS <depend>...]
)

# Parameters:
# - target: Specifies the name of the executable target
# - sources: List of source files
# - include_directories: List of include directories
# - compile_options: List of compile options
# - link_options: List of link options
# - libraries: List of host libraries
# - depends: List of dependencies

# Scope:
# - Arguments following both PRIVATE and PUBLIC are used to build the current target.
```

### Creating a Library for the Host Platform

To define a library target for the host platform, use the `add_host_library` function:

```cmake
add_host_library(<target> <type>
  [SOURCES <source>...]
  [INCLUDE_DIRECTORIES <PRIVATE|PUBLIC> <include_directory>...]
  [COMPILE_OPTIONS <PRIVATE|PUBLIC> <compile_option>...]
  [LINK_OPTIONS <PRIVATE|PUBLIC> <link_option>...]
  [DEPENDS <depend>...]
)

# Parameters:
# - target: Specifies the name of the library target
# - type: Type of the library (e.g. STATIC, INTERFACE)
# - sources: List of source files (Note: INTERFACE library requires no source files)
# - include_directories: List of include directories
# - compile_options: List of compile options
# - link_options: List of link options
# - depends: List of dependencies

# Scope:
# - Arguments following both PRIVATE and PUBLIC are used to build the current target.
# - Arguments following PUBLIC are also used to build another target that links to the current target.
```

### Host Target Dependencies

The host functions, such as `add_host_library` and `add_host_executable`, create target names with the virtual namespace prefix `Host::` to distinguish them from ordinary target names. The host target names are used to define dependencies between host targets. For instance, the following code demonstrates how to create a host executable named `hello` that depends on a host library named `world`.

```cmake
add_host_executable(hello
  SOURCES hello.c
  LINK_LIBRARIES Host::world
)

add_host_library(world STATIC
  SOURCES world.c
)
```

#### Limitations

Only direct dependencies between host targets are allowed. Indirect dependencies are not properly reflected.

### Adding an Executable as a Test with CTest

To add an executable target as a test with CTest, use the `add_host_test` function:

```cmake
add_host_test(<target> [EXTRA_ARGS <extra_args>])

# Parameters:
# - target: Specifies the name of the executable target created with `add_host_executable`
# - extra_args: Any additional arguments to pass on the command line
```

### Adding Executable Tests by Scanning Source Code for Unity Test Macros

To automatically add executable tests by scanning the source code for Unity test macros, use the `unity_fixture_add_host_tests` function:

```cmake
unity_fixture_add_host_tests(<target> [EXTRA_ARGS <extra_args>])

# Parameters:
# - target: Specifies the name of the executable target created with `add_host_executable`
# - extra_args: Any additional arguments to pass on the command line
```

## CMake Variables

The following CMake variables can be used to configure internal behaviors:

- `CMAKE_HOST${lang}_COMPILER_LIST`: This variable is used to find the host compiler
- `CMAKE_HOST${lang}_OUTPUT_EXTENSION`: Defines the extension for object files
- `CMAKE_HOST${lang}_STANDARD`: Defines the language standard version
- `CMAKE_HOST${lang}_EXTENSIONS`: Specifies whether compiler-specific extensions are required
- `CMAKE_HOST_EXECUTABLE_SUFFIX`: Defines the extension for executable files
- `CMAKE_HOST_STATIC_LIBRARY_PREFIX`: Defines the prefix for static libraries
- `CMAKE_HOST_STATIC_LIBRARY_SUFFIX`: Defines the extension for static libraries
- `CMAKE_HOST_BUILD_TARGET`: Defines the target name to be used when building host targets (default: host-targets)

## Building the Project

To build and execute sample tests, use the following commands:

```bash
$ cd sample
$ cmake .
$ make host-targets
$ ctest
```

## Testing the CMake Scripts

To test the CMake scripts, use the following command:

```bash
$ pytest -n auto
```

## License

This project is licensed under the MIT License. For more details, see the [LICENSE](LICENSE) file.
