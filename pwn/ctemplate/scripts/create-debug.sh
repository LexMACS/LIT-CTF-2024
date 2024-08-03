#!/bin/bash

sudo docker build -t ctemplate ../challenge/

sudo docker rm -f testpwn
sudo docker run  --name=testpwn -d \
  -v /home/rythm/ctf/writing/LIT-CTF-2024/pwn/ctemplate/challenge/ctemplate.c:/app/ctemplate.c \
  -v /home/rythm/ctf/writing/LIT-CTF-2024/pwn/ctemplate/challenge/exploit.py:/debug/exploit.py \
  -p 1337:1337 ctemplate 

sudo docker cp ./setup-debug.sh testpwn:/debug/setup.sh
sudo docker exec -it testpwn /debug/setup.sh
