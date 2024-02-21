# cmake-host-unittest

## About

This project provides CMake scripts designed to build unit test programs using the host build toolchain and execute them via CTest while a cross-build toolchain environment is configured.


## Prerequisite

The following packages must be installed on your host environment

- CMake (3.10 or above)
- G++
- GCC
- gcovr
- pytest3
- python3

You may use the following command to install required packages on your Ubuntu machine

    $ sudo apt-get update
    $ sudo apt-get install -y cmake gcc gcc-multilib g++ g++-multilib python3 python3-pytest
    $ python3 -m pipi install -U pip
    $ python3 -m pipi install -U pytest gcovr


## How to use

You may use the following commands to build and execute sample tests

    $ cmake .
    $ make build-test
    $ ctest


## How to test

You may use the following commands to test CMake scripts

    $ pytest


## License

This project source code is available under MIT license. See [LICENSE](LICENSE).
