#!/usr/bin/env python3


base = "/home/lexmathcsclub/LIT-CTF-2024"
playerBase = base + "/player"

# idea: go through directories and look for a folder that is either called 'attachments' or 'player'
import os
import subprocess
import json

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
		if chal not in os.listdir(playerBase + "/" + category):
			subprocess.run(["mkdir", playerFilePre])
		#playerFilePre = playerBase + "/" + category + "/" + chal
		ufPath = chal_base + "/" + userFiles
		for file in os.listdir(ufPath):
			filePath = ufPath + "/" + file
			playerFilePath = playerFilePre + "/" + file
			subprocess.run(["cp", "-r", filePath, playerFilePath])
