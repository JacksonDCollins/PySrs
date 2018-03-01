import tkinter as tk
import tkinter.ttk as ttk
import helpLibs.srs as srs
import helpLibs.audio as audio
import helpLibs.consts as consts

class Mainmenu(tk.Frame):
	def __init__(self, master, controller, *args):
		tk.Frame.__init__(self, master)
		self.grid()
		self.controller = controller
		self.size = "800x500"
		if consts.defaultLang():
			self.curlang = consts.defaultLang()
		else:
			if not self.controller.langs == {}:
				self.curlang = [self.controller.langs[x] for x in self.controller.langs][len(self.controller.langs) -1]
			else:
				self.controller.langs = {'none': 'None'}
				self.curlang = [self.controller.langs[x] for x in self.controller.langs][len(self.controller.langs) -1]
		self.bind("<<ShowFrame>>", self.on_show_frame)
		self.createWidgets()
		
	def createWidgets(self):
		self.reviewButton = tk.Button(self, text = "Review: {}".format(len(self.controller.toReview)), command = self.reviewLesson)
		self.reviewButton.grid(row = 0, column = 1)
		if len(self.controller.toReview) == 0:
			self.reviewButton['state'] = tk.DISABLED

		# self.toReviewLabel = tk.Label(self, text = "Review: {}".format(len(self.controller.toReview)))
		# self.toReviewLabel.grid(row = 0, column = 2)	

		self.buttonDecksAndLevels = tk.Button(self, text = "Decks and Levels", command = self.DecksAndLevels)
		self.buttonDecksAndLevels.grid(row = 1, column = 1)
		
		self.analyticsButton = tk.Button(self, text = "Analytics", command = self.Analytics)
		self.analyticsButton.grid(row = 0, column = 2)

		self.settingsButton = tk.Button(self, text = "Settings", command = self.Settings)
		self.settingsButton.grid(row = 1, column = 2)

		self.langSelectCBoxString = tk.StringVar()
		self.langSelectCBoxString.set(self.curlang)
		self.langSelectCBox = ttk.Combobox(self, values = [self.controller.langs[x] for x in self.controller.langs], validate = 'all', validatecommand = self.chooseLang, state = 'readonly', textvariable = self.langSelectCBoxString, exportselection=0)
		self.langSelectCBox.grid(row = 3, column = 1, columnspan = 999)

		self.dlLabel = tk.Label(self, text = '')
		self.dlLabel.grid(row = 4, column = 1, columnspan = 999)

		self.panes = [] 
		self.panesFrame = VerticalScrolledFrame(self)
		self.panesFrame.grid(row = 0, column = 0, rowspan = 9999)

		for n,i in enumerate([x for x in self.controller.dandl if self.controller.deckLangs[x] == self.curlang]):
			self.panes.append(tk.PanedWindow(self.panesFrame.interior, orient = tk.VERTICAL, relief = 'groove', borderwidth = 2, width = 500))
			self.panes[n].add(DeckEntry(self, i, self.controller.reviewCounts[i], self.controller.learnCounts[i], self.controller.totalCounts[i]), pady = 5)
		for pane in self.panes:
			pane.grid(columnspan = 3, pady = 5)

	def chooseLang(self):
		if not self.langSelectCBoxString.get() == self.curlang:
			self.curlang = self.langSelectCBoxString.get()
			self.langSelectCBoxString.set(self.curlang)
			self.langSelectCBox['values'] = [self.controller.langs[x] for x in self.controller.langs]
			self.on_show_frame(None)
		return True

	def on_show_frame(self, event):
		for widget in self.winfo_children():
			widget.destroy()
		self.controller.geometry(self.size)
		self.createWidgets()

	def DecksAndLevels(self):
		self.controller.show_frame("DAndLgui", me = self)

	def reviewLesson(self):
		self.controller.r = srs.setupNewLesson(deck = self.controller.deck)
		for n,i in enumerate(self.controller.r):
			self.dlLabel['text'] = "Gathering files: {}/{}".format(n+1,len(self.controller.r))
			self.controller.update()
			audio.preload(i.split(','))
		self.controller.show_frame("reviewLesson", me = self)

	def Analytics(self):
		self.controller.show_frame("Analytics", me = self)

	def learnLesson(self):
		print('1',self.controller.r)
		self.controller.r = srs.setupNewLesson(deck = self.controller.deck, review = False)
		print(self.controller.r)
		for n,i in enumerate(self.controller.r):
			self.dlLabel['text'] = "Gathering files: {}/{}".format(n+1,len(self.controller.r))
			self.controller.update()
			audio.preload(i.split(','))
		self.controller.show_frame("learnLesson", me = self)

	def Settings(self):
		self.controller.show_frame("Settings", me = self)


class VerticalScrolledFrame(tk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set, height = 500)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

class DeckEntry(tk.Frame):
	def __init__(self, master, *args):
		tk.Frame.__init__(self, master)
		self.deck = args[0]
		self.deckName = tk.Label(self, text = "{}".format(args[0]), width = 50)
		self.deckName.grid(row = 0, column = 0)

		self.reviewButton = tk.Button(self, text = "Review: {}".format(args[1]), command = self.doReview, width = 15)
		self.reviewButton.grid(row = 0, column = 1)
		if args[1] == 0:
			self.reviewButton['state'] = tk.DISABLED

		self.toLearn = tk.Label(self, text = "{}/{} words learned".format(args[3] - args[2], args[3]))
		self.toLearn.grid(row = 1, column = 0)

		self.pbcont = tk.IntVar()
		self.progBar = ttk.Progressbar(self, maximum = args[3], mode = 'determinate', orient = tk.HORIZONTAL, length = 475, variable = self.pbcont)
		self.progBar.grid(row = 2, column = 0, columnspan = 2, sticky = 'nw')
		if args[3] - args[2] == args[3]:
			self.progBar.grid_forget()
		else:
			self.pbcont.set(args[3] - args[2])
			self.learnButton = tk.Button(self, text = "Learn", command = self.doLearn, width = 15)
			self.learnButton.grid(row = 1, column = 1, pady = 5)

	def doReview(self):
		self.master.controller.r = srs.setupNewLesson(deck = self.deck)
		for n,i in enumerate(self.master.controller.r):
			self.master.dlLabel['text'] = "Gathering files: {}/{}".format(n+1,len(self.master.controller.r))
			self.master.controller.update()
			audio.preload(i.split(','))
		self.master.controller.show_frame("reviewLesson", me = self)

		#self.master.controller.show_frame("reviewLesson", deck = self.deck)
		#self.master.controller.event_generate("<<ShowFrame>>")
		return True

	def doLearn(self):
		self.master.controller.r = srs.setupNewLesson(deck = self.deck, review = False)
		for n,i in enumerate(self.master.controller.r):
			self.master.dlLabel['text'] = "Gathering files: {}/{}".format(n+1,len(self.master.controller.r))
			self.master.controller.update()
			audio.preload(i.split(','))
		self.master.controller.show_frame("learnLesson", me = self)

		#self.master.controller.show_frame("learnLesson", deck = self.deck)
		#self.master.controller.event_generate("<<ShowFrame>>")
		return True