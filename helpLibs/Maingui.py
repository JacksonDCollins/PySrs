import tkinter as tk
import tkinter.ttk as ttk
import helpLibs.srs as srs
import os
import helpLibs.mycsv as mycsv
import zipfile
import datetime
import zlib
from datetime import timedelta as td
import guiLibs.Mainmenu as Mainmenu
import guiLibs.learnLesson as learnLesson
import guiLibs.reviewLesson as reviewLesson
import guiLibs.Analytics as Analytics
import guiLibs.Settings as Settings
import helpLibs.DAndLgui as DAndLgui
import helpLibs.consts as consts
import threading

def convertStrTimeAddDays(date, days = 0):
	k = srs.convertToTime(date) + td(days = days)
	return "{}/{}/{}".format(k.day, k.month, k.year), k

def Crc32Hasher(file_path):
    buf_size = 65536
    crc32 = 0
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(buf_size)
            if not data:
                break
            crc32 = zlib.crc32(data, crc32)
    return format(crc32 & 0xFFFFFFFF, '08x')

def makeBackup():
	dal = srs.findDecksAndLevels()
	for folder, subfolders, files in os.walk("{}\{}".format(consts.cwd(),consts.fname())):
		subs = subfolders
		for i in subs:
			if i in dal:
				for folder, subfolders, files in os.walk("{}\{}\{}".format(consts.cwd(),consts.fname(),i)):
					nsubs = subfolders
					for j in nsubs:
						if j in dal[i]:
							for folder, subfolders, files in os.walk("{}\{}\{}\{}".format(consts.cwd(),consts.fname(),i,j)):
									for f in files:
										nnsubs = [x[0].lower() for x in dal[i][j]]
										f = f.replace(".mp3", "").replace("qchar","?").replace("slashchar","/")
										if f in nnsubs:
											pass
										else:
											if os.path.isfile("{}\{}.mp3".format(folder, f)):
												if not 'audio-' in "{}\{}.mp3".format(folder, f):
													os.remove("{}\{}.mp3".format(folder, f))
											else:
												try:
													if not 'audio-' in "{}\{}".format(folder, f.replace("?","qchar") + '.mp3'):
														os.remove("{}\{}".format(folder, f.replace("?","qchar") + '.mp3'))
												except: pass

						else:
							for folder, subfolders, files in os.walk("{}\{}\{}\{}".format(consts.cwd(),consts.fname(),i,j), topdown = False):
								for file in files:
									os.remove("{}\{}".format(folder, file))
								os.rmdir(folder)
			else:
				for folder, subfolders, files in os.walk("{}\{}\{}".format(consts.cwd(),consts.fname(),i), topdown = False):
					for file in files:
						os.remove("{}\{}".format(folder, file))
					os.rmdir(folder)		
		
		
	d = str(datetime.datetime.now()).split(" ")[0]

	if not os.path.isdir(consts.backups() + d):
	 		os.makedirs(consts.backups() + d)

	for folder, subfolders, files in os.walk(consts.backups() + d):
		if len(files) == 0:
			p = consts.backups() + d + '\\session1.zip'
		else:
			p = consts.backups() + d + '\\session{}.zip'.format(len(files)+1)

	mzip = zipfile.ZipFile(p, 'w')

	for folder, subfolders, files in os.walk(consts.cwd()):
		for file in files:
			if file.endswith('.csv'):
				mzip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), consts.cwd()), compress_type = zipfile.ZIP_DEFLATED)
	mzip.close()

	for folder, subfolders, files in os.walk(consts.backups() + d):
		f = (consts.backups() + d + "\\" + files[len(files)-2])
		fc = Crc32Hasher(f)
		pc = Crc32Hasher(p)
		if fc == pc and not f == p:
			os.remove(p)

	for folder, subfolders, files in os.walk(consts.backups()):
		for i in subfolders:
			j = i.replace("-","/").split("/")
			k = "{}/{}/{}".format(j[2],j[1],j[0])
			if (convertStrTimeAddDays(mycsv.curdate)[1] - convertStrTimeAddDays(k)[1]).days > 5:
				for folder, subfolders, files in os.walk(consts.backups() + i):
					for file in files:
						os.remove(consts.backups() + i + "\\" + file)
				os.rmdir(consts.backups() + i)

def createDefaults():
	if not os.path.isfile(consts.workdoc()):
		with open(consts.workdoc(), 'w', encoding = 'utf-8') as t:
			t.write('0SENTENCE,1TRANSLATION,2TAGS,3LEARNED,4ATTEMPTS,5SUCCESFUL ATTEMPS,6DAY LAST ATTEMPT,7LAST ATTEMPT RESULT,8DAY TO REVIEW,9ATTEMPT STREAK,10ID,DECK11,LEVEL12,IGNORE13,LANGUAGE14')
		t.close()


class MainFrame(tk.Tk):
	class Splash(tk.Frame):
		def __init__(self, parent):
			tk.Frame.__init__(self, parent)
			self.loadingLabel = tk.Label(self, text = "Loading")
			self.loadingLabel.grid()

	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.size = "800x500"
		self.title('PySrs')
		self.geometry(self.size)

		load = self.Splash(self)
		load.grid()
		self.update()

		#createDefaults()
		self.doValues()
		self.deck = None
		self.r = None
		container = tk.Frame(self)
		container.grid()
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		
		self.frames = {}
		self.size = "800x500"

		for F in (Mainmenu.Mainmenu, DAndLgui.DAndLgui, reviewLesson.reviewLesson, Analytics.Analytics, learnLesson.learnLesson,Settings.Settings):
			page_name = F.__name__
			frame = F(container, self)
			self.frames[page_name] = frame

			# put all of the pages in the same location;
			# the one on the top of the stacking order
			# will be the one that is visible.
			frame.grid(row=0, column=0, sticky="nsew")

		load.destroy()
		self.geometry(self.size)
		self.show_frame("Mainmenu")

	def show_frame(self, page_name, me = None, deck = None):
		if me:
			for widget in me.winfo_children():
				widget.destroy()
		'''Show a frame for the given page name'''
		self.deck = deck
		frame = self.frames[page_name]
		frame.tkraise()
		frame.event_generate("<<ShowFrame>>")

	def doValues(self):
		try: 
			#?????????????????????????????????????????????????????????????????????????????????????????????????????????
			self.frames['Analytics'].historyfiles()
			self.Analynew = False
		except: 
			self.Analynew = True
		t = srs.findTo()
		self.toReview = t[0]
		self.toLearn = t[1]
		self.total = t[2]
		self.deck = None
		self.dandl = srs.findDecksAndLevels()
		self.reviewCounts = {}
		self.learnCounts = {}
		self.totalCounts = {}
		self.langs = [{consts.supportedLangs()[x]:x} if x in consts.supportedLangs() else {'Other':x} for x in list(set([x.split(',')[14] for x in self.total]))]
		self.langs = {v:k for d in self.langs for k, v in d.items()}
		self.deckLangs = {}
		for i in self.dandl:
			self.reviewCounts[i] = len([x for x in self.toReview if i in x.split(",")[11]])
			self.learnCounts[i] = len([x for x in self.toLearn if i in x.split(",")[11]])
			self.totalCounts[i] = len([x for x in self.total if i in x.split(",")[11]])

			for j in self.dandl[i]:
				for k in self.dandl[i][j]:
					if i not in self.deckLangs:
						self.deckLangs[i] = ''
					#if not k[14] == self.deckLangs[i] and not self.deckLangs[i] == '':
					#	print('error found entry with different language in the deck')
					self.deckLangs[i] = self.langs[k[14]]