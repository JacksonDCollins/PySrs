import tkinter as tk
import helpLibs.memrise as memrise
import threading
import requests
from PIL import Image, ImageTk
from io import BytesIO
import queue

def doTWork(self, func, args = {}, kwargs = {}, after = None, daemon = False):
	t = threading.Thread(target = func, args = args, kwargs = kwargs)
	t.daemon = daemon
	t.start()
	if not daemon:
		while t.isAlive():
			self.update()
	if after: after()

class browseFromMemrise(tk.Toplevel):
	def __init__(self, master):
		tk.Toplevel.__init__(self, master)
		self.controller = master
		self.name = None
		self.newCourse = None
		self.submitted = None
		#self.browser = memrise.CourseBrowser()
		self.geometry("800x600")
		self.protocol("WM_DELETE_WINDOW", self.sendNameClose)
		self.createWidgets()
		self.populate()

	def createWidgets(self):
		self.langsLBoxDict = {}
		self.langsLBox = tk.Listbox(self, exportselection = 0, selectmode = tk.BROWSE, activestyle = 'none')
		self.langsLBox.grid()
		
		self.langsLBoxDict2 = {}
		self.langsLBox2 = tk.Listbox(self, exportselection = 0, selectmode = tk.BROWSE, activestyle = 'none')
		self.langsLBox2.grid()

		self.langsLBoxDict3 = {}
		self.langsLBox3 = tk.Listbox(self, exportselection = 0, selectmode = tk.BROWSE, activestyle = 'none')
		self.langsLBox3.grid()

		self.loadMoreButton = tk.Button(self, text ='Load more', command = self.loadMoreFunc)
		self.loadMoreButton.grid()

		self.loadingLabel = tk.Label(self, text = 'Ready')
		self.loadingLabel.grid()

		self.coursesHolder = VerticalScrolledFrame(self, width = 650)
		self.coursesHolder.grid(row = 0, column = 1, rowspan = 9999)

		for i in self.winfo_children():
			if isinstance(i,tk.Listbox):
				i.bind('<<ListboxSelect>>', self.lBoxSelect)

	def t(self): self.browser.loadMore()
	def loadMoreFunc(self):
		self.loadingLabel['text'] = 'Loading'
		doTWork(self, self.t, after = self.showCourses)
		self.loadingLabel['text'] = 'Ready'

	def k(self): self.browser = memrise.CourseBrowser()	
	def populate(self):
		self.loadingLabel['text'] = 'Loading'
		doTWork(self, self.k)
		for i in self.browser.allCat:
			self.langsLBoxDict[i.text.strip()] = i
			self.langsLBox.insert(tk.END, i.text.strip())
		self.loadingLabel['text'] = 'Ready'

	def p(self, b): self.browser.loadCourses(b)
	def lBoxSelect(self,e):
		if e.widget == self.langsLBox:
			l = self.langsLBoxDict[self.langsLBox.get(tk.ANCHOR)]
			self.langsLBox2.delete(0,tk.END)
			self.langsLBoxDict2 = {}
			for i in self.browser.allCat[l]:
				self.langsLBoxDict2[i.text.strip()] = i
				self.langsLBox2.insert(tk.END, i.text.strip())

		if e.widget == self.langsLBox2:
			l = self.langsLBoxDict[self.langsLBox.get(tk.ANCHOR)]
			l2 = self.langsLBoxDict2[self.langsLBox2.get(tk.ANCHOR)]
			self.langsLBox3.delete(0, tk.END)
			self.langsLBoxDict3 = {}
			if len(self.browser.allCat[l][l2]) > 0:
				for i in self.browser.allCat[l][l2]:
					self.langsLBoxDict3[i.text.strip()] = i
					self.langsLBox3.insert(tk.END, i.text.strip())
			else:
				l2 = self.langsLBox2.get(tk.ANCHOR)
				for i in self.winfo_children():
					if isinstance(i,tk.Listbox):
						i.unbind('<<ListboxSelect>>')
				self.loadingLabel['text'] = 'Loading'
				doTWork(self, self.p, kwargs = {'b':l2}, after = self.showCourses)
				self.loadingLabel['text'] = 'Ready'

		if e.widget == self.langsLBox3:
			l3 = self.langsLBox3.get(tk.ANCHOR)
			for i in self.winfo_children():
				if isinstance(i,tk.Listbox):
					i.unbind('<<ListboxSelect>>')
			self.loadingLabel['text'] = 'Loading'
			doTWork(self, self.p, kwargs = {'b':l3}, after = self.showCourses)
			self.loadingLabel['text'] = 'Ready'

		for i in self.winfo_children():
			if isinstance(i,tk.Listbox):
				i.bind('<<ListboxSelect>>', self.lBoxSelect)

	def showCourses(self):
		toAdd = self.browser.getCourses()
		
		col = 0
		row = 0
		for i in self.coursesHolder.interior.winfo_children():
			if i.id in toAdd:
				toAdd.remove(i.id)
				col += 1
				if col == 3: col = 0; row += 1
				if row == 0: row = 1; col -= 1
				#i.destroy()
			else:
				i.destroy()

		
		for i in toAdd:
			width = self.coursesHolder['width']
			if row > 0: width /= 3
			p = tk.PanedWindow(self.coursesHolder.interior, borderwidth = 0, width = width)#, height = 110 if not row == 0 else 160)
			p.id = i
			def g(): p.add(courseHolder(self, i, width), pady = 5)
			def k(): p.grid(column = col, row = row, columnspan = 3 if row == 0 else 1, sticky = 'nw')
			doTWork(self, g, after = k, daemon = True)
			
		

			col += 1
			if col == 3: col = 0; row += 1
			if row == 0: row = 1; col -= 1

	def sendName(self, name):
		self.name = name
		if not self.name == "":
			self.loadingLabel['text'] = 'Retrieving info'
			self.update()
			self.newCourse = memrise.Course(self.name, self.controller.supportedLangsReversed)

			self.loadingLabel['text'] = 'Downloading'
			self.update()
			self.newCourse.dump_course()

			self.loadingLabel['text'] = 'Cleaning it up'
			self.update()
			self.newCourse.fix()

			self.newCourse = self.newCourse.newCourse
			self.submitted = True

	def sendNameClose(self):
		self.name = None
		self.submitted = True

