FROM ubuntu:24.04 AS base

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential socat

COPY ./Makefile ./boring.c ./flag.txt ./
RUN make

CMD socat \
       TCP-LISTEN:1337,reuseaddr,fork \
       EXEC:"./boring",pty,ctty,stderr,raw,echo=0
