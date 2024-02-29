# Copyright (c) 2024 LG Electronics Inc.
# SPDX-License-Identifier: MIT

FROM ubuntu:20.04 AS builder

ARG DEBIAN_FRONTEND=noninteractive

RUN echo "dash dash/sh boolean false" | debconf-set-selections
RUN dpkg-reconfigure dash

RUN apt-get clean
RUN apt-get update
RUN apt-get install -y --no-install-recommends locales software-properties-common
RUN locale-gen en_US.UTF-8

RUN apt-get install -y --no-install-recommends \
    build-essential \
    clang \
    cmake \
    gcc \
    gcc-mingw-w64 \
    gcc-multilib \
    ninja-build \
    python3 \
    python3-pip \
    python3-pytest \
    tzdata

RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install -U pip
RUN python3 -m pip install -U \
    gcovr \
    pytest

FROM ubuntu:20.04

COPY --from=builder /usr /usr
COPY --from=builder /etc /etc
COPY --from=builder /var /var

ENV LANG=en_US.UTF-8
ENV TZ=Asia/Seoul
ENV GIT_SSL_NO_VERIFY=true

CMD ["/bin/bash"]
