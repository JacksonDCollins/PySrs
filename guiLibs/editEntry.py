import tkinter as tk
import tkinter.ttk as ttk
import guiLibs.rusEntry as rusEntry

class editEntry(tk.Toplevel):
	def __init__(self, master, line):
		tk.Toplevel.__init__(self, master)
		self.geometry("500x500")
		self.master = master
		self.createWidgets()

	def createWidgets(self):
		self.labels = []
		self.entries = []

		self.textLabel = tk.Label(self, text = "Entry")
		self.labels.append(self.textLabel)

		self.textEntry = rusEntry.Entry(self)
		self.entries.append(self.textEntry)

		self.transLabel = tk.Label(self, text = "Translation")
		self.labels.append(self.transLabel)

		self.transEntry = rusEntry.Entry(self)
		self.entries.append(self.transEntry)

		self.tagsLabel = tk.Label(self, text = "Tags")
		self.labels.append(self.tagsLabel)

		self.tagsEntry = tk.Entry(self)
		self.entries.append(self.tagsEntry)

		self.learnedLabel = tk.Label(self, text = "Learned")
		self.labels.append(self.learnedLabel)

		self.learnedEntry = tk.Label(self, text = "-")
		self.entries.append(self.learnedEntry)

		self.attemptsLabel = tk.Label(self, text = "Attmpts")
		self.labels.append(self.attemptsLabel)

		self.attemptsEntry = tk.Label(self, text = "-")
		self.entries.append(self.attemptsEntry)

		self.successfulAttemptsLabel = tk.Label(self, text = "Successful attempts")
		self.labels.append(self.successfulAttemptsLabel)

		self.successfulAttemptsEntry = tk.Label(self, text = "-")
		self.entries.append(self.successfulAttemptsEntry)

		self.dayLastAttemptLabel = tk.Label(self, text = "Day of last attempt")
		self.labels.append(self.dayLastAttemptLabel)

		self.dayLastAttemptEntry = tk.Label(self, text = "-")
		self.entries.append(self.dayLastAttemptEntry)

		self.lastAttemptResultLabel = tk.Label(self, text = "Result of last attempt")
		self.labels.append(self.lastAttemptResultLabel)

		self.lastAttemptResultEntry = tk.Label(self, text = "-")
		self.entries.append(self.lastAttemptResultEntry)

		self.dayToReviewLabel = tk.Label(self, text = "Day of next review")
		self.labels.append(self.dayToReviewLabel)

		self.dayToReviewEntry = tk.Label(self, text = "-")
		self.entries.append(self.dayToReviewEntry)

		self.attemptStreakLabel = tk.Label(self, text = "Attempt streak")
		self.labels.append(self.attemptStreakLabel)

		self.attemptStreakEntry = tk.Label(self, text = "-")
		self.entries.append(self.attemptStreakEntry)

		self.idLabel = tk.Label(self, text = "ID")
		self.labels.append(self.idLabel)

		self.idLabel2 = tk.Label(self, text = "-")
		self.entries.append(self.idLabel2)

		self.deckLabel = tk.Label(self, text = "Deck")
		self.labels.append(self.deckLabel)

		self.deckEntry = tk.Entry(self)
		self.entries.append(self.deckEntry)

		self.levelLabel = tk.Label(self, text = "Level")
		self.labels.append(self.levelLabel)

		self.levelEntry = tk.Entry(self)
		self.entries.append(self.levelEntry)

		self.ignoreLabel = tk.Label(self, text = "Ignore")
		self.labels.append(self.ignoreLabel)

		self.ignoreEntry = tk.Label(self, text = "-")
		self.entries.append(self.ignoreEntry)

		self.langLabel = tk.Label(self, text = "Language")
		self.labels.append(self.langLabel)

		self.langEntry = tk.Entry(self)
		self.entries.append(self.langEntry)

		for n,w in enumerate(self.labels):
			w.grid(row = n, column = 1)
		for n,w in enumerate(self.entries):
			w.grid(row = n, column = 2, sticky = 'w', columnspan = 999)
			w['width'] = 55
			if w == self.ignoreEntry:
				w['width'] = 50

			if w['text'] == "-":
				w['text'] = self.master.line[n]
			else:
				w.insert(0, self.master.line[n].replace("commaChar", ","))

		self.ignoreCheck = tk.Checkbutton(self, command = self.ignoreCheckFunc)
		self.ignoreCheck.grid(column = 875, row = 13, sticky = 'e')
		if self.ignoreEntry['text'] == "yes":
			self.ignoreCheck.select()
		else:
			self.ignoreCheck.deselect()

		self.saveButton = tk.Button(self, text = "Save", command = self.saveEdits)
		self.saveButton.grid(column = 0, columnspan = 2)

	def ignoreCheckFunc(self):
		if self.ignoreEntry['text'] == "no":
			self.ignoreEntry['text'] =  "yes"
		else:
			self.ignoreEntry['text'] = "no"

	def saveEdits(self):
		self.master.lineEdited = True
		for n,w in enumerate(self.entries):
			try:
				self.master.line[n] = w.get().replace(",", "commaChar")
			except:
				self.master.line[n] = w['text']