#!/bin/bash

sudo rm -r ../attachments/*

sudo docker cp "testpwn:/lib/x86_64-linux-gnu/libc.so.6" ../attachments/
sudo docker cp "testpwn:/app/bflat" ../attachments/
