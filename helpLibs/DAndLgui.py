import tkinter as tk
import tkinter.ttk as ttk
import guiLibs.newSearch as newSearch
import guiLibs.newCards as newCards
import guiLibs.DecksAndLevels as DecksAndLevels

class DAndLgui(tk.Frame):
	def __init__(self, master, controller):
		tk.Frame.__init__(self, master)
		self.frames = {}
		self.controller = controller
		self.bind("<<ShowFrame>>", self.on_show_frame)
		container = tk.Frame(self)
		container.grid()
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		for F in (DecksAndLevels.DecksAndLevels, newSearch.newSearch, newCards.newCards):
			page_name = F.__name__
			frame = F(container, self)
			self.frames[page_name] = frame

			# put all of the pages in the same location;
			# the one on the top of the stacking order
			# will be the one that is visible.
			frame.grid(row=0, column=0, sticky="nsew")

	def show_frame(self, page_name, me = None, *args):
		'''Show a frame for the given page name'''
		if me:
			for widget in me.winfo_children():
				widget.destroy()
		if len(args):
			self.deck = args[0]
		frame = self.frames[page_name]
		frame.tkraise()
		frame.event_generate("<<ShowFrame>>")

	def on_show_frame(self, event):
		self.show_frame("DecksAndLevels")