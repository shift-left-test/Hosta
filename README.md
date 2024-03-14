# lute

> Lightweight unit test environment on host machines for CMake

## About

This project provides CMake scripts designed to build unit test programs using the host build toolchain and execute them on the host machine via CTest while a cross-build toolchain environment is configured.


## Prerequisite

The following packages should be installed to use on your host environment

- CMake (3.10 or above)
- GCC toolchain
- Make

The following packages are necessary to test this project

- Docker
- clang
- gcc-mingw-w64
- gcovr
- ninja-build
- pytest3
- pytest3-xdist
- python3

You may use the following commands to build a Docker image which the required packages are installed

    $ docker build -t host-test-dev .
    $ docker run --rm -it -v `pwd`:/test host-test-dev
    $ cd /test


## How to use

You may use the following commands to build and execute sample tests

    $ cmake .
    $ make build-test
    $ ctest


## How to test

You may use the following commands to test CMake scripts

    $ pytest -n auto


## License

This project source code is available under MIT license. See [LICENSE](LICENSE).
