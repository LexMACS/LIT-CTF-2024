#!/bin/bash

sudo docker build -t bflat ../challenge

sudo docker rm -f testpwn
sudo docker run  --name=testpwn -d --priviliged \
  -v /home/rythm/ctf/writing/LIT-CTF-2024/pwn/bflat/challenge/bflat.c:/app/bflat.c \
  -v /home/rythm/ctf/writing/LIT-CTF-2024/pwn/bflat/challenge/Makefile:/app/Makefile \
  -v /home/rythm/ctf/writing/LIT-CTF-2024/pwn/bflat/challenge/exploit.py:/debug/exploit.py \
  -p 1337:1337 bflat 

sudo docker cp ./setup-debug.sh testpwn:/debug/setup.sh
sudo docker exec -it testpwn /debug/setup.sh
