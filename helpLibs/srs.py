import os
from datetime import datetime, timedelta
import helpLibs.mycsv as mycsv
import helpLibs.audio as audio
import time
import tkinter as tk
import math
import random
from PIL import Image, ImageTk
import helpLibs.consts as consts
import threading

try: audLight = Image.open('helpLibs/audLight.png')
except: audLight = Image.open('audLight.png')

try: audDark = Image.open('helpLibs/audDark.png')
except: audDark = Image.open('audDark.png')

def findTo(r = None, workdoc = consts.workdoc(), *args):
	toReview = []
	rList = []
	lList = []
	tList = []
	curdate = datetime.strptime("{}/{}/{}".format(datetime.now().day,datetime.now().month,datetime.now().year), "%d/%m/%Y")
	lines = mycsv.read()
	
	if len(args):
		if r == "review":
			for i in range(1,len(lines)):
				if lines[i].split(",")[13] == "no":
					d = convertToTime(lines[i].split(",")[8])
					if d <= curdate:
						if lines[i].split(",")[11] == args[0]:
							if lines[i].split(",")[3] == "yes":
								toReview.append(lines[i])
		elif r == "learn":
			for i in range(1,len(lines)):
				if lines[i].split(",")[13] == 'no':
					if lines[i].split(",")[11] == args[0]:
						if not lines[i].split(",")[3] == "yes":
							toReview.append(lines[i])
		elif r == "total":
			for i in range(1,len(lines)):
				if lines[i].split(",")[13] == 'no':
					if lines[i].split(",")[11] == args[0]:
						toReview.append(lines[i])
	else:
		if r == "review":
			for i in range(1,len(lines)):
				if lines[i].split(",")[13] == 'no':
					d = convertToTime(lines[i].split(",")[8])
					if d <= curdate:
						if lines[i].split(",")[3] == "yes":
							toReview.append(lines[i])
		elif r == "learn":
			for i in range(1,len(lines)):
				if lines[i].split(",")[13] == 'no':
					if not lines[i].split(",")[3] == "yes":
						toReview.append(lines[i])
		elif r == "total":
			for i in range(1,len(lines)):
				if lines[i].split(",")[13] == 'no':
					toReview.append(lines[i])
		elif r == None: 	
			for i in range(1,len(lines)):
				if lines[i].split(",")[13] == 'no':
					d = convertToTime(lines[i].split(",")[8])
					if d <= curdate:
						if lines[i].split(",")[3] == "yes":
							rList.append(lines[i])

					if not lines[i].split(",")[3] == "yes":
						lList.append(lines[i])

					tList.append(lines[i])
			toReview = [rList, lList, tList]
	return toReview

def findDecksAndLevels():
	decks = {}
	lines = mycsv.read()
	j = 0
	for i in lines:
		if j == 1:
			i = i.split(",")
			if not i[11] in decks:
				decks[i[11]] = {}
			if not i[12] in decks[i[11]]:
				decks[i[11]][i[12]] = []
			decks[i[11]][i[12]].append(i)
		else: j = 1
	return decks

def setupNewLesson(deck = None, workdoc = consts.workdoc(), review = True):
	reviewPerLesson = consts.reviewPerLesson()
	newPerLesson = consts.newPerLesson()
	if review:
		selectedReview = []
		tr = findTo("review", workdoc, deck)
		sr = findTo("review")
		if not deck == None:
			if len(tr) >= reviewPerLesson:
				for i in tr:
					if len(selectedReview) < reviewPerLesson:
						selectedReview.append(i)
					else:
						for n,j in enumerate(selectedReview):
							if convertToTime(j.split(',')[8]) > convertToTime(i.split(',')[8]):
								if i not in selectedReview:
									selectedReview[n] = i
			else:
				selectedReview = tr
			return selectedReview
		else:
			if len(sr) >= reviewPerLesson:
				for i in sr:
					if len(selectedReview) < reviewPerLesson:
						selectedReview.append(i)
					else:
						for n,j in enumerate(selectedReview):
							if convertToTime(j.split(',')[8]) > convertToTime(i.split(',')[8]):
								if i not in selectedReview:
									selectedReview[n] = i
			else:
				selectedReview = sr
			return selectedReview
	else:
		selectedLearn = []
		tl = findTo("learn", workdoc, deck)
		for i in tl:
			if len(selectedLearn) < newPerLesson:
				selectedLearn.append(i)
		return selectedLearn

