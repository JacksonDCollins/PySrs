from gtts import gTTS
import os
import pygame
import time
from bs4 import BeautifulSoup
import requests
import time
import math
import sys
import helpLibs.consts as consts

volume = 0.8

freq = 48000     # audio CD quality
bitsize = -16    # unsigned 16 bit
channels = 2     # 1 is mono, 2 is stereo
buffer = 2048    # number of samples (experiment to get best sound)


def startAudio():
	pygame.mixer.init(freq, bitsize, channels, buffer)

def endAudio():
	pygame.mixer.quit()

def play(i):
	file = "{}\\{}\\{}\\{}\\{}.mp3".format(consts.cwd(),consts.fname(),i[11],i[12],i[0].replace("?", "qChar"))
	file = file.replace(" .mp3", ".mp3")
	file = file.replace("..mp3", ".mp3")
	file = file.replace("/", "slashChar")
	file = file.lower()
	pygame.mixer.music.load(file)
	pygame.mixer.music.set_volume(volume)
	pygame.mixer.music.play()

	while pygame.mixer.music.get_busy():
		pass		

def preload(i):
	if i[14] == 'none':return
	fdir ="{}\\{}\\{}\\{}".format(consts.cwd(),consts.fname(),i[11],i[12])
	file = "{}\\{}\\{}\\{}\\{}.mp3".format(consts.cwd(),consts.fname(),i[11],i[12],i[0].replace("?", "qChar"))
	file = file.replace(" .mp3", ".mp3")
	file = file.replace("..mp3", ".mp3")
	file = file.replace("/", "slashChar")
	file = file.lower()
	if not os.path.isdir(fdir):
		os.makedirs(fdir)
	if not os.path.isfile(file):
		try:
			with open(file, 'wb') as f:
				f.write(getVoice(i[0], i[14]))
		except:
			tts = gTTS(text=i[0].replace("commaChar", ","), lang=i[14])
			tts.save("{}".format(file))

def getVoice(word, lang):
	session = requests.session()
	url = 'http://shtooka.net/search.php?str={}'.format(word)
	r = session.get(url)

	soup = BeautifulSoup(r.text, "html.parser")

	a = soup.findAll("h1")
	for i in a:
		for j in i.findAll("img"):
			if 'class="player' in str(i):
				if lang in str(i).split("'")[3].split("'")[0]:
					mp3url = str(i).split("'")[3].split("'")[0]
					break

	r = session.get(mp3url)
	return r.content

def dAllVoice(workdoc):
	j = 1
	source = ""
	shc = 0
	ttsc = 0
	t0 = time.time()
	with open(workdoc,'r', encoding = 'utf-8') as f:
		lines = f.read().split("\n")
	f.close()
	for i in lines:
		if j ==0:
			i = i.split(",")
			fdir ="{}\\{}\\{}\\{}".format(consts.cwd(),consts.fname(),i[11],i[12])
			file = "{}\\{}\\{}\\{}\\{}.mp3".format(consts.cwd(),consts.fname(),i[11],i[12],i[0].replace("?", "qChar"))
			file = file.replace(" .mp3", ".mp3")
			file = file.replace("..mp3", ".mp3")
			file = file.replace("/", "slashChar")
			file = file.lower()
			if not os.path.isdir(fdir):
				os.makedirs(fdir)
			if not os.path.isfile(file):
				try:
					with open(file, 'wb') as f:
						f.write(getVoice(i[0].replace('commaChar',",").replace("qChar","?").replace("slashChar","/").lower()))
						source = "shtooka"
						shc = shc + 1
				except Exception as e:
					tts = gTTS(text=i[0].replace('commaChar',",").replace("qChar","?").replace("slashChar","/").lower(), lang=i[14])
					tts.save("{}".format(file))
					source = "tts"
					ttsc = ttsc + 1
				
				progress = int(i[10])/len(lines)
				progress = math.floor(progress*100)
				os.system('cls')
				print('\r[{}] {}% {}/{} {} {} tts:{} shtooka:{} time:{}'.format('#'*math.floor(progress/10) + ' '*(10-math.floor(progress/10)), progress, i[10], len(lines), file, source, ttsc, shc, math.floor(time.time() - t0)), end = "\r", flush = True)
		else:
			j = 0

if __name__ == "__main__":
	dAllVoice(consts.workdoc())