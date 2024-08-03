#!/bin/bash

apt install -y python3 python3-pip gdb git vim tmux
pip3 install pwntools

git clone https://github.com/longld/peda.git ~/peda
echo "source ~/peda/peda.py" >> ~/.gdbinit

tmux
