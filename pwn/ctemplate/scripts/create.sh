#!/bin/bash

sudo docker build -t ctemplate ../challenge/

sudo docker rm -f testpwn
sudo docker run  --name=testpwn -d -p 1337:1337 ctemplate
