import tkinter as tk
import tkinter.filedialog as filedialog
import helpLibs.consts as consts
import configparser

class Settings(tk.Frame):
	def __init__(self, master, controller):
		tk.Frame.__init__(self, master)
		self.grid()
		self.controller = controller
		self.size = "800x500"		
		self.bind("<<ShowFrame>>", self.on_show_frame)
		self.createWidgets()

	def createWidgets(self):
		# [GENERAL]
		# cwd = C:\Users\Jc\Desktop\srs rus
		# month = 30
		# workdoc = C:\Users\Jc\Desktop\srs rus\sentences.csv
		# hwdoc = \history.csv
		# fname = data
		# backups = C:\Users\Jc\Desktop\srs rus\backups\
		# newperlesson = 5
		# reviewperlesson = 25

		self.cwdLabel = tk.Label(self, text = "Current working directory:")
		self.cwdLabel.grid(row = 0, column = 0)
		self.cwdEntry = tk.Label(self, text = consts.cwd())
		self.cwdEntry.grid(row = 0, column = 1)
		def f(self): mdir = filedialog.askdirectory(initialdir = self.cwdEntry['text']).replace("/","\\"); self.cwdEntry['text'] = mdir if mdir else consts.cwd(); self.checkChanges()
		self.cwdBrowser = tk.Button(self, text = "Change directory", command = lambda: f(self))
		self.cwdBrowser.grid(row = 0, column=2)

		self.workdocLabel = tk.Label(self, text = "Current workdoc:")
		self.workdocLabel.grid(row = 1, column = 0)
		self.workdocEntry = tk.Label(self, text = consts.workdoc())
		self.workdocEntry.grid(row = 1, column = 1)
		def k(self): mdir = filedialog.askopenfilename(initialfile = self.workdocEntry['text'], filetypes = (('csv files','*.csv'),)).replace("/","\\"); self.workdocEntry['text'] = mdir if mdir else consts.workdoc(); self.checkChanges()
		self.workdocBrowser = tk.Button(self, text = "Change file", command = lambda: k(self))
		self.workdocBrowser.grid(row = 1, column=2)

		self.monthLabel = tk.Label(self, text = "Month:")
		self.monthLabel.grid(row = 2, column = 0)
		self.monthEntry = tk.Entry(self, validate = 'key', validatecommand = (self.register(lambda x: x.isdigit()), '%S'))
		self.monthEntry.insert(tk.END, consts.month())
		self.monthEntry.grid(row = 2, column = 1)


		# self.hwdocLabel = tk.Label(self, text = "Current hwdoc:")
		# self.hwdocLabel.grid(row = 3, column = 0)
		# self.hwdocEntry = tk.Label(self, text = consts.hwdoc())
		# self.hwdocEntry.grid(row = 3, column = 1)


		# self.fnameLabel = tk.Label(self, text = "Current fname:")
		# self.fnameLabel.grid(row = 4, column = 0)
		# self.fnameEntry = tk.Label(self, text = consts.fname())
		# self.fnameEntry.grid(row = 4, column = 1)


		# self.backupsLabel = tk.Label(self, text = "Current backups directory:")
		# self.backupsLabel.grid(row = 5, column = 0)
		# self.backupsEntry = tk.Label(self, text = consts.backups())
		# self.backupsEntry.grid(row = 5, column = 1)


		self.newPerLessonLabel = tk.Label(self, text = "Current newPerLesson:")
		self.newPerLessonLabel.grid(row = 6, column = 0)
		self.newPerLessonEntry = tk.Entry(self, validate = 'key', validatecommand = (self.register(lambda x: x.isdigit()), '%S'))
		self.newPerLessonEntry.insert(tk.END, consts.newPerLesson())
		self.newPerLessonEntry.grid(row = 6, column = 1)


		self.reviewPerlessonLabel = tk.Label(self, text = "Current reviewPerLesson:")
		self.reviewPerlessonLabel.grid(row = 7, column = 0)
		self.reviewPerlessonEntry = tk.Entry(self, validate = 'key', validatecommand = (self.register(lambda x: x.isdigit()), '%S'))
		self.reviewPerlessonEntry.insert(tk.END, consts.reviewPerLesson())
		self.reviewPerlessonEntry.grid(row = 7, column = 1)


		self.buttonGoBack = tk.Button(self, text = "Go Back", command = self.goMainMenu)
		self.buttonGoBack.grid(row = 0, column=3)

		self.saveButton = tk.Button(self, text = "Save changes", command = self.saveChanges, state = tk.DISABLED)
		self.saveButton.grid(row = 8, columnspan = 2)

		for w in self.winfo_children():
			if isinstance(w, tk.Entry):
				w.bind('<Key>', lambda x: self.after(0, self.checkChanges))

	def checkChanges(self):
		if self.monthEntry.get() == str(consts.month()) and self.newPerLessonEntry.get() == str(consts.newPerLesson()) and self.reviewPerlessonEntry.get() == str(consts.reviewPerLesson()) and self.workdocEntry['text'] == consts.workdoc() and self.cwdEntry['text'] == consts.cwd():
			self.saveButton['state'] = tk.DISABLED
		else:
			self.saveButton['state'] = tk.ACTIVE

	def saveChanges(self):
		config = configparser.ConfigParser()
		config.read(consts.confile)

		config['GENERAL']['month'] = self.monthEntry.get()
		config['GENERAL']['newPerLesson'] = self.newPerLessonEntry.get()
		config['GENERAL']['reviewPerLesson'] = self.reviewPerlessonEntry.get()

		with open(consts.confile, 'w') as c:
			config.write(c)

		self.checkChanges()
	
	def on_show_frame(self, event):
		for widget in self.winfo_children():
			widget.destroy()
		self.controller.geometry(self.size)
		self.createWidgets()

	def goMainMenu(self):
		self.controller.show_frame("Mainmenu", me = self)
		