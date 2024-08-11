#!/bin/bash

cd /debug

apt update
apt install -y python3 python3-pip gdb git vim tmux elfutils

rm /usr/lib/python*/EXTERNALLY-MANAGED
pip3 install pwntools

git clone https://github.com/pwndbg/pwndbg
cd pwndbg
./setup.sh

cd /debug

#remember to hold "shift" when selecting stuff with mouse for copy/paste
tmux new-session "tmux setw -g mouse on; bash"
