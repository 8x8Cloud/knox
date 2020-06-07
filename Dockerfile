# Apache Software License 2.0
#
# Copyright (c) 2020, Lance Johnson.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Built with following command:
#
# docker build --no-cache=true -t 8x8cloud/knox:vX.X.X
ARG IMAGE_URL=python
ARG IMAGE_TAG=3.8-alpine

FROM $IMAGE_URL:$IMAGE_TAG as base

FROM base as builder

# Dependencies for python packages
RUN apk update && apk upgrade
RUN apk --no-cache add --virtual .buildset build-base gcc libffi-dev openssl-dev

RUN mkdir /install
WORKDIR /install
COPY /src/knox/requirements.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt --no-warn-script-location

RUN apk del .buildset

FROM base

LABEL org.label-schema.schema-version="1.0" \
      org.label-schema.maintainer="lance.johnson@8x8.com" \
      org.label-schema.name="8x8cloud/knox" \
      org.label-schema.description="Certificate management using a Vault backend" \
      org.label-schema.url="https://knox.readthedocs.org" \
      org.label-schema.vcs-url="git@github.com/8x8cloud/knox.git" \
      org.label-schema.vendor="8x8" \
      org.label-schema.version='0.0.24'

COPY --from=builder /install /usr/local
COPY /src /app

WORKDIR /app

ENTRYPOINT ["/usr/local/bin/python", "-m", "knox"]
