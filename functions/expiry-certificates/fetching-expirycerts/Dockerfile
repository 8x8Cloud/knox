FROM openfaas/classic-watchdog:0.18.18 as watchdog

FROM ubuntu:latest as base

FROM base as builder

COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

# Dependencies for python packages
RUN apt-get update
RUN apt-get install -y build-essential gcc make libssl-dev libffi-dev python3-dev python3-pip jq
RUN groupadd app && useradd -r -g app app

COPY /src/knox/requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
RUN pip3 install knox==0.1.11

LABEL org.label-schema.schema-version="1.0" \
      org.label-schema.maintainer="lance.johnson@8x8.com" \
      org.label-schema.name="8x8cloud/knox" \
      org.label-schema.description="Certificate management using a Vault backend" \
      org.label-schema.url="https://knox.readthedocs.org" \
      org.label-schema.vcs-url="git@github.com/8x8cloud/knox.git" \
      org.label-schema.vendor="8x8" \
      org.label-schema.version='0.1.11'

COPY /src/.env /app/.env
COPY /src/config/settings.json /app/config/settings.json

WORKDIR /app

RUN chown app /app

USER app

ENV fprocess="xargs knox"

ENV read_timeout="120"
ENV write_timeout="120"

ENV write_debug="true"

EXPOSE 8080

HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