def afterAnswer(w, i, root):
	root.submit = False
	w.delete(0, len(w.get()))
	w["bg"] = "white"
	w["fg"] = "black"
	if not root.lineEdited:
		if not 'audio-' in root.line.split(',')[1].replace('commaChar', ','): audio.preload(root.line.split(',')); audio.play(root.line.split(','))
		else: audio.play(root.line.split(','), a = True)
	root.update()

def waitForAnswer(gotAnswer, root, eWidget, line):
	root.submit = False
	start = time.time()
	rtime = 0
	last = ""
	lasttime = 0
	l = start
	afk = False
	try:
		while not gotAnswer:
			userinput = eWidget.get().replace(',','commaChar').lower()
			if root.focus_get() == eWidget and not afk: rtime += time.time() - l
			l = time.time()
			if not last == userinput:
				last = userinput
				lasttime = rtime
				afk = False
			if rtime - lasttime > 5:
				afk = True
				rtime = lasttime

			if root.submit:
				root.submit = False
				gotAnswer = True
			if userinput == root.line[0].lower().replace(".", ""):
				gotAnswer = True
				root.submit = False
			if root.lineEdited:
				return (userinput.lower(), -1)
			root.update()
		return (userinput.lower(), rtime)
	except:
		return (userinput.lower(), rtime)
	
