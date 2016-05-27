FROM python:2.7.9
MAINTAINER XiVO Team "dev+docker@proformatique.com"

ADD . /usr/src/xivo-backup

WORKDIR /usr/src/xivo-backup

RUN install /usr/src/xivo-backup/bin/* /usr/sbin
