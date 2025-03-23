FROM python:latest


ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV ALLOWED_IDS ""
ENV BOT_TOKEN ""
ENV TG_PROXY ""
LABEL authors="tomer.klein@gmail.com"

RUN apt -yqq update && \
    apt -yqq install fping && \
    rm -rf /var/lib/apt/lists/*
    
RUN pip3 install --upgrade pip --no-cache-dir && \
    pip3 install --upgrade setuptools --no-cache-dir

RUN mkdir -p /app/config

COPY requirements.txt /tmp

RUN pip3 install -r /tmp/requirements.txt

# EXPOSE 8081

COPY app /app

WORKDIR /app

ENTRYPOINT ["/usr/local/bin/python3", "/app/app.py"]