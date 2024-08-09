#!/usr/local/bin/python
import string

_ = open("flag.txt", "rb").read()
blocked = string.ascii_letters + string.digits

while True:
    cmd = ascii(input("Enter code: "))[1:-1]
    if any([char in cmd for char in blocked]):
        print("no haxing >:(")
        continue
    try:
        exec(cmd)
    except:
        print("error :P")
