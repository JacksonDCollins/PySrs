import tkinter as tk
import tkinter.ttk as ttk
import helpLibs.srs as srs
import helpLibs.audio as audio
import guiLibs.rusEntry as rusEntry
import helpLibs.mycsv as mycsv

class DecksAndLevels(tk.Frame):
	def __init__(self, master, controller):
		tk.Frame.__init__(self, master)
		self.grid()
		self.controller = controller
		self.size = "900x600"
		self.line = None
		self.lastDeck = ()
		self.lastLevel = ()
		self.lastEntry = ()
		self.deckLevels = self.controller.controller.dandl
		self.changes = ['None,None,None,None,None,None,None,None,None,None,None,None,None,None']
		self.bind("<<ShowFrame>>", self.on_show_frame)

	def on_show_frame(self, event):
		for widget in self.winfo_children():
			widget.destroy()
		self.controller.controller.geometry(self.size)
		self.createWidgets()
		self.deckLevels = self.controller.controller.dandl
		self.lastDeck = ()
		self.lastLevel = ()
		self.lastEntry = ()

	def createWidgets(self):
		self.changes = ['None,None,None,None,None,None,None,None,None,None,None,None,None,None']
		self.decksLBox = tk.Listbox(self, selectmode = "BROWSE", exportselection=0, width = 40, activestyle = 'none')
		for i in srs.findDecksAndLevels():
			self.decksLBox.insert(tk.END, i)
		self.decksLBox.grid(column = 0, row =0)
		self.decksLBox.bind('<<ListboxSelect>>', self.decksLBoxSelect)
		self.decksLBox.bind('<Key>', self.decksLBoxSelect)   

		self.levelsLBox = tk.Listbox(self, selectmode = "BROWSE", exportselection=0, width = 40, activestyle = 'none')
		self.levelsLBox.grid(column = 1, row = 0)
		self.levelsLBox.bind('<<ListboxSelect>>', self.levelsLBoxSelect)
		self.levelsLBox.bind('<Key>', self.levelsLBoxSelect)   

		self.entriesLBox = tk.Listbox(self, selectmode = "BROWSE", exportselection=0, width = 40, activestyle = 'none')
		self.entriesLBox.grid(column = 2, row = 0)
		self.entriesLBox.bind('<<ListboxSelect>>', self.entriesLBoxSelect)
		self.entriesLBox.bind('<Key>', self.entriesLBoxSelect)

		self.f = tk.Frame(self)
		self.f.grid(column = 3, row = 0, sticky = 'N')

		self.searchButton = tk.Button(self.f, text = "Search", command = self.search)
		self.searchButton.grid(row = 1)

		self.newButton = tk.Button(self.f, text = "Add new decks and entries", command = self.new)
		self.newButton.grid(row = 2)

		self.buttonGoBack = tk.Button(self.f, text = "Go Back and commit saves", command = self.goMainMenu)
		self.buttonGoBack.grid(row = 0)

		self.editFrame = tk.Frame(self)

	def new(self):
		self.controller.show_frame("newCards", me = self)
		
	def search(self):
		self.controller.show_frame("newSearch", me = self)
			
	def decksLBoxSelect(self, e):
		if not self.decksLBox.curselection() == ():
			try:
				if e.keysym == 'Down':
					if self.decksLBox.curselection()[0] < self.decksLBox.size() -1:
						t = self.decksLBox.curselection()[0] + 1 
					else: 
						return
					self.decksLBox.select_clear(self.decksLBox.curselection())
					self.decksLBox.selection_set(t)
					self.controller.update()
					self.update()
				elif e.keysym == 'Up':
					if self.decksLBox.curselection()[0] > 0:
						t = self.decksLBox.curselection()[0] - 1 
					else: 
						return
					self.decksLBox.select_clear(self.decksLBox.curselection())
					self.decksLBox.selection_set(t)
					self.controller.update()
					self.update()
				elif e.keysym == '??':
					pass
				else:
					return
			except:
				pass

			self.editFrame.grid_forget()
			self.lastDeck = self.decksLBox.get(self.decksLBox.curselection())
			self.levelsLBox.delete(0, tk.END)
			self.entriesLBox.delete(0, tk.END)
			for i in self.deckLevels[self.lastDeck]:
				self.levelsLBox.insert(tk.END, i)
			self.createEditDeckWidgets(self.editFrame, self.lastDeck)
			self.editFrame.grid(column = 0, row = 1, columnspan = 9999, sticky = 'n')

	def levelsLBoxSelect(self, e):
		if not self.levelsLBox.curselection() == ():
			try:
				if e.keysym == 'Down':
					if self.levelsLBox.curselection()[0] < self.levelsLBox.size() -1:
						t = self.levelsLBox.curselection()[0] + 1 
					else: 
						return
					self.levelsLBox.select_clear(self.levelsLBox.curselection())
					self.levelsLBox.selection_set(t)
					self.controller.update()
					self.update()
				elif e.keysym == 'Up':
					if self.levelsLBox.curselection()[0] > 0:
						t = self.levelsLBox.curselection()[0] - 1 
					else:
						return
					self.levelsLBox.select_clear(self.levelsLBox.curselection())
					self.levelsLBox.selection_set(t)
					self.controller.update()
					self.update()
				elif e.keysym == '??':
					pass
				else:
					return
			except:
				pass

			self.editFrame.grid_forget()
			self.lastLevel = self.levelsLBox.get(self.levelsLBox.curselection())
			self.entriesLBox.delete(0, tk.END)
			for n,i in enumerate(self.deckLevels[self.lastDeck][self.lastLevel]):
				self.entriesLBox.insert(tk.END, "{}: {}".format(i[0],i[1]).replace("commaChar", ","))
				for j in self.changes:
					j = j.split(",")
					if i[10] == j[10]:
						self.entriesLBox.delete(n,tk.END)
						self.entriesLBox.insert(tk.END, "{}: {}".format(j[0],j[1]).replace("commaChar", ","))

			self.createEditLevelWidgets(self.editFrame, self.lastDeck, self.lastLevel)
			self.editFrame.grid(column = 0, row = 1, columnspan = 9999, sticky = 'n')

	def entriesLBoxSelect(self, e):
		if not self.entriesLBox.curselection() == ():
			try:
				if e.keysym == 'Down':
					if self.entriesLBox.curselection()[0] < self.entriesLBox.size() -1:
						t = self.entriesLBox.curselection()[0] + 1 
					else: 
						return
					self.entriesLBox.select_clear(self.entriesLBox.curselection())
					self.entriesLBox.selection_set(t)
					self.controller.update()
					self.update()
				elif e.keysym == 'Up':
					if self.entriesLBox.curselection()[0] > 0:
						t = self.entriesLBox.curselection()[0] - 1 
					else: 
						return
					self.entriesLBox.select_clear(self.entriesLBox.curselection())
					self.entriesLBox.selection_set(t)
					self.controller.controller.update()
					self.update()
				elif e.keysym == '??':
					pass
				else:
					return
			except:
				pass

			sel = self.entriesLBox.get(self.entriesLBox.curselection()).split(": ")
			for j in self.deckLevels[self.lastDeck][self.lastLevel]:
				 if self.loadSel(j, sel):
				 	break
						
	def loadSel(self, j, sel):
		# DecksAndLevelsFuncs.loadSel(self, j, sel)
		for k in self.changes:
			k = k.split(",")	
			if sel[0].replace(",","commaChar") in k and sel[1].replace(",","commaChar") in k:
				self.line = k
				self.createEditFrameWidgets(self.editFrame, self.line)
				self.editFrame.grid(column = 0, row = 1, columnspan = 9999, sticky = 'n')
				return True
			if sel[0].replace(",","commaChar") in j and sel[1].replace(",","commaChar") in j:
				self.line = j
				self.createEditFrameWidgets(self.editFrame, self.line)
				self.editFrame.grid(column = 0, row = 1, columnspan = 9999, sticky = 'n')
				return False

	def goMainMenu(self):
		# DecksAndLevelsFuncs.goMainMenu(self)
		if len(self.changes) > 1:
			mycsv.write(mstr = self.changes, lesson = True)
			self.controller.controller.doValues()
		self.controller.controller.show_frame("Mainmenu")

	def createEditDeckWidgets(self, frame, deck):
		for w in frame.winfo_children():
			w.destroy()

		self.deckNameLabel = tk.Label(frame, text = "Deck Name")
		self.deckNameLabel.grid(row = 0, column = 0)

		self.deckNameEntry = rusEntry.Entry(frame, width = 50)
		self.deckNameEntry.insert(0, deck)
		self.deckNameEntry.grid(row = 0, column = 1)

		self.saveButton = tk.Button(frame, text = "Save", command = lambda: self.saveEditsDeck(deck))
		self.saveButton.grid(row = 0, column = 2)

		self.totalLevelsLabel = tk.Label(frame, text = "Total Levels")
		self.totalLevelsLabel.grid(row = 1, column = 0)

		self.totalLevelsLabel2 = tk.Label(frame, text = len(self.deckLevels[deck]))
		self.totalLevelsLabel2.grid(row = 1, column = 1)

		self.totalEntriesLabel = tk.Label(frame, text = "Total entries")
		self.totalEntriesLabel.grid(row = 2, column = 0)
		tc = 0
		d = self.deckLevels[deck]
		for e in d:
			tc += len(d[e])
		self.totalLevelsLabel2 = tk.Label(frame, text = tc )
		self.totalLevelsLabel2.grid(row = 2, column = 1)

		self.deleteDeckButton = tk.Button(frame, text = "Delete deck", command = lambda: self.deleteDeck(deck))
		self.deleteDeckButton.grid(column = 0, columnspan = 2)

	def deleteDeck(self, deck):
		mycsv.clearlines(mstr = deck, option = 11)
		for w in self.winfo_children():
			w.destroy()
		self.controller.controller.doValues()
		self.deckLevels = self.controller.controller.dandl
		self.createWidgets()

	def saveEditsDeck(self, origDeckName):
		newDeckName = self.deckNameEntry.get()
		mycsv.write(mstr = (origDeckName, newDeckName), option = 11)

		for w in self.winfo_children():
			w.destroy()
		self.controller.controller.doValues()
		self.deckLevels = self.controller.controller.dandl
		self.createWidgets()
		for n,i in enumerate(self.decksLBox.get(0, tk.END)):
			if i == newDeckName:
				self.decksLBox.selection_set(n)
				self.decksLBoxSelect(None)
		
	def createEditLevelWidgets(self, frame, deck, level):
		for w in frame.winfo_children():
			w.destroy()

		self.levelNameLabel = tk.Label(frame, text = "Deck Name")
		self.levelNameLabel.grid(row = 0, column = 0)

		self.levelNameLabel2 = tk.Label(frame, text = level)
		self.levelNameLabel2.grid(row = 0, column = 1)

		self.totalEntriesLabel = tk.Label(frame, text = "Total Entries")
		self.totalEntriesLabel.grid(row = 1, column = 0)

		self.totalEntriesLabel2 = tk.Label(frame, text = len(self.deckLevels[deck][level]))
		self.totalEntriesLabel2.grid(row = 1, column = 1)

		self.ignoreAllLabel = tk.Label(frame, text = "Ignore level?")
		self.ignoreAllLabel.grid(row = 2, column = 0)

		self.v = tk.StringVar()
		self.ignoreAllCheckbutton = tk.Checkbutton(frame, command = lambda: self.ignoreAll(deck, level, self.v.get()), variable = self.v, onvalue = "yes", offvalue = "no")
		self.ignoreAllCheckbutton.grid(row= 2, column = 2)
		for j in self.deckLevels[deck][level]:
			if j[13] == "no":
				self.ignoreAllCheckbutton.deselect()
				break
			else:
				self.ignoreAllCheckbutton.select()

		self.deleteLevelButton = tk.Button(frame, text = "Delete level", command = lambda: self.deleteLevel(deck, level))
		self.deleteLevelButton.grid(row = 3, column = 0, columnspan = 2)

	def deleteLevel(self, deck, level):
		mycsv.clearlines(mstr = (deck,level), option = (11,12))
		for w in self.winfo_children():
			w.destroy()
		self.controller.controller.doValues()
		self.deckLevels = self.controller.controller.dandl
		self.createWidgets()

	def ignoreAll(self, deck, level, val):
		mycsv.write(mstr = val, row = (deck, level), option = 13)

	def createEditFrameWidgets(self, frame, line, search = False):
		self.labels = []
		self.entries = []

		for w in frame.winfo_children():
			w.destroy()

		self.textLabel = tk.Label(frame, text = "Entry")
		self.labels.append(self.textLabel)

		self.textEntry = rusEntry.Entry(frame)
		self.entries.append(self.textEntry)

		self.transLabel = tk.Label(frame, text = "Translation")
		self.labels.append(self.transLabel)

		self.transEntry = rusEntry.Entry(frame)
		self.entries.append(self.transEntry)

		self.tagsLabel = tk.Label(frame, text = "Tags")
		self.labels.append(self.tagsLabel)

		self.tagsEntry = tk.Entry(frame)
		self.entries.append(self.tagsEntry)

		self.learnedLabel = tk.Label(frame, text = "Learned")
		self.labels.append(self.learnedLabel)

		self.learnedEntry = tk.Label(frame, text = "-")
		self.entries.append(self.learnedEntry)

		self.attemptsLabel = tk.Label(frame, text = "Attmpts")
		self.labels.append(self.attemptsLabel)

		self.attemptsEntry = tk.Label(frame, text = "-")
		self.entries.append(self.attemptsEntry)

		self.successfulAttemptsLabel = tk.Label(frame, text = "Successful attempts")
		self.labels.append(self.successfulAttemptsLabel)

		self.successfulAttemptsEntry = tk.Label(frame, text = "-")
		self.entries.append(self.successfulAttemptsEntry)

		self.dayLastAttemptLabel = tk.Label(frame, text = "Day of last attempt")
		self.labels.append(self.dayLastAttemptLabel)

		self.dayLastAttemptEntry = tk.Label(frame, text = "-")
		self.entries.append(self.dayLastAttemptEntry)

		self.lastAttemptResultLabel = tk.Label(frame, text = "Result of last attempt")
		self.labels.append(self.lastAttemptResultLabel)

		self.lastAttemptResultEntry = tk.Label(frame, text = "-")
		self.entries.append(self.lastAttemptResultEntry)

		self.dayToReviewLabel = tk.Label(frame, text = "Day of next review")
		self.labels.append(self.dayToReviewLabel)

		self.dayToReviewEntry = tk.Label(frame, text = "-")
		self.entries.append(self.dayToReviewEntry)

		self.attemptStreakLabel = tk.Label(frame, text = "Attempt streak")
		self.labels.append(self.attemptStreakLabel)

		self.attemptStreakEntry = tk.Label(frame, text = "-")
		self.entries.append(self.attemptStreakEntry)

		self.idLabel = tk.Label(frame, text = "ID")
		self.labels.append(self.idLabel)

		self.idLabel2 = tk.Label(frame, text = "-")
		self.entries.append(self.idLabel2)

		self.deckLabel = tk.Label(frame, text = "Deck")
		self.labels.append(self.deckLabel)

		self.deckEntry = tk.Entry(frame)
		self.entries.append(self.deckEntry)

		self.levelLabel = tk.Label(frame, text = "Level")
		self.labels.append(self.levelLabel)

		self.levelEntry = tk.Entry(frame)
		self.entries.append(self.levelEntry)

		self.ignoreLabel = tk.Label(frame, text = "Ignore")
		self.labels.append(self.ignoreLabel)

		self.ignoreEntry = tk.Label(frame, text = "-")
		self.entries.append(self.ignoreEntry)

		self.langLabel = tk.Label(frame, text = "Language")
		self.labels.append(self.langLabel)

		self.langEntry = tk.Entry(frame)
		self.entries.append(self.langEntry)

		for n,w in enumerate(self.labels):
			w.grid(row = n, column = 1)
		for n,w in enumerate(self.entries):
			w.grid(row = n, column = 2)
			if w['text'] == "-":
				w['text'] = line[n]
			else:
				w.insert(0, line[n].replace("commaChar", ","))
			w['width'] = 55

		if self.ignoreEntry['text'] == "no":
			self.ignoreCheck = tk.Checkbutton(frame, command = self.ignoreCheckFunc)
			self.ignoreCheck.grid(column = 3, row = 13)
		else:
			self.ignoreCheck = tk.Checkbutton(frame, command = self.ignoreCheckFunc)
			self.ignoreCheck.grid(column = 3, row = 13)
			self.ignoreCheck.toggle()
		
		self.listenButton = tk.Button(frame, text = "Listen", command = self.listen)
		self.listenButton.grid(column = 3, row = 0)
		
		if not search:
			self.saveButton = tk.Button(frame, text = "Save", command = self.saveEdits)
			self.saveButton.grid(column = 1, columnspan = 2)
		else:
			self.saveButton = tk.Button(frame, text = "Save", command = self.saveEditsSearch)
			self.saveButton.grid(column = 1, columnspan = 2)

		self.deleteEntryButton = tk.Button(frame, text = "Delete entry", command = lambda: self.deleteEntry(line[10]))
		self.deleteEntryButton.grid(row  = 15, column = 3, columnspan = 2)

	def deleteEntry(self, ID):
		mycsv.clearlines(mstr = ID, option = 10)
		for w in self.winfo_children():
			w.destroy()
		self.controller.controller.doValues()
		self.deckLevels = self.controller.controller.dandl
		self.createWidgets()

	def ignoreCheckFunc(self):
		if self.ignoreEntry['text'] == "no":
			self.ignoreEntry['text'] = "yes"
		else:
			self.ignoreEntry['text'] ="no"

	def saveEdits(self):
		newline = []
		for n,w in enumerate(self.entries):
			try:
				newline.append(w.get().replace(",", "commaChar"))
			except:
				newline.append(w['text'])
		self.changes.append(','.join(newline))
		lsel = self.entriesLBox.curselection()
		for n,i in enumerate(self.levelsLBox.get(0, tk.END)):
			if i == self.levelsLBox.get(self.levelsLBox.curselection()):
				self.levelsLBox.selection_set(n)
				self.levelsLBoxSelect(None)
		self.entriesLBox.selection_set(lsel)
		self.entriesLBoxSelect(None)

	def listen(self):
		audio.preload(self.line)
		audio.startAudio()
		audio.play(self.line)
		audio.endAudio()