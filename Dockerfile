FROM python:2.7
MAINTAINER XiVO Team "dev@avencall.com"

ADD . /usr/src/xivo-backup

WORKDIR /usr/src/xivo-backup
RUN pip install -r requirements.txt

RUN install /usr/src/xivo-backup/bin/* /usr/sbin