def doReviewLesson(sentences, root, tWidget, eWidget, tagsWidget, cWidget):
	curdate = "{}/{}/{}".format(datetime.now().day,datetime.now().month,datetime.now().year)
	completed = []
	uncompleted = []
	redo = []
	hissentences = []
	gotAnswer = False

	while len(sentences) > 0:
		for n,i in enumerate(sentences):
			cWidget.configure(text = "{}/{}".format(len(completed) + 1, len(sentences) + len(completed) + len(uncompleted) + len(redo)))
				# if len(uncompleted) > 0:
				# 	if random.randint(0,4) == 1:
				# 		i = uncompleted[len(uncompleted) - 1]
				# 		n = len(uncompleted) - 1
				# 		fromUncomplete = True
			root.line = i.split(",")

			eWidget.delete(0, len(eWidget.get()))
			if not 'img-' in root.line[1].replace('commaChar', ',') and not 'audio-' in root.line[1].replace('commaChar', ','):
				tWidget.configure(text = root.line[1].replace("commaChar", ","), image = None)
				tWidget.unbind('<Button-1>')
			elif 'img-' in root.line[1].replace('commaChar', ','):
				imgFile = "{}\\{}\\{}\\{}\\{}\\{}".format(consts.cwd(),consts.fname(),root.line[11],root.line[12],consts.images(),root.line[1].replace('img-',''))
				im = Image.open(imgFile)
				img = ImageTk.PhotoImage(im)
				tWidget.img = img
				tWidget.configure(image = img, text = '')
				tWidget.unbind('<Button-1>')
			elif 'audio-' in root.line[1].replace('commaChar', ','):
				img = ImageTk.PhotoImage(audLight)
				tWidget.img = img
				tWidget.configure(image = img, text = '')
				def audPlay(): img = ImageTk.PhotoImage(audDark); tWidget.img = img; tWidget.configure(image = img, text = ''); audio.play(root.line, a = True); img = ImageTk.PhotoImage(audLight); tWidget.img = img;	tWidget.configure(image = img, text = '')
				tWidget.bind('<Button-1>', lambda x: threading.Thread(target = audPlay, daemon = True).start())
			tagsWidget.configure(text = root.line[2].replace("commaChar", ",")) if not root.line[2] == "none" else tagsWidget.configure(text = "")
			eWidget.focus()
			gotAnswer = False
			root.lineEdited = False

			res = waitForAnswer(gotAnswer, root, eWidget, root.line)
			userinput = res[0]
			wait = res[1]
			
			try:
				root.editEntrytl.destroy()
			except:
				pass

			if root.lineEdited == False:
					if userinput == root.line[0].lower().replace(".", ""):
						eWidget["bg"] = "lime green"
						eWidget["fg"] = "white"
						root.update()
						root.line[4] = str(int(root.line[4]) + 1)
						root.line[5] = str(int(root.line[5]) + 1)					
						root.line[6] = curdate						
						root.line[7] = 'success'						
						root.line[9] = str(int(root.line[9]) + 1)						
						root.line[8] = addDays(root.line)					
						nhisline = root.line[:]
						nhisline.append('none')
						nhisline.append("-1")
						nhisline.append(str(datetime.now().strftime('%H:%M:%S')))
						nhisline.append(str(wait))
						hissentences.append(nhisline)
						root.line = ','.join(root.line)
						completed.append(root.line)
						del sentences[n]
					else:
						eWidget["bg"] = "red"
						eWidget["fg"] = "white"
						root.update()
						root.line[4] = str(int(root.line[4]) + 1)
						root.line[6] = curdate
						root.line[7] = 'fail'
						root.line[8] = addDays(root.line)
						root.line = ','.join(root.line)
						redo.append(root.line)
						del sentences[n]
			else:
				if root.line[13] == "no":
					del sentences[n]
					root.line = ','.join(root.line)
					sentences.append(root.line)
				elif root.line[13] == "yes":
					del sentences[n]
					nhisline = root.line[:]
					nhisline.append('none')
					nhisline.append("-1")
					nhisline.append(str(datetime.now().strftime('%H:%M:%S')))
					nhisline.append('-1')
					hissentences.append(nhisline)
					root.line = ','.join(root.line)
					completed.append(root.line)
		
			afterAnswer(eWidget, root.line.split(","), root)
			root.lineEdited = False

			while len(redo) > 0:
				for n, i in enumerate(redo):
					cWidget.configure(text = "{}/{}".format(len(completed) + 1, len(sentences) + len(completed) + len(uncompleted) + len(redo)))
					root.line = i.split(",")
					if not 'img-' in root.line[1].replace('commaChar', ',') and not 'audio-' in root.line[1].replace('commaChar', ','):
						tWidget.configure(text = root.line[1].replace("commaChar", ","), image = None)
						tWidget.unbind('<Button-1>')
					elif 'img-' in root.line[1].replace('commaChar', ','):
						imgFile = "{}\\{}\\{}\\{}\\{}\\{}".format(consts.cwd(),consts.fname(),root.line[11],root.line[12],consts.images(),root.line[1].replace('img-',''))
						im = Image.open(imgFile)
						#im = im.resize(size=(50,50))
						img = ImageTk.PhotoImage(im)
						tWidget.img = img
						tWidget.configure(image = img, text = '')
						tWidget.unbind('<Button-1>')
					elif 'audio-' in root.line[1].replace('commaChar', ','):
						img = ImageTk.PhotoImage(audLight)
						tWidget.img = img
						tWidget.configure(image = img, text = '')
						def audPlay(): img = ImageTk.PhotoImage(audDark); tWidget.img = img; tWidget.configure(image = img, text = ''); audio.play(root.line, a = True); img = ImageTk.PhotoImage(audLight); tWidget.img = img;	tWidget.configure(image = img, text = '')
						tWidget.bind('<Button-1>', lambda x: threading.Thread(target = audPlay, daemon = True).start())
					gotAnswer = False

					root.lineEdited = False
					cAnswerEntry =  tk.Label(root, text = root.line[0].lower().replace(".", ""), font = (lambda x: cAnswerEntry.cget('font'), 32), width = 50, wraplength = 1255)
					cAnswerEntry.grid(row = 4, column = 0, columnspan = 2, rowspan = 1)
					
					res = waitForAnswer(gotAnswer, root, eWidget, root.line)
					userinput = res[0]
					wait = res[1] + wait

					try:
						root.editEntrytl.destroy()
					except:
						pass
							
					if root.lineEdited == False:
							if userinput == root.line[0].lower().replace(".", ""):
								eWidget["bg"] = "lime green"
								eWidget["fg"] = "white"
								root.update()
								root.line[9] = str(1)
								root.line[8] = addDays(root.line)
								root.line.append(str(wait))
								root.line = ','.join(root.line)
								uncompleted.append(root.line)
								del redo[n]
							else:
								eWidget["bg"] = "red"
								eWidget["fg"] = "white"
								root.line = ','.join(root.line)
								redo.append(root.line)
								del redo[n]
								root.update()
					else:
						if root.line[13] == "no":
							del redo[n]
							root.line = ','.join(root.line)
							redo.append(root.line)
						elif root.line[13] == "yes":
							del redo[n]
							nhisline = root.line[:]
							nhisline.append('none')
							nhisline.append("-1")
							nhisline.append(str(datetime.now().strftime('%H:%M:%S')))
							nhisline.append('-1')
							hissentences.append(nhisline)
							root.line = ','.join(root.line)
							completed.append(root.line)

					afterAnswer(eWidget, root.line.split(","), root)
					root.lineEdited = False
					cAnswerEntry.destroy()

	while len(uncompleted) > 0:
		for n, i in enumerate(uncompleted):
			cWidget.configure(text = "{}/{}".format(len(completed) + 1, len(sentences) + len(completed) + len(uncompleted)))
			root.line = i.split(",")
			if not 'img-' in root.line[1].replace('commaChar', ',') and not 'audio-' in root.line[1].replace('commaChar', ','):
				tWidget.configure(text = root.line[1].replace("commaChar", ","), image = None)
				tWidget.unbind('<Button-1>')
			elif 'img-' in root.line[1].replace('commaChar', ','):
				imgFile = "{}\\{}\\{}\\{}\\{}\\{}".format(consts.cwd(),consts.fname(),root.line[11],root.line[12],consts.images(),root.line[1].replace('img-',''))
				im = Image.open(imgFile)
				#im = im.resize(size=(50,50))
				img = ImageTk.PhotoImage(im)
				tWidget.img = img
				tWidget.configure(image = img, text = '')
				tWidget.unbind('<Button-1>')
			elif 'audio-' in root.line[1].replace('commaChar', ','):
				img = ImageTk.PhotoImage(audLight)
				tWidget.img = img
				tWidget.configure(image = img, text = '')
				def audPlay(): img = ImageTk.PhotoImage(audDark); tWidget.img = img; tWidget.configure(image = img, text = ''); audio.play(root.line, a = True); img = ImageTk.PhotoImage(audLight); tWidget.img = img;	tWidget.configure(image = img, text = '')
				tWidget.bind('<Button-1>', lambda x: threading.Thread(target = audPlay, daemon = True).start())
			gotAnswer = False

			root.lineEdited = False
			cAnswerEntry =  tk.Label(root, text = root.line[0].lower().replace(".", ""), font = (lambda x: cAnswerEntry.cget('font'), 32), width = 50, wraplength = 1255)
			cAnswerEntry.grid(row = 4, column = 0, columnspan = 2, rowspan = 1)
			
			res = waitForAnswer(gotAnswer, root, eWidget, root.line)
			userinput = res[0]
			wait = res[1]

			try:
				root.editEntrytl.destroy()
			except:
				pass
					
			if root.lineEdited == False:
					if userinput == root.line[0].lower().replace(".", ""):
						eWidget["bg"] = "lime green"
						eWidget["fg"] = "white"
						root.update()
						root.line[9] = str(1)
						root.line[8] = addDays(root.line)
						nhisline = root.line[:-1]
						nhisline.append('none')
						nhisline.append("-1")
						nhisline.append(str(datetime.now().strftime('%H:%M:%S')))
						nhisline.append(str(float(root.line[15]) + wait))
						del root.line[15]
						hissentences.append(nhisline)
						root.line = ','.join(root.line)
						completed.append(root.line)
						del uncompleted[n]
					else:
						eWidget["bg"] = "red"
						eWidget["fg"] = "white"
						root.update()
						root.line = ','.join(root.line)
						uncompleted.append(root.line)
						del uncompleted[n]
			else:
				if root.line[13] == "no":
					del uncompleted[n]
					root.line = ','.join(root.line[:-1])
					uncompleted.append(root.line)
				elif root.line[13] == "yes":
					del uncompleted[n]
					nhisline = root.line[:-1]
					nhisline.append('none')
					nhisline.append("-1")
					nhisline.append(str(datetime.now().strftime('%H:%M:%S')))
					nhisline.append('-1')
					hissentences.append(nhisline)
					root.line = ','.join(root.line[:-1])
					completed.append(root.line)

			afterAnswer(eWidget, root.line.split(","), root)
			root.lineEdited = False

	root.update()
	for widget in root.winfo_children():
		widget.destroy()
		root.update()
	text = tk.Label(root, font =(lambda x: Label.cget('font'), 32), text = "Review Done!")
	text.grid()
	root.update()

	mycsv.write(consts.workdoc(), mstr = completed, lesson = True, review = True)
	mycsv.writeHistory(hissentences,  tag = 'review')

