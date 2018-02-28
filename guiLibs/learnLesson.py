import tkinter as tk
import tkinter.ttk as ttk
import helpLibs.srs as srs
import helpLibs.audio as audio
import guiLibs.editEntry as editEntry
import guiLibs.rusEntry as rusEntry

class learnLesson(tk.Frame):
	def __init__(self, master, controller):
		tk.Frame.__init__(self, master)
		self.grid()
		self.line = None
		self.lineEdited = False
		self.controller = controller
		self.size = "1255x300"
		self.submit = False
		self.editEntrytl = None
		self.bind("<<ShowFrame>>", self.on_show_frame)

	def createWidgets(self):
		self.confirmButton = tk.Button(self, text = "Submit", command = self.submitAnswer)
		self.confirmButton.grid(row = 4, column = 0, columnspan = 2)
		
		self.label = tk.Label(self, text = "", font = (lambda x: self.cget('font'), 32), width = 50, wraplength = 1000)
		self.label.grid(row = 1, column = 0, columnspan = 2, rowspan = 2)

		self.tagsLabel = tk.Label(self, text = "", font =(lambda x: self.cget('font'), 12))
		self.tagsLabel.grid(row = 3, column = 0, columnspan = 2, rowspan = 1)

		self.exitButton = tk.Button(self, text = "Exit", font = (lambda x: self.cget('font'), 32), command = self.goMainMenu)
		self.exitButton.grid(row = 1, column = 1, sticky = 'ne')

		self.answerEntry = rusEntry.Entry(self, font = (lambda x: self.cget('font'), 32))
		self.answerEntry.grid(row = 5, column = 0, columnspan = 2)
		self.answerEntry.bind('<Return>', lambda x: self.submitAnswer())

		self.editButton = tk.Button(self, text = "Edit", command =  lambda: self.editEntry(self.line))
		self.editButton.grid(row = 6, column = 0, columnspan = 2)

		self.pbcont = tk.IntVar()
		self.progBar = ttk.Progressbar(self, maximum = 6, mode = 'determinate', orient = tk.HORIZONTAL, length = 200, variable = self.pbcont)
		self.progBar.grid(row = 1, column = 0, sticky = 'nw')

	def submitAnswer(self):
		self.submit = True
		self.update()

	def learn(self, deck):
		#r = srs.setupNewLesson(deck = deck, review = False)
		#print(self.controller.r)
		try:
			audio.startAudio()
			srs.doLearnLesson(self.controller.r, self, tWidget = self.label, eWidget = self.answerEntry, tagsWidget = self.tagsLabel, cWidget = self.pbcont)
			audio.endAudio()
			self.controller.doValues()
			self.goMainMenu()
		except Exception as e:
			print(e)
			self.goMainMenu()

	def on_show_frame(self, event):
		for widget in self.winfo_children():
			widget.destroy()
		self.controller.geometry(self.size)
		self.createWidgets()
		self.learn(self.controller.deck)

	def editEntry(self, test):
		self.editEntrytl = editEntry.editEntry(self, test)

	def goMainMenu(self):
		try:
			self.editEntrytl.destroy()
		except:
			pass

		self.controller.show_frame("Mainmenu", me = self)