# 配置基础镜像
FROM centos:latest

# 添加标签说明
# LABEL author="Archerx" email="xuchaoao@outlook.com"  purpose="test dockerfile"
# LABEL version="1.0"
RUN yum install update && \
    yum install python36 && yum install pip3-python
ADD . /code
WORKDIR /code
RUN pip install -r requirements/requirements.txt
ENTRYPOINT [ "/bin/bash" ]
CMD celery -A celery_tasks.main  worker --loglevel=info -P gevent --without-heartbeat
