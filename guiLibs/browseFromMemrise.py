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
		for i in self.coursesHolder.interior.winfo_children():
			i.destroy()

		col = 0
		row = 0
		for i in self.browser.getCourses():
			width = self.coursesHolder['width']
			if row > 0: width /= 3
			p = tk.PanedWindow(self.coursesHolder.interior, borderwidth = 0, width = width)
			def g(): p.add(courseHolder(self, i), pady = 5)
			def k(): p.grid(column = col, row = row, columnspan = 3 if row == 0 else 1)
			doTWork(self, g, after = k, daemon = True)
			col += 1
			if col == 3: col = 0; row += 1
			if row == 0: row = 1; col -= 1

	def sendNameClose(self):
		self.name = None
		self.submitted = True

class courseHolder(tk.Frame):
	def __init__(self, parent, *args, **kw):
		self.controller = parent
		Ctype = None
		t = args[0].attrs['class'][0]
		if t == 'featured-course-box':
			Ctype = 'featured'
			tk.Frame.__init__(self, parent, borderwidth = 2, relief = tk.RIDGE)
		elif t == 'course-box-wrapper':
			Ctype = 'normal'
			tk.Frame.__init__(self, parent, borderwidth = 2, relief = tk.RIDGE)
		self.renderCourseFrame(Ctype, args[0])

	def renderCourseFrame(self, Ctype, code):	
		if Ctype == 'featured':
			"""<a class="featured-course-box" href="/course/110929/romanian-101/">
				<div class="inner-wrap">
				 <span class="start-icon ico ico-arr-right ico-l">
				 </span>
				 <div class="picture-wrap">
				  <img alt="" src="https://d2rhekw5qr4gcj.cloudfront.net/img/400sqf/from/uploads/course_photos/76031_memrise.jpg"/>
				 </div>
				 <div class="details-wrap">
				  <span class="author pull-right" data-direction="bottom" data-role="hovercard" data-user-id="839544">
				   by
				   <strong>
				    TeonaBaetu
				   </strong>
				  </span>
				  <div class="details">
				   <h2>
				    Romanian 101
				   </h2>
				   <div class="description">
				    Your Romanian language survival kit. (with audio) 

					Please post feedback here:
					https://community.memrise.com/t/course-forum-romanian-101-typo-in-solutions/1956/9
				   </div>
				  </div>
				  <div class="stats">
				   <span class="stat">
				    <span class="ico ico-user">
				    </span>
				    19.2k learners
				   </span>
				   <span class="stat">
				    <span class="ico ico-clock">
				    </span>
				    3h avg duration
				   </span>
				  </div>
				 </div>
				</div>
				<span class="target-photo">
				 <img alt="" src="https://d2rhekw5qr4gcj.cloudfront.net/uploads/language_photos/Romanian.png"/>
				</span>
			   </a>
			"""
			courseName = code.find('div', {'class':'details'}).find('h2').text.strip()
			coursePicture = code.find('div', {'class':'picture-wrap'}).find('img').attrs['src']
			courseDesc = code.find('div', {'class':'description'}).text.strip()
			courseLearning = code.find('div', {'class':'stats'} ).find('span',{'class':'ico ico-user'}).text.strip()
			courseDuration = code.find('div', {'class':'stats'}).find('span',{'class':'ico ico-clock'}).text.strip()
			courseAuthor = code.find('div',  {'class':'details-wrap'}).text.strip()
			courseUrl = code.attrs['href']
			
			label = tk.Label(self, text = courseName)
			label.grid()

			def test(coursePicture):
				raw_data = requests.get(coursePicture).content
				im = Image.open(BytesIO(raw_data))
				im = im.resize(size=(64,64))
				image = ImageTk.PhotoImage(im)
				label1 = tk.Label(self, image=image)
				label1.image = image
				label1.grid()
			doTWork(self.controller, test, kwargs={'coursePicture':coursePicture}, after = self.update)	

		elif Ctype == 'normal':
			"""<div class="course-box-wrapper col-xs-12 col-sm-6 col-md-4">
				<div class="course-box ">
				 <div class="inner-wrap">
				  <a class="picture-wrapper" href="/course/53658/romanian-for-beginners/">
				   <div class="course-box-picture" style='background-image: url("https://d2rhekw5qr4gcj.cloudfront.net/img/400sqf/from/uploads/course_photos/prenos.jpg")'>
				   </div>
				  </a>
				  <div class="details-wrapper">
				   <div class="target-photo">
				    <img alt="" src="https://d2rhekw5qr4gcj.cloudfront.net/uploads/language_photos/Romanian.png"/>
				   </div>
				   <div class="clearfix">
				    <span class="author pull-right">
				     by
				     <span>
				      _deleted_151212_2050_34
				     </span>
				    </span>
				    <a class="category" href="/courses/english/romanian/" title="Romanian">
				     Romanian
				    </a>
				   </div>
				   <h3>
				    <a class="inner" href="/course/53658/romanian-for-beginners/" title="Romanian for beginners">
				     Romanian for beginners
				    </a>
				   </h3>
				   <div class="details">
				    <div class="stats">
				     <span class="stat" title="
				                         9.69k people are learning this course
				                         ">
				      <span class="ico ico-user">
				      </span>
				      9.69k
				     </span>
				     <span class="stat" title="This course takes about 4h">
				      <span class="ico ico-clock">
				      </span>
				      4h
				     </span>
				    </div>
				   </div>
				  </div>
				 </div>
				</div>
			   </div>
				"""

			courseName = code.find('a', {'class':'inner'}).text.strip()
			coursePicture = code.find('div', {'class':'course-box-picture'}).attrs['style'].split('"')[1].split('"')[0].replace('https','http')
			courseLearning = code.find('div', {'class':'stats'}).find('span', {'class':'ico ico-user'}).text.strip()
			courseDuration = code.find('div', {'class':'stats'}).find('span', {'class':'ico ico-clock'}).text.strip()
			courseAuthor = code.find('span', {'class':'author pull-right'}).text.strip()
			courseUrl = code.find('a', {'class':'inner'}).attrs['href']

			label = tk.Label(self, text = courseName)
			label.grid()

			def test(coursePicture):
				raw_data = requests.get(coursePicture).content
				im = Image.open(BytesIO(raw_data))
				im = im.resize(size=(64,64))
				image = ImageTk.PhotoImage(im)
				label1 = tk.Label(self, image=image)
				label1.image = image
				label1.grid()
			doTWork(self.controller, test, kwargs={'coursePicture':coursePicture}, after = self.update)
			

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