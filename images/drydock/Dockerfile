# Copyright 2017 AT&T Intellectual Property.  All other rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
FROM ubuntu:16.04

ARG UBUNTU_REPO=http://archive.ubuntu.com/ubuntu
ARG TRUSTED_UBUNTU_REPO=no
ARG ALLOW_UNAUTHENTICATED=false
ARG PIP_TRUSTED_HOST=foo.com
ARG PIP_INDEX_URL=https://pypi.org/simple
ENV container docker
ENV PORT 9000
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# Copy direct dependency requirements only to build a dependency layer
RUN echo  "deb  ${UBUNTU_REPO} xenial main restricted universe multiverse" > /etc/apt/sources.list; \
    echo "deb  ${UBUNTU_REPO} xenial-security main restricted universe multiverse" >> /etc/apt/sources.list; \
    echo "deb  ${UBUNTU_REPO} xenial-updates main restricted universe multiverse" >> /etc/apt/sources.list; \
    cat /etc/apt/sources.list; \
    echo "APT::Get::AllowUnauthenticated ${ALLOW_UNAUTHENTICATED};" >> /etc/apt/apt.conf.d/00-local-mirrors;


COPY ./requirements-host.txt /tmp/drydock/
COPY ./hostdeps.sh /tmp/drydock
WORKDIR /tmp/drydock
RUN ./hostdeps.sh; \
    rm -r /var/lib/apt/lists/*

COPY ./requirements-lock.txt /tmp/drydock/
RUN pip3 install \
    --no-cache-dir \
    -r /tmp/drydock/requirements-lock.txt


COPY . /tmp/drydock

WORKDIR /tmp/drydock
RUN python3 setup.py install

EXPOSE $PORT

ENTRYPOINT ["./entrypoint.sh"]

CMD ["server"]
