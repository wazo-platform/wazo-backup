FROM python:2.7.16-buster
MAINTAINER Wazo Maintainers <dev@wazo.community>

ADD . /usr/src/xivo-backup

WORKDIR /usr/src/xivo-backup

RUN install /usr/src/xivo-backup/bin/* /usr/sbin
