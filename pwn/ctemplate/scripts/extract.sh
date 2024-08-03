#!/bin/bash

sudo docker cp "testpwn:/lib/x86_64-linux-gnu/libc.so.6" ../attachments/
sudo docker cp "testpwn:/lib64/ld-linux-x86-64.so.2" ../attachments/
sudo docker cp "testpwn:/app/ctemplate" ../attachments/
