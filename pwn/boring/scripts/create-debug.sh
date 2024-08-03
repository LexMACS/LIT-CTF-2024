#!/bin/bash

sudo docker build -t boring ../challenge

sudo docker rm -f testpwn
sudo docker run  --name=testpwn -d \
  -v /home/rythm/ctf/writing/LIT-CTF-2024/pwn/boring/challenge/boring.c:/app/boring.c \
  -v /home/rythm/ctf/writing/LIT-CTF-2024/pwn/boring/challenge/exploit.py:/debug/exploit.py \
  -p 1337:1337 boring 

sudo docker cp ./setup-debug.sh testpwn:/debug/setup.sh
sudo docker exec -it testpwn /debug/setup.sh
