FROM python:alpine
WORKDIR /

RUN apk add --no-cache wget tar gzip build-base libffi-dev && \
    wget https://github.com/thewhiteh4t/nexfil/archive/refs/heads/main.tar.gz && \
    tar -xzf main.tar.gz && \
    rm main.tar.gz

WORKDIR /nexfil-main

RUN pip3 install -r requirements.txt

RUN echo '#!/bin/sh' > /nexfil-main/run.sh && \
    echo 'python3 /nexfil-main/nexfil.py $@' >> /nexfil-main/run.sh && \
    chmod +x /nexfil-main/run.sh

RUN apk del --no-cache wget tar gzip build-base

ENTRYPOINT [ "/nexfil-main/run.sh" ]
