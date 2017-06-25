FROM alpine:latest
LABEL maintainer="playniuniu@gmail.com"

ENV BUILD_DEP gcc make python3-dev musl-dev

COPY app/ /opt/app/
COPY run.py /opt/

RUN apk add --no-cache --update python3 $BUILD_DEP \
    && pip3 install --no-cache-dir -U pip \
    && pip3 install --no-cache-dir -r /opt/app/requirments.txt \
    && apk del $BUILD_DEP \
    && rm -rf /var/cache/apk/* \
    && rm -rf /root/.cache/pip/*

EXPOSE  9011 
WORKDIR /opt/

CMD ["./run.py"]