def convertToTime(date):
	return datetime.strptime("{}/{}/{}".format(date.split("/")[0],date.split("/")[1],date.split("/")[2]), "%d/%m/%Y")

def addDays(line):
	if line[7] == "fail":
		days = 1
	else:
		streakco = math.floor((float(line[9]) * 1.8)*(float(line[9]) * 1.8))
		attemptsco = int(line[4])
		sucattemptsco = int(line[5])
		try:
			tco = (sucattemptsco/attemptsco)
		except:
			tco = 0
		days = math.floor(streakco * tco)
		if days == 0:
			days = 1
		
	newDate = convertToTime(line[6]) + timedelta(days = days)
	return "{}/{}/{}".format(newDate.day, newDate.month, newDate.year)

def doLearnLesson(sentences, root, tWidget, eWidget, tagsWidget, cWidget):
	curdate = "{}/{}/{}".format(datetime.now().day,datetime.now().month,datetime.now().year)
	gotAnswer = False
	completed = []

	while len(sentences) > 0:
		random.shuffle(sentences)
		for n,i in enumerate(sentences):
			root.line = i.split(",")
			eWidget.delete(0, len(eWidget.get()))
			if not 'img-' in root.line[1].replace('commaChar', ',') and not 'audio-' in root.line[1].replace('commaChar', ','):
				tWidget.configure(text = root.line[1].replace("commaChar", ","), image = None)
				tWidget.unbind('<Button-1>')
			elif 'img-' in root.line[1].replace('commaChar', ','):
				imgFile = "{}\\{}\\{}\\{}\\{}\\{}".format(consts.cwd(),consts.fname(),root.line[11],root.line[12],consts.images(),root.line[1].replace('img-',''))
				im = Image.open(imgFile)
				#im = im.resize(size=(50,50))
				img = ImageTk.PhotoImage(im)
				tWidget.img = img
				tWidget.configure(image = img, text = '')
				tWidget.unbind('<Button-1>')
			elif 'audio-' in root.line[1].replace('commaChar', ','):
				img = ImageTk.PhotoImage(audLight)
				tWidget.img = img
				tWidget.configure(image = img, text = '')
				def audPlay(): img = ImageTk.PhotoImage(audDark); tWidget.img = img; tWidget.configure(image = img, text = ''); audio.play(root.line, a = True); img = ImageTk.PhotoImage(audLight); tWidget.img = img;	tWidget.configure(image = img, text = '')
				tWidget.bind('<Button-1>', lambda x: threading.Thread(target = audPlay, daemon = True).start())

			tagsWidget.configure(text = root.line[2].replace("commaChar", ",")) if not root.line[2] == "none" else tagsWidget.configure(text = "")

			if root.line[3] == 'no':
				cAnswerEntry =  tk.Label(root, text = root.line[0].replace("commaChar", ",").replace(".", ""), font = (lambda x: cAnswerEntry.cget('font'), 32), width = 50, wraplength = 1255)
				cAnswerEntry.grid(row = 4, column = 0, columnspan = 2, rowspan = 1)
				cWidget.set(0)
				root.update()		
				if not 'audio-' in root.line[1].replace('commaChar', ','): audio.preload(root.line); audio.play(root.line)
				else:
					img = ImageTk.PhotoImage(audDark)
					tWidget.img = img
					tWidget.configure(image = img, text = '')
					root.update()
					audio.play(root.line, a = True)
					img = ImageTk.PhotoImage(audLight)
					tWidget.img = img
					tWidget.configure(image = img, text = '')
				root.line[3] = 'step0'
			else:
				cWidget.set(int(root.line[3].split("step")[1]))

			eWidget.focus()
			gotAnswer = False
			root.lineEdited = False
			userinput , time = waitForAnswer(gotAnswer, root, eWidget, root.line)
			try:
				root.editEntrytl.destroy()
			except:
				pass
					
			if userinput == root.line[0].lower().replace(".", ""):
				eWidget["bg"] = "lime green"
				eWidget["fg"] = "white"
				root.line[3] = "step{}".format(int(root.line[3].split("step")[1])+1)
				cWidget.set(int(root.line[3].split("step")[1]))
				root.update()
				root.line = ','.join(root.line)
				sentences[n] = root.line
			else:
				eWidget["bg"] = "red"
				eWidget["fg"] = "white"
				root.line[3] = "no-step{}".format(int(root.line[3].split("step")[1]))
				root.update()
				root.line = ','.join(root.line)
				sentences[n] = root.line

			cAnswerEntry.destroy()
			afterAnswer(eWidget, root.line.split(","), root)

			if not 'no' in root.line.split(",")[3]:
				if int(root.line.split(",")[3].split('step')[1]) == 6:
					root.line = root.line.split(",")
					root.line[3] = 'yes'
					root.line[6] = curdate
					root.line[8] = addDays(root.line)
					root.line = ','.join(root.line)
					completed.append(root.line)
					del sentences[n]
			else:
				root.line = root.line.split(",")
				root.line[3] = root.line[3].split("no-")[1]
				root.line = ','.join(root.line)
				sentences[n] = root.line

	root.update()
	for widget in root.winfo_children():
		widget.destroy()
		root.update()
	text = tk.Label(root, font =(lambda x: Label.cget('font'), 32), text = "lesson Done!")
	text.grid()
	root.update()

	mycsv.write(consts.workdoc(), mstr = completed, lesson = True, review = False, learn = True)
