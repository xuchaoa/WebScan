# 配置基础镜像
FROM ubuntu:16.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U && python3 -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
USER root

COPY requirements/requirements.txt /tmp/python3.reqs
RUN python3 -m pip install -r /tmp/python3.reqs
ENTRYPOINT [ "/bin/bash" ]
RUN apt-get autoclean && apt-get clean && apt-get autoremove
ADD . /code
WORKDIR /code
CMD celery -A celery_tasks.main  worker --loglevel=info -P gevent --without-heartbeat


