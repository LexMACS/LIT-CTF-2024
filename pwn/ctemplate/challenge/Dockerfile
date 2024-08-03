FROM ubuntu:22.04 AS base

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential socat

COPY ./Makefile ./ctemplate.c ./flag.txt ./
RUN make

CMD socat \
       TCP-LISTEN:1337,reuseaddr,fork \
       EXEC:"./ctemplate",pty,ctty,stderr,raw,echo=0
