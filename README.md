# Hosta

> Host based test automation for C

## About

This project provides CMake scripts designed to build unit test programs using the host build toolchain and execute them on the host machine via CTest while a cross-build toolchain environment is configured.


## Prerequisite

The following packages should be installed to use on your host environment

- CMake (3.16 or above)
- C compiler toolchain (GCC, clang, etc)

The following packages are necessary to test this project

- build-essential
- docker
- clang
- gcc-mingw-w64
- gcovr
- ninja-build
- pytest3
- pytest3-xdist
- python3

You may use the following commands to build a Docker image which the required packages are installed
```bash
$ docker build -t host-test-dev .
$ docker run --rm -it -v `pwd`:/test host-test-dev
$ cd /test
```

## How to set up

You may copy the files under cmake directory to CMake script directory of your project, then add the following command to your top-level CMakeLists.txt

```cmake
include(cmake/HostTest.cmake)
```

## How to use

Create an executable running on the host

```cmake
add_host_executable(<target>
  [SUFFIX <suffix>]
  [SOURCES <sources>]
  [OBJECTS <objects>]
  [INCLUDE_DIRECTORIES <include_directories>]
  [COMPILE_OPTIONS <compile_options>]
  [LINK_OPTIONS <link_options>]
  [DEPENDS <depends>]
)

# target: Specifies an executable target name
# suffix: Speficies an executable suffix
# sources: List of source files
# objects: List of object files
# include_directories: List of include directories
# compile_options: List of compile options
# link_options: List of link options
# depends: List of dependencies
```

Automatically add an executable running on the host as a test with CTest

```cmake
add_host_test(<target> [EXTRA_ARGS <extra_args>])

# target: Specifies an executable target created with `add_host_executable`
# extra_args: Any extra arguments to pass on the command line
```

Automatically add an executable running on the host as tests with CTest by scanning source code for Unity test macros

```cmake
unity_fixture_add_host_tests(<target> [EXTRA_ARGS <extra_args>])

# target: Specifies an executable target created with `add_host_executable`
# extra_args: Any extra arguments to pass on the command line
```

## How to build

You may use the following commands to build and execute sample tests
```bash
$ cd sample
$ cmake .
$ make host-targets
$ ctest
```

## How to test

You may use the following commands to test CMake scripts
```bash
$ pytest -n auto
```

## License

This project source code is available under MIT license. See [LICENSE](LICENSE).