class courseHolder(tk.Frame):
	def __init__(self, parent, *args, **kw):
		tk.Frame.__init__(self, parent, borderwidth = 2, relief = tk.RIDGE)
		self.controller = parent
		self.width = args[1]
		Ctype = None
		t = args[0].attrs['class'][0]
		if t == 'featured-course-box':
			Ctype = 'featured'
		elif t == 'course-box-wrapper':
			Ctype = 'normal'
		self.renderCourseFrame(Ctype, args[0])

	def downloadCourse(self, url):
		url = 'http://www.memrise.com{}'.format(url)
		self.controller.sendName(url)

	def renderCourseFrame(self, Ctype, code):
		def downloadPic(coursePicture, size):
				raw_data = requests.get(coursePicture).content
				im = Image.open(BytesIO(raw_data))
				im = im.resize(size=size)
				image = ImageTk.PhotoImage(im)
				label1 = tk.Label(coursePictureFrame, image=image)
				label1.image = image
				label1.grid()

		if Ctype == 'featured':
			courseName = code.find('div', {'class':'details'}).find('h2').text.strip()
			coursePicture = code.find('div', {'class':'picture-wrap'}).find('img').attrs['src']
			courseDesc = code.find('div', {'class':'description'}).text.strip()
			courseLearning = code.find('div', {'class':'stats'}).find('span', {'class':'stat'}).text.strip()
			courseDuration = code.find('div', {'class':'stats'}).find('span', {'class':'stat'}).find_next_sibling().text.strip()
			courseAuthor = code.find('div',  {'class':'details-wrap'}).find('strong').text.strip()
			courseUrl = code.attrs['href']
			
			courseNameLabel = tk.Label(self, text = courseName, wraplength = self.width/3)
			courseNameLabel.grid(row = 0, column = 0, sticky = 'nw')

			coursePictureFrame = tk.Frame(self, height = 128, width = 128)
			coursePictureFrame.grid(row= 1, column = 0, sticky = 'nw', rowspan = 3, pady = 10)
			doTWork(self.controller, downloadPic, kwargs={'coursePicture':coursePicture,'size':(128,128)}, after = self.update, daemon = True)

			courseDescLabel = tk.Label(self, text = courseDesc, wraplength = self.width * (2/3))
			courseDescLabel.grid(row = 1, column = 1, rowspan = 2, columnspan = 2, sticky = 'nw')

			courseLearningLabel = tk.Label(self, text = 'Learning: {}'.format(courseLearning), wraplength = self.width/3)
			courseLearningLabel.grid(row = 3, column = 2, sticky = 'nw')

			courseDurationLabel = tk.Label(self, text = 'Duration: {}'.format(courseDuration), wraplength = self.width/3)
			courseDurationLabel.grid(row = 3, column = 1, sticky = 'nw')

			courseAuthorLabel = tk.Label(self, text = 'Author: {}'.format(courseAuthor), wraplength = self.width/3)
			courseAuthorLabel.grid(row = 0, column = 1, sticky = 'nw')

			courseDownloadButton = tk.Button(self, text = 'Download', command = lambda: self.downloadCourse(courseUrl))
			courseDownloadButton.grid(row = 0, column = 2, sticky = 'ne')

		elif Ctype == 'normal':
			courseName = code.find('a', {'class':'inner'}).text.strip()
			coursePicture = code.find('div', {'class':'course-box-picture'}).attrs['style'].split('"')[1].split('"')[0].replace('https','http')
			courseLearning = code.find('div', {'class':'stats'}).find('span', {'class':'stat'}).text.strip()
			courseDuration = code.find('div', {'class':'stats'}).find('span', {'class':'stat'}).find_next_sibling().text.strip()
			try: courseAuthor = code.find('span', {'class':'author pull-right'}).find('a').text.strip()
			except:	courseAuthor = 'UserDeleted'
			courseUrl = code.find('a', {'class':'inner'}).attrs['href']

			courseNameLabel = tk.Label(self, text = courseName, wraplength = self.width * (2/3))
			courseNameLabel.grid(row = 0, column = 0, sticky = 'nw', columnspan = 2)

			coursePictureFrame = tk.Frame(self, height = 64, width = 64)
			coursePictureFrame.grid(row=1, column = 0, sticky = 'nw', rowspan = 3, pady = 10)
			doTWork(self.controller, downloadPic, kwargs={'coursePicture':coursePicture,'size':(64,64)}, after = self.update, daemon = True)

			courseLearningLabel = tk.Label(self, text = "Learning: {}".format(courseLearning), wraplength = self.width * (2/3))
			courseLearningLabel.grid(row = 3, column = 1, sticky = 'nw', columnspan = 2)

			courseDurationLabel = tk.Label(self, text = "Duration: {}".format(courseDuration), wraplength = self.width * (2/3))
			courseDurationLabel.grid(row = 2, column = 1, sticky = 'nw', columnspan = 2)

			courseAuthorLabel = tk.Label(self, text = 'Author: {}'.format(courseAuthor), wraplength = self.width * (2/3))
			courseAuthorLabel.grid(row = 1, column = 1, sticky = 'nw', columnspan = 2)

			courseDownloadButton = tk.Button(self, text = 'Download', command = lambda: self.downloadCourse(courseUrl))
			courseDownloadButton.grid(row = 0, column = 2, sticky = 'ne')
			
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
                canvas.config(width = interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width = canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)