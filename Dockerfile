#FROM python:3.6-alpine
#ADD . /code
#WORKDIR /code
#RUN pip install -r requirements/requirements.txt
#CMD ['celery', '-A', 'celery_tasks.main', 'worker', '--loglevel=info', '-P', 'gevent', '--without-heartbeat']

# 配置基础镜像
FROM alpine:latest

# 添加标签说明
LABEL author="Archerx" email="xuchaoao@outlook.com"  purpose="test dockerfile"
LABEL version="1.0"
LABEL description="This text illustrates \ that label-values can span multiple lines."

# 配置清华镜像地址
RUN echo "https://mirror.tuna.tsinghua.edu.cn/alpine/v3.8/main/" > /etc/apk/repositories

## 配置工作目录
#WORKDIR /data
#
## 配置Volueme挂载点 "/data"
#VOLUME [ "/data" ]

# 设置用户
USER root

# 设置时区变量
ENV TIME_ZONE Asia/Shanghai

#安装时区包并配置时区TIME_ZONE为中国标准时间
RUN apk add --no-cache -U tzdata \
    && ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime \
    && echo "${TIME_ZONE}" > /etc/timezone

# 更新升级软件
RUN apk add --update --upgrade \
    vim \
    gcc \
    g++

# 安装软件python3,升级pip,setuptools,安装selenium
RUN apk add --no-cache python3 \
    #&& apk add --no-cache python3-dev \
    && python3 -m ensurepip \
    && rm -r /usr/lib/python*/ensurepip \
    && pip3 install --default-timeout=100 --no-cache-dir --upgrade pip \
    && pip3 install --default-timeout=100 --no-cache-dir --upgrade setuptools \
    && if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi \
    && if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi \
    && rm -rf /var/cache/apk/* \
    && rm -rf ~/.cache/pip

ADD . /code
WORKDIR /code
RUN pip install -r requirements/requirements.txt
#RUN celery -A celery_tasks.main  worker --loglevel=info -P gevent --without-heartbeat
RUN echo "Archerx"

# 设置启动点 镜像启动时的第一个命令, 通常 docker run 的参数不会覆盖掉该指令
ENTRYPOINT [ "/bin/sh" ]

# 配置非生效对外端口
EXPOSE 8008

# 设置启动时预期的命令参数, 可以被 docker run 的参数覆盖掉.
# CMD [ "/bin/sh" ]
#CMD celery -A celery_tasks.main  worker --loglevel=info -P gevent --without-heartbeat


