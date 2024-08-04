#!/bin/bash

sudo docker build -t bflat ../challenge/

sudo docker rm -f testpwn
sudo docker run  --name=testpwn -d -p 1337:1337 bflat
