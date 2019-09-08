# 配置基础镜像
FROM centos:latest

# 添加标签说明
# LABEL author="Archerx" email="xuchaoao@outlook.com"  purpose="test dockerfile"
# LABEL version="1.0"
RUN yum install epel-* -y \
    yum install python36 -y \
    yum install python36-pip -y

RUN python3 -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN python3 -m pip install --upgrade pip

ADD . /code
WORKDIR /code
RUN pip install -r requirements/requirements.txt
ENTRYPOINT [ "/bin/bash" ]
CMD celery -A celery_tasks.main  worker --loglevel=info -P gevent --without-heartbeat
