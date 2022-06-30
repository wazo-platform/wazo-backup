FROM python:3.7-slim-buster
LABEL maintainer="Wazo Maintainers <dev@wazo.community>"

COPY . /usr/src/wazo-backup
WORKDIR /usr/src/wazo-backup
RUN install /usr/src/wazo-backup/bin/* /usr/sbin
