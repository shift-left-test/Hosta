# cmake-host-unittest

## About

This project provides CMake scripts designed to build unit test programs using the host build toolchain and execute them via CTest while a cross-build toolchain environment is configured.


## Prerequisite

The following packages should be installed on your host environment

- CMake (3.10 or above)
- GCC toolchain
- Make

The following packages may be required for extra purposes

- Docker (to build and run a Docker image)
- gcovr (for code coverage)
- ninja-build (to use the Ninja generator)
- pytest3 (for selftesting)
- python3 (for selftesting)

You may use the following commands to build a Docker image which the required packages are installed

    $ docker build -t host-test-dev .
    $ docker run --rm -it -v `pwd`:/test host-test-dev
    $ cd /test

Or you may use the following commands to install required packages on your Ubuntu machine

    $ sudo apt-get update
    $ sudo apt-get install -y cmake gcc gcc-multilib g++ g++-multilib python3 python3-pytest ninja-build
    $ python3 -m pip install -U pip
    $ python3 -m pip install -U pytest gcovr


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
