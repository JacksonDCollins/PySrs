import tkinter as tk
import tkinter.ttk as ttk
import guiLibs.rusEntry as rusEntry

class AddDeckOrLevel(tk.Toplevel):
	def __init__(self, master, mtype):
		tk.Toplevel.__init__(self, master)
		self.controller = master
		self.type = mtype
		self.name = None
		self.submitted = False
		self.geometry("300x100")
		self.protocol("WM_DELETE_WINDOW", self.sendNameClose)
		self.createWidgets()

	def createWidgets(self):
		self.titleLabel = tk.Label(self, text = "Enter {} name".format(self.type))
		self.titleLabel.pack()

		self.deckNameEntry = rusEntry.Entry(self)
		self.deckNameEntry.pack()

		self.addDeckButton = tk.Button(self, text = "Add", command = self.sendName)
		self.addDeckButton.pack()

	def sendName(self):
		self.name = self.deckNameEntry.get()
		if not self.name == "":
			self.submitted = True

	def sendNameClose(self):
		self.name = None
		self.submitted = True