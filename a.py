#!/usr/bin/env python3

import os
import subprocess
import json

base = "/home/lexmathcsclub/LIT-CTF-2024"
playerBase = base + "/player"

if "player" in os.listdir(base):
	subprocess.run(["rm", "-rf", playerBase])

print("Removed player folder")

if "player" not in os.listdir(base):
	subprocess.run(["mkdir", playerBase])

categories = ["pwn", "rev", "crypto", "web", "misc"]

for c in categories:
	if c not in os.listdir(playerBase):
		subprocess.run(["mkdir", playerBase + "/" + c])

# idea: go through directories and look for a folder that is either called 'attachments' or 'player'
categories = [name for name in os.listdir(base) if os.path.isdir(os.path.join(base, name)) and name[0] != '.']

print(categories)

for category in categories:
	cat_base = base + "/" + category
	chals = [name for name in os.listdir(cat_base) if os.path.isdir(os.path.join(cat_base, name))]
	for chal in chals:
		chal_base = cat_base + "/" + chal
		files = os.listdir(chal_base)
		
		userFiles = ""
		if "attachments" in files:
			userFiles = "attachments"
		if "player" in files:
			userFiles = "player"

		if userFiles == "":
			continue

		playerFilePre = playerBase + "/" + category + "/" + chal
		ufPath = chal_base + "/" + userFiles
		if chal not in os.listdir(playerBase + "/" + category) and len(os.listdir(ufPath)) > 0:
			subprocess.run(["mkdir", playerFilePre])
		

		# is there a director in ufPath?
		hasDir = False
		for file in os.listdir(ufPath):
			if os.path.isdir(ufPath + "/" + file):
				hasDir = True
				break
		if hasDir:
			subprocess.run(["mkdir", playerFilePre + "/" + chal])
		for file in os.listdir(ufPath):
			filePath = ufPath + "/" + file
			playerFilePath = playerFilePre + "/" + file
			if hasDir:
				playerFilePath = playerFilePre + "/" + chal + "/" + file
			subprocess.run(["cp", "-r", filePath, playerFilePath])
		if hasDir:
			os.chdir(playerFilePre)
			subprocess.run(["zip", "-r", chal + ".zip", chal])
			#subprocess.run(["mv", base + "/" + chal + ".zip", playerFilePre])
			subprocess.run(["rm", "-rf", chal])

os.chdir(base)
