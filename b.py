#!/usr/bin/env python3
import os
import subprocess

base = "/home/lexmathcsclub/LIT-CTF-2024"

chal = input("Challenge: ")
auth = input("Author: ")
desc = input("Description: ")

path = base + "/" + chal

print(os.listdir(path))

if "player" not in os.listdir(path) and "attachments" not in os.listdir(path):
	subprocess.run(["mkdir", path + "/player"])

keyword = "player"
if "attachments" in os.listdir(path):
	keyword = "attachments"

string = f"Author: {auth}\nDescription: {desc}\n"
with open(path + f"/{keyword}/desc.txt", "w") as f:
	f.write(string)

print("Write complete")
