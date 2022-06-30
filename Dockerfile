FROM python:2.7.16-buster
MAINTAINER Wazo Maintainers <dev@wazo.community>

ADD . /usr/src/wazo-backup

WORKDIR /usr/src/wazo-backup

RUN install /usr/src/wazo-backup/bin/* /usr/sbin
