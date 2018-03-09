import tkinter as tk
import tkinter.ttk as ttk
import guiLibs.rusEntry as rusEntry
import helpLibs.srs as srs
import guiLibs.AddDeckOrLevel as AddDeckOrLevel
import guiLibs.addFromMemrise as addFromMemrise
import guiLibs.browseFromMemrise as browseFromMemrise
import helpLibs.mycsv as mycsv
import helpLibs.consts as consts
import helpLibs.audio as audio
import threading

class newCards(tk.Frame):
	def __init__(self, master, controller):
		tk.Frame.__init__(self, master)
		self.controller = controller
		self.size = '950x500'
		self.bind("<<ShowFrame>>", self.on_show_frame)
		self.newAdditions = []
		self.newDeckLevels = {}
		self.curDecksAndLevels = srs.findDecksAndLevels()
		self.supportedLangs = consts.supportedLangs()
		self.supportedLangsReversed = {y:x for x,y in self.supportedLangs.items()}
		self.langCodes = [x for  x in self.supportedLangs]
		self.langNames = [self.supportedLangs[x] for x in self.langCodes] 

	def on_show_frame(self, event):
		for widget in self.winfo_children():
			widget.destroy()
		self.controller.controller.geometry(self.size)
		self.createWidgets()
		self.curDecksAndLevels = srs.findDecksAndLevels()
		self.newAdditions = []
		self.newDeckLevels = {}

	def createWidgets(self):
		self.firstFrame = tk.Frame(self)
		self.firstFrame.grid(sticky = 'n')
		self.title = tk.Label(self.firstFrame, font = (lambda x: self.cget('font'), 20), text = "Create new entry")
		self.title.grid(columnspan = 2)

		self.entryLabel  = tk.Label(self.firstFrame, text = "Entry*")
		self.entryLabel.grid(row = 1, column = 0)
		self.entryEntry = rusEntry.Entry(self.firstFrame)
		self.entryEntry.grid(row = 1, column = 1)

		self.translationLabel  = tk.Label(self.firstFrame, text = "Translation*")
		self.translationLabel.grid(row = 2, column = 0)
		self.translationEntry = rusEntry.Entry(self.firstFrame)
		self.translationEntry.grid(row = 2, column = 1)

		self.languageLabel = tk.Label(self.firstFrame, text = "Language code")
		self.languageLabel.grid(row = 3, column = 0)
		self.languageComboboxString = tk.StringVar()
		self.languageCombobox = ttk.Combobox(self.firstFrame, width = 17, values = self.langNames, validate = 'all', validatecommand = self.convertLangCode, state = 'readonly', textvariable = self.languageComboboxString, exportselection=0)
		self.languageCombobox.grid(row = 3, column = 1)
		self.notLang = tk.IntVar()
		self.LanguageCButton = tk.Checkbutton(self.firstFrame, text = "Check if not a language", variable= self.notLang, command = self.notLangCButtonPressed)
		self.LanguageCButton.grid(row = 3, column = 2)

		self.tagsLabel = tk.Label(self.firstFrame, text = "Tags")
		self.tagsLabel.grid(row = 4, column = 0)
		self.tagsEntry = rusEntry.Entry(self.firstFrame)
		self.tagsEntry.grid(row = 4, column = 1)

		self.deckLabel = tk.Label(self.firstFrame, text = "Deck")
		self.deckLabel.grid(row = 5, column = 0)
		self.deckEntry = tk.Entry(self.firstFrame, state = tk.DISABLED)
		self.deckEntry.grid(row = 5, column = 1)

		self.levelLabel = tk.Label(self.firstFrame, text = "Level")
		self.levelLabel.grid(row = 6, column = 0)
		self.levelEntry = tk.Entry(self.firstFrame, state = tk.DISABLED)
		self.levelEntry.grid(row = 6, column = 1)

		self.addButton = tk.Button(self.firstFrame, text = "Add entry", command = self.addEntry)
		self.addButton.grid(row = 7, column = 1)

		self.thirdFrame = tk.Frame(self)
		self.thirdFrame.grid(columnspan = 2, sticky = 'n')
		self.deckSelectLabel = tk.Label(self.thirdFrame, text = "Select deck for new entry")
		self.deckSelectLabel.grid(row = 0, column = 0)
		self.deckSelectListbox = tk.Listbox(self.thirdFrame, width = 50, selectmode = "BROWSE", exportselection=0, activestyle = 'none')
		self.deckSelectListbox.bind('<<ListboxSelect>>', self.populateLevelsListbox)
		self.deckSelectListbox.grid(row = 1, column = 0)
		self.addNewDeckButton = tk.Button(self.thirdFrame, text = "Add new deck", command = self.addNewDeck)
		self.addNewDeckButton.grid(row = 2, column = 0)

		self.levelSelectLabel = tk.Label(self.thirdFrame, text = "Select level for new entry")
		self.levelSelectLabel.grid(row = 0, column = 1)
		self.levelSelectListbox = tk.Listbox(self.thirdFrame, width = 50, selectmode = "BROWSE", exportselection=0, activestyle = 'none')
		self.levelSelectListbox.bind('<<ListboxSelect>>', self.updateDeckAndLevelEntry)
		self.levelSelectListbox.grid(row = 1, column = 1)	
		self.addNewLevelButton = tk.Button(self.thirdFrame, text = "Add new level", command = self.addNewLevel)
		self.addNewLevelButton.grid(row = 2, column = 1)

		self.entryShowLabel = tk.Label(self.thirdFrame, text = "Entries in the current level")
		self.entryShowLabel.grid(row = 0, column = 2)
		self.entryShowListbox = tk.Listbox(self.thirdFrame, width = 50, selectmode = "BROWSE", exportselection=0, activestyle = 'none')
		self.entryShowListbox.bind('<FocusOut>', lambda e: self.entryShowListbox.selection_clear(0, tk.END))
		self.entryShowListbox.grid(row = 1, column = 2)

		self.secondFrame = tk.Frame(self)
		self.secondFrame.grid(row = 0, column = 1, sticky = 'n')
		self.sessionAdditionsLabel = tk.Label(self.secondFrame, font = (lambda x: self.cget('font'), 20), text = "New additions")
		self.sessionAdditionsLabel.grid()

		self.scrollFrame = tk.Frame(self.secondFrame)
		self.scrollFrame.grid(rowspan = 2)
		self.sessionAdditionsListbox = tk.Listbox(self.scrollFrame, width = 50, selectmode = "BROWSE", exportselection=0, activestyle = 'none')
		self.sessionAdditionsListbox.bind('<FocusOut>', lambda e: self.sessionAdditionsListbox.selection_clear(0, tk.END))
		self.sessionAdditionsListbox.pack()
		self.scrollBar = tk.Scrollbar(self.scrollFrame, orient = tk.HORIZONTAL, command = self.sessionAdditionsListbox.xview)
		self.scrollBar.pack(side=tk.BOTTOM, fill=tk.X)
		self.sessionAdditionsListbox.config(xscrollcommand = self.scrollBar.set)

		self.pushButton = tk.Button(self.secondFrame, text = "Push additions", command = self.Push)
		self.pushButton.grid()

		self.removeSelectedAdditionButton = tk.Button(self.secondFrame, text = "Remove selected addition", command = self.removeSelectedAddition)
		self.removeSelectedAdditionButton.grid(column = 3, row = 1)

		self.backButton = tk.Button(self.secondFrame, text = "Go back", command = self.goback)
		self.backButton.grid(column = 4, row = 0, sticky = 'nw')

		self.addFromMemriseButton = tk.Button(self.secondFrame, text = "Add deck from Memrise", command = self.addFromMemriseFunc)
		self.addFromMemriseButton.grid(column = 3, row = 0, sticky = 'nw')

		self.browseFromMemriseButton = tk.Button(self.secondFrame, text = "Browse decks from Memrise", command = self.browseFromMemriseFunc)
		self.browseFromMemriseButton.grid(column = 3, row = 1, sticky = 'nw')

		self.populateDeckListbox()

	def browseFromMemriseFunc(self):
		gui = browseFromMemrise.browseFromMemrise(self)
		while not gui.submitted:
			self.controller.update()
			name = gui.name
		
		newCourse = gui.newCourse

		self.imgDl = []
		self.audDl = []
		if name:
			lastl = None
			for i in newCourse: #fixfiles.fix(name, self.supportedLangsReversed):
				i = i.split(',')
				if i[0].split('-')[0] == 'audio':
					temp = i[0]
					i[0] = i[1]
					i[1] = temp
					self.audDl.append(i.copy())
					i[1] = 'audio-' + i[1].split('/')[len(i[1].split('/')) - 1]

				elif i[1].split('-')[0] == 'audio':
					self.audDl.append(i.copy())
					i[1] = 'audio-' + i[1].split('/')[len(i[1].split('/')) - 1]

				elif i[0].split('-')[0] == 'img':
					temp = i[0]
					i[0] = i[1]
					i[1] = temp
					self.imgDl.append(i.copy())
					i[1] = 'img-' + i[1].split('/')[len(i[1].split('/')) -1]

				elif i[1].split('-')[0] == 'img':
					self.imgDl.append(i.copy())
					i[1] = 'img-' + i[1].split('/')[len(i[1].split('/')) -1]

				if not i[11] in self.newDeckLevels: 
					self.newDeckLevels[i[11]] = {}
					self.populateDeckListbox()
					self.deckSelectListbox.see(tk.END)
					self.deckSelectListbox.selection_set(tk.END)
					self.deckSelectListbox.selection_anchor(tk.END)
					#self.updateDeckAndLevelEntry()
					self.populateLevelsListbox()

				if not lastl == i[12]: self.addNewLevel(); lastl = i[12]
				i[10] = 0
				for L in self.curDecksAndLevels:
					for j in self.curDecksAndLevels[L]:
						for k in self.curDecksAndLevels[L][j]:
							if int(i[10]) <= int(k[10]):
								i[10] = str(int(k[10]) + 1)
				for L in self.newAdditions:
					if int(i[10]) <= int(L[10]):
								i[10] = str(int(L[10]) + 1)

				self.newAdditions.append(i)
				self.populateEntriesListbox()
				self.entryEntry.delete(0, tk.END)
				self.translationEntry.delete(0, tk.END)
				self.tagsEntry.delete(0, tk.END)

		self.populateSessionAdditionsListbox()
		gui.destroy()
		
	def addFromMemriseFunc(self):
		gui = addFromMemrise.addFromMemrise(self)
		while not gui.submitted:
			self.controller.update()
			name = gui.name
		
		newCourse = gui.newCourse

		self.imgDl = []
		self.audDl = []
		if name:
			lastl = None
			for i in newCourse: #fixfiles.fix(name, self.supportedLangsReversed):
				i = i.split(',')
				if i[0].split('-')[0] == 'audio':
					temp = i[0]
					i[0] = i[1]
					i[1] = temp
					self.audDl.append(i.copy())
					i[1] = 'audio-' + i[1].split('/')[len(i[1].split('/')) - 1]

				elif i[1].split('-')[0] == 'audio':
					self.audDl.append(i.copy())
					i[1] = 'audio-' + i[1].split('/')[len(i[1].split('/')) - 1]

				elif i[0].split('-')[0] == 'img':
					temp = i[0]
					i[0] = i[1]
					i[1] = temp
					self.imgDl.append(i.copy())
					i[1] = 'img-' + i[1].split('/')[len(i[1].split('/')) -1]

				elif i[1].split('-')[0] == 'img':
					self.imgDl.append(i.copy())
					i[1] = 'img-' + i[1].split('/')[len(i[1].split('/')) -1]

				if not i[11] in self.newDeckLevels: 
					self.newDeckLevels[i[11]] = {}
					self.populateDeckListbox()
					self.deckSelectListbox.see(tk.END)
					self.deckSelectListbox.selection_set(tk.END)
					self.deckSelectListbox.selection_anchor(tk.END)
					#self.updateDeckAndLevelEntry()
					self.populateLevelsListbox()

				if not lastl == i[12]: self.addNewLevel(); lastl = i[12]
				i[10] = 0
				for L in self.curDecksAndLevels:
					for j in self.curDecksAndLevels[L]:
						for k in self.curDecksAndLevels[L][j]:
							if int(i[10]) <= int(k[10]):
								i[10] = str(int(k[10]) + 1)
				for L in self.newAdditions:
					if int(i[10]) <= int(L[10]):
								i[10] = str(int(L[10]) + 1)

				self.newAdditions.append(i)
				self.populateEntriesListbox()
				self.entryEntry.delete(0, tk.END)
				self.translationEntry.delete(0, tk.END)
				self.tagsEntry.delete(0, tk.END)
		self.populateSessionAdditionsListbox()
		gui.destroy()

	def Push(self):
		if len(self.newAdditions) > 0:
			mycsv.write(mstr = self.newAdditions, lesson = True, new = True)
			self.controller.controller.doValues()
			self.curDecksAndLevels = srs.findDecksAndLevels()
			self.newAdditions = []
			self.newDeckLevels = {}
			self.populateSessionAdditionsListbox()
			
			old = self.deckSelectListbox.curselection()
			self.populateDeckListbox()
			self.deckSelectListbox.selection_set(old)
			self.deckSelectListbox.selection_anchor(old)
			self.deckSelectListbox.see(tk.ANCHOR)

			old = self.levelSelectListbox.curselection()
			self.populateLevelsListbox()
			self.levelSelectListbox.selection_set(old)
			self.levelSelectListbox.selection_anchor(old)
			self.levelSelectListbox.see(tk.ANCHOR)

			self.populateEntriesListbox()

			def d(self):
				for i in self.imgDl:
					audio.preload(i, r = True)
				for i in self.audDl:
					audio.preload(i, r = True)
			threading.Thread(target = d, kwargs={'self':self}, daemon = True).start()

	def removeSelectedAddition(self):
		if self.sessionAdditionsListbox.curselection() == (): return
		del self.newAdditions[self.sessionAdditionsListbox.curselection()[0]] 
		for n,h in enumerate(self.newAdditions):
			self.newAdditions[n][10] = '0'
			for i in self.curDecksAndLevels:
				for j in self.curDecksAndLevels[i]:
					for k in self.curDecksAndLevels[i][j]:
						if int(h[10]) <= int(k[10]):
							self.newAdditions[n][10] = str(int(k[10]) + 1)
			self.newAdditions[n][10] = str(int(h[10]) + n)
		self.populateSessionAdditionsListbox()

	def addNewDeck(self):
		gui = AddDeckOrLevel.AddDeckOrLevel(self, 'deck')
		while not gui.submitted:
			self.controller.update()
			name = gui.name
		gui.destroy()
		if name:
			if not name in self.newDeckLevels: self.newDeckLevels[name] = {}
			self.populateDeckListbox()
			self.deckSelectListbox.see(tk.END)
			self.deckSelectListbox.selection_set(tk.END)
			self.deckSelectListbox.selection_anchor(tk.END)
			self.updateDeckAndLevelEntry()
			self.populateLevelsListbox()

	def addNewLevel(self):
		if self.levelSelectListbox.get(tk.END) == '':
			if not self.deckSelectListbox.get(tk.ANCHOR) in self.newDeckLevels: self.newDeckLevels[self.deckSelectListbox.get(tk.ANCHOR)] = {}
			self.newDeckLevels[self.deckSelectListbox.get(tk.ANCHOR)]["Level1"] = []

		elif self.levelSelectListbox.get(tk.END).split("Level"):
			if self.deckSelectListbox.get(tk.ANCHOR) in self.curDecksAndLevels:
				if self.levelSelectListbox.get(tk.END) in self.curDecksAndLevels[self.deckSelectListbox.get(tk.ANCHOR)]:
					if not self.deckSelectListbox.get(tk.ANCHOR) in self.newDeckLevels: self.newDeckLevels[self.deckSelectListbox.get(tk.ANCHOR)] = {}
					self.newDeckLevels[self.deckSelectListbox.get(tk.ANCHOR)]["Level{}".format(int(self.levelSelectListbox.get(tk.END).split("Level")[1]) + 1)] = []
				
				elif self.levelSelectListbox.get(tk.END) in self.newDeckLevels[self.deckSelectListbox.get(tk.ANCHOR)]:
					if len(self.newDeckLevels[self.deckSelectListbox.get(tk.ANCHOR)][self.levelSelectListbox.get(tk.END)]) > 0:
						if not self.deckSelectListbox.get(tk.ANCHOR) in self.newDeckLevels: self.newDeckLevels[self.deckSelectListbox.get(tk.ANCHOR)] = {}
						self.newDeckLevels[self.deckSelectListbox.get(tk.ANCHOR)]["Level{}".format(int(self.levelSelectListbox.get(tk.END).split("Level")[1]) + 1)] = []

				elif len([x for x in [x for x in self.newAdditions if x[11] == self.deckSelectListbox.get(tk.ANCHOR).replace("*","")] if x[12] == self.levelSelectListbox.get(tk.END).replace("*","")]) > 0:
					self.newDeckLevels[self.deckSelectListbox.get(tk.ANCHOR)]["Level{}".format(int(self.levelSelectListbox.get(tk.END).split("Level")[1]) + 1)] = []
			elif len([x for x in self.newAdditions if x[11] == self.deckSelectListbox.get(tk.ANCHOR).replace("*","")]) > 0:
				if len([x for x in [x for x in self.newAdditions if x[11] == self.deckSelectListbox.get(tk.ANCHOR).replace("*","")] if x[12] == self.levelSelectListbox.get(tk.END).replace("*","")]) > 0:
					self.newDeckLevels[self.deckSelectListbox.get(tk.ANCHOR)]["Level{}".format(int(self.levelSelectListbox.get(tk.END).split("Level")[1]) + 1)] = []

		self.populateLevelsListbox()
		self.levelSelectListbox.see(tk.END)
		self.levelSelectListbox.selection_set(tk.END)
		self.levelSelectListbox.selection_anchor(tk.END)
		self.updateDeckAndLevelEntry()
		self.populateEntriesListbox()

	def addEntry(self):
		newline = [None]*15
		
		newline[0] = self.entryEntry.get().replace(",",'commaChar').replace("?","qChar").replace("/","slashChar")
		if newline[0] == "": return
		while newline[0][len(newline[0]) - 1] == " ":
			if newline[0] == " ": return
			newline[0] = newline[0][:-1]
			
		newline[1] = self.translationEntry.get().replace(",",'commaChar').replace("?","qChar").replace("/","slashChar")
		if newline[1] == "": return
		while newline[1][len(newline[1]) - 1] == " ":
			if newline[1] == " ": return
			newline[1] = newline[1][:-1]
		
		newline[2] = self.tagsEntry.get().replace(",",'commaChar').replace("?","qChar").replace("/","slashChar")
		if newline[2] == "": newline[2] = 'none' 
		while newline[2][len(newline[2]) - 1] == " ":
			newline[2] = newline[2][:-1]
		
		newline[3] = 'no'
		
		newline[4] = '0'
		
		newline[5] = '0'
		
		newline[6] = mycsv.curdate
		
		newline[7] = 'none'
		
		newline[8] = mycsv.curdate
		
		newline[9] = '0'
		
		newline[10] = '0'
		for i in self.curDecksAndLevels:
			for j in self.curDecksAndLevels[i]:
				for k in self.curDecksAndLevels[i][j]:
					if int(newline[10]) <= int(k[10]):
						newline[10] = str(int(k[10]) + 1)
		for i in self.newAdditions:
			if int(newline[10]) <= int(i[10]):
						newline[10] = str(int(i[10]) + 1)
		
		newline[11] = self.deckEntry.get().replace(",",'commaChar').replace("?","qChar").replace("/","slashChar")
		if newline[11] == "": return
		
		newline[12] = self.levelEntry.get()
		if newline[12] == "": return
		
		newline[13] = 'no'
		
		newline[14] = self.languageCombobox.get() if not self.notLang.get() else 'none'
		if newline[14] == "": return
		
		self.newAdditions.append(newline)		
		self.populateSessionAdditionsListbox()
		self.populateEntriesListbox()
		self.entryEntry.delete(0, tk.END)
		self.translationEntry.delete(0, tk.END)
		self.tagsEntry.delete(0, tk.END)

	def populateSessionAdditionsListbox(self):
		self.sessionAdditionsListbox.delete(0, tk.END)
		for i in self.newAdditions:
			self.sessionAdditionsListbox.insert(tk.END, "{}: {}: {}: {}: {}: {}".format(i[0],i[1],i[2],i[11],i[12],self.supportedLangs[i[14]]).replace("commaChar", ",").replace("qChar","?").replace("slashChar","/"))

	def updateDeckAndLevelEntry(self, e = None):
		self.populateEntriesListbox()
		self.deckEntry['state'] = tk.NORMAL
		self.deckEntry.delete(0, tk.END)
		self.deckEntry.insert(0, self.deckSelectListbox.get(tk.ANCHOR).replace("*",""))
		self.deckEntry['state'] = tk.DISABLED
		self.levelEntry['state'] = tk.NORMAL
		self.levelEntry.delete(0, tk.END)
		self.levelEntry.insert(0, self.levelSelectListbox.get(tk.ANCHOR).replace("*",""))
		self.levelEntry['state'] = tk.DISABLED

	def populateDeckListbox(self):
		self.deckSelectListbox.delete(0,tk.END)
		for i in self.curDecksAndLevels:
			self.deckSelectListbox.insert(tk.END, i)
		for i in self.newDeckLevels:
			if i not in self.curDecksAndLevels and not i[0] == '*':
				self.deckSelectListbox.insert(tk.END, "*"+i)

	def populateLevelsListbox(self, e = None):
		self.levelSelectListbox.delete(0, tk.END)
		if self.deckSelectListbox.get(tk.ANCHOR) in self.curDecksAndLevels:
			for i in self.curDecksAndLevels[self.deckSelectListbox.get(tk.ANCHOR)]:
				self.levelSelectListbox.insert(tk.END, i)
		if self.deckSelectListbox.get(tk.ANCHOR) in self.newDeckLevels:
			for i in self.newDeckLevels[self.deckSelectListbox.get(tk.ANCHOR)]:
				self.levelSelectListbox.insert(tk.END, "*"+i)
		self.updateDeckAndLevelEntry()

	def populateEntriesListbox(self):
		self.entryShowListbox.delete(0, tk.END)
		if self.deckSelectListbox.get(tk.ANCHOR) in self.curDecksAndLevels:
			if self.levelSelectListbox.get(tk.ANCHOR) in self.curDecksAndLevels[self.deckSelectListbox.get(tk.ANCHOR)]:
				for i in self.curDecksAndLevels[self.deckSelectListbox.get(tk.ANCHOR)][self.levelSelectListbox.get(tk.ANCHOR)]:
					self.entryShowListbox.insert(tk.END, "{}: {}".format(i[0],i[1]).replace("commaChar", ","))
		if self.deckSelectListbox.get(tk.ANCHOR) in self.newDeckLevels:
			if self.levelSelectListbox.get(tk.ANCHOR) in self.newDeckLevels[self.deckSelectListbox.get(tk.ANCHOR)]:
				for i in self.newDeckLevels[self.deckSelectListbox.get(tk.ANCHOR)][self.levelSelectListbox.get(tk.ANCHOR)]:
					self.entryShowListbox.insert(tk.END, "*{}: {}".format(i[0],i[1]).replace("commaChar", ","))
		for i in [x for x in [x for x in self.newAdditions if x[11] == self.deckSelectListbox.get(tk.ANCHOR).replace("*","")] if x[12] == self.levelSelectListbox.get(tk.ANCHOR).replace("*","")]:
			self.entryShowListbox.insert(tk.END, "*{}: {}".format(i[0],i[1]).replace("commaChar", ","))

	def convertLangCode(self):
		if self.languageComboboxString.get() in self.supportedLangsReversed:
			self.languageComboboxString.set(self.supportedLangsReversed[self.languageCombobox.get()])
		return True

	def notLangCButtonPressed(self):
		if self.notLang.get():
			self.languageCombobox['state'] = tk.DISABLED
		else:
			self.languageCombobox['state'] = tk.NORMAL

	def goback(self):
		self.controller.show_frame("DecksAndLevels", me = self)