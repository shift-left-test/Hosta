# hosta

> Host based test automation for CMake

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
```cmake
add_host_test(<Name>
  DISABLED  # When set, this test will not be run
  SOURCES <list of source files>
  INCLUDE_DIRECTORIES <list of header paths>
  COMPILE_OPTIONS <list of compile options>
  LINK_OPTIONS <list of link options>
  DEPENDS <list of dependencies>
  EXTRA_ARGS <arguments for test executable>
)

unity_fixture_add_tests(<Name>
  DISABLED  # When set, this test will not be run
  SOURCES <list of source files>
  INCLUDE_DIRECTORIES <list of header paths>
  COMPILE_OPTIONS <list of compile options>
  LINK_OPTIONS <list of link options>
  DEPENDS <list of dependencies>
  EXTRA_ARGS <arguments for test executable>
)
```

## How to build

You may use the following commands to build and execute sample tests
```bash
$ cd sample
$ cmake .
$ make build-test
$ ctest
```

## How to test

You may use the following commands to test CMake scripts
```bash
$ pytest -n auto
```

## License

This project source code is available under MIT license. See [LICENSE](LICENSE).
