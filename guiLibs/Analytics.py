import tkinter as tk
import tkinter.ttk as ttk
import helpLibs.mycsv as mycsv
import helpLibs.srs as srs
import helpLibs.consts as consts
from datetime import timedelta as td
import math

class Analytics(tk.Frame):
	def __init__(self, master, controller):
		tk.Frame.__init__(self, master)
		self.grid()
		self.controller = controller		
		self.size = "800x600"
		self.bind("<<ShowFrame>>", self.on_show_frame)
		self.init_vals()
		if self.controller.Analynew == True:
			self.historyFiles()
			self.controller.Analynew = False
		

	def init_vals(self):
		self.allHis = []
		self.hfiles = []
		self.hfilesread = {}
		self.days = {}
		self.secondsLearn = 0 
		self.minutesLearn = 0
		self.hoursLearn = 0

	def convertStrTimeAddDays(self, date, days = 0):
		k = srs.convertToTime(date) + td(days = days)
		return "{}/{}/{}".format(k.day, k.month, k.year), k

	def historyFiles(self):
		self.init_vals()
		for i in self.controller.dandl:
			self.controller.update()
			print('{}\\{}\\{}{}'.format(consts.cwd(),consts.fname(),i,consts.hwdoc()))
			self.hfiles.append('{}\\{}\\{}{}'.format(consts.cwd(),consts.fname(),i,consts.hwdoc()))

		for j in self.hfiles:
			self.controller.update()
			try:
				deckName = j.split("\\")[6]
				self.hfilesread[deckName] = []
				for line in mycsv.read(j).split("\n"):
					self.controller.update()
					if not line == '':
						self.hfilesread[deckName].append(line.split(','))
			except:
				pass

		for k in self.hfilesread:
			self.controller.update()
			for n,i in enumerate(self.hfilesread[k]):
				self.controller.update()
				self.allHis.append(i)

		#
		l = []
		p = []
		seconds = 0
		for i in self.allHis:
			self.controller.update()
			if i[16] == mycsv.curdate and i[15] == "review":
				l.append(i)
				seconds += float(i[18])
			if i[16] == mycsv.curdate and i [15] == "learn":
				p.append(i)
		self.donetoday = len(l)
		self.learnedtoday = len(p)

		self.minutesLearn, self.secondsLearn = divmod(seconds, 60)
		self.hoursLearn, self.minutesLearn = divmod(self.minutesLearn, 60)

		j = self.convertStrTimeAddDays(mycsv.curdate)
		l = self.convertStrTimeAddDays(mycsv.curdate)
		for i in self.controller.total:
			self.controller.update()
			k = self.convertStrTimeAddDays(i.split(",")[8])
			if k[1] > j[1]:
				j = k
			if k[1] < l[1]:
				l = k

		self.latestdate = j
		self.earliestdate = l
		self.startdate = self.earliestdate
		
		while not self.startdate[1] == self.latestdate[1]:
			self.controller.update()
			self.startdate = self.convertStrTimeAddDays(self.startdate[0], days = 1)
			if not self.startdate[0] in self.days:
				self.days[self.startdate[0]] = []
			for i in self.controller.total:
				if i.split(",")[8] == self.startdate[0]:
					self.days[self.startdate[0]].append(i)
	
	def clamp(self, n, minn, maxn): return max(min(maxn, n), minn)
	def equals(self, n, k):
		if n == k:
			return 0
		else:
			return 1

	def drawBar(self):
		c_width = 650
		c_height = 300
		self.f = tk.Frame(self)
		self.f.grid(padx = 5, row = 0, column = 0)
		self.l = tk.Label(self.f, text = "REVIEW FORECAST")
		self.l.pack()
		self.c = tk.Canvas(self.f, width=c_width, height=c_height, bg = 'white')
		self.c.pack()
		self.v = tk.Scrollbar(self.f, orient = tk.HORIZONTAL)
		self.v.pack(fill=tk.X)
		self.ldonetoday = tk.Label(self.f)

		if self.hoursLearn > 0:
			if self.hoursLearn < 2 and self.hoursLearn > 1:
				if self.minutesLearn > 0:
					if self.minutesLearn < 2 and self.minutesLearn > 1:
						if self.secondsLearn > 0:
							if self.secondsLearn < 2 and self.secondsLearn > 1:
								self.ldonetoday['text'] = "Words reviewed today : {} \n In {} hour, {} minute and {} second".format(self.donetoday, math.floor(self.hoursLearn), math.floor(self.minutesLearn), math.floor(self.secondsLearn))
							else:
								self.ldonetoday['text'] = "Words reviewed today : {} \n In {} hour, {} minute and {} seconds".format(self.donetoday, math.floor(self.hoursLearn), math.floor(self.minutesLearn), math.floor(self.secondsLearn))
						else:
							self.ldonetoday['text'] = "Words reviewed today : {} \n In {} hour and {} minute".format(self.donetoday, math.floor(self.hoursLearn), math.floor(self.minutesLearn))
					else:
						if self.secondsLearn > 0:
							if self.secondsLearn < 2 and self.secondsLearn > 1:
								self.ldonetoday['text'] = "Words reviewed today : {} \n In {} hour, {} minutes and {} second".format(self.donetoday, math.floor(self.hoursLearn), math.floor(self.minutesLearn), math.floor(self.secondsLearn))
							else:
								self.ldonetoday['text'] = "Words reviewed today : {} \n In {} hour, {} minutes and {} seconds".format(self.donetoday, math.floor(self.hoursLearn), math.floor(self.minutesLearn), math.floor(self.secondsLearn))
						else:
							self.ldonetoday['text'] = "Words reviewed today : {} \n In {} hour and {} minutes".format(self.donetoday, math.floor(self.hoursLearn), math.floor(self.minutesLearn))
				else:
					if self.secondsLearn > 0:
						if self.secondsLearn < 2 and self.secondsLearn > 1:
							self.ldonetoday['text'] = "Words reviewed today : {} \n In {} hour and {} second".format(self.donetoday, math.floor(self.hoursLearn),  math.floor(self.secondsLearn))
						else:
							self.ldonetoday['text'] = "Words reviewed today : {} \n In {} hour and {} seconds".format(self.donetoday, math.floor(self.hoursLearn),  math.floor(self.secondsLearn))
					else:
						self.ldonetoday['text'] = "Words reviewed today : {} \n In {} hour".format(self.donetoday, math.floor(self.hoursLearn))
			else:
				if self.minutesLearn > 0:
					if self.minutesLearn < 2 and self.minutesLearn > 1:
						if self.secondsLearn < 2 and self.secondsLearn > 1:
							self.ldonetoday['text'] = "Words reviewed today : {} \n In {} hours, {} minute and {} second".format(self.donetoday, math.floor(self.hoursLearn), math.floor(self.minutesLearn), math.floor(self.secondsLearn))
						else:
							self.ldonetoday['text'] = "Words reviewed today : {} \n In {} hours, {} minute and {} seconds".format(self.donetoday, math.floor(self.hoursLearn), math.floor(self.minutesLearn), math.floor(self.secondsLearn))
					else:
						if self.secondsLearn < 2 and self.secondsLearn > 1:
							self.ldonetoday['text'] = "Words reviewed today : {} \n In {} hours, {} minutes and {} second".format(self.donetoday, math.floor(self.hoursLearn), math.floor(self.minutesLearn), math.floor(self.secondsLearn))
						else:
							self.ldonetoday['text'] = "Words reviewed today : {} \n In {} hours, {} minutes and {} seconds".format(self.donetoday, math.floor(self.hoursLearn), math.floor(self.minutesLearn), math.floor(self.secondsLearn))
				else:
					if self.secondsLearn > 0:
						if self.secondsLearn < 2 and self.secondsLearn > 1:
							self.ldonetoday['text'] = "Words reviewed today : {} \n In {} hours and {} second".format(self.donetoday, math.floor(self.hoursLearn),  math.floor(self.secondsLearn))
						else:
							self.ldonetoday['text'] = "Words reviewed today : {} \n In {} hours and {} seconds".format(self.donetoday, math.floor(self.hoursLearn), math.floor(self.secondsLearn))
					else:
						self.ldonetoday['text'] = "Words reviewed today : {} \n In {} hours".format(self.donetoday, math.floor(self.hoursLearn))
		else:
			if self.minutesLearn > 0:
				if self.minutesLearn < 2 and self.minutesLearn > 1:
					if self.secondsLearn > 0:
						if self.secondsLearn < 2 and self.secondsLearn > 1:
							self.ldonetoday['text'] = "Words reviewed today : {} \n In {} minute and {} second".format(self.donetoday, math.floor(self.minutesLearn), math.floor(self.secondsLearn))
						else:
							self.ldonetoday['text'] = "Words reviewed today : {} \n In {} minute and {} seconds".format(self.donetoday, math.floor(self.minutesLearn), math.floor(self.secondsLearn))
					else:
						self.ldonetoday['text'] = "Words reviewed today : {} \n In {} minute".format(self.donetoday, math.floor(self.minutesLearn))
				else:
					if self.secondsLearn > 0:
						if self.secondsLearn < 2 and self.secondsLearn > 1:
							self.ldonetoday['text'] = "Words reviewed today : {} \n In {} minutes and {} second".format(self.donetoday, math.floor(self.minutesLearn), math.floor(self.secondsLearn))
						else:
							self.ldonetoday['text'] = "Words reviewed today : {} \n In {} minutes and {} seconds".format(self.donetoday, math.floor(self.minutesLearn), math.floor(self.secondsLearn))
					else:
						self.ldonetoday['text'] = "Words reviewed today : {} \n In {} minutes".format(self.donetoday, math.floor(self.minutesLearn))
			else:
				if self.secondsLearn < 2 and self.secondsLearn > 1:
					self.ldonetoday['text'] = "Words reviewed today : {} \n In {} second".format(self.donetoday, math.floor(self.secondsLearn))
				else:
					self.ldonetoday['text'] = "Words reviewed today : {} \n In {} seconds".format(self.donetoday, math.floor(self.secondsLearn))

		
		hours = math.floor(self.hoursLearn)
		minutes = math.floor(self.minutesLearn)
		seconds = math.floor(self.secondsLearn)

		##fix this
		line = ( "Words reviewed today : {}\nIn{}{}{}{}{}".format(self.donetoday," {} hour{}".format(hours,"s"*self.equals(hours,1))*self.clamp(hours,0,1)," and"*self.equals(self.clamp(minutes,0,1)+self.clamp(seconds,0,1),2) + ","*self.clamp(hours,0,1) * self.clamp(minutes,0,1) * self.clamp(seconds,0,1)," {} minute{}".format(minutes,"s"*self.equals(minutes,1))*self.clamp(minutes,0,1)," and"*self.clamp(seconds,0,1), " {} second{}".format(seconds,"s"*self.equals(seconds,1))*self.clamp(seconds,0,1)))# + ("and" - hour,minute,second > 0)
		self.ldonetoday['text'] = line

		self.ldonetoday.pack()
		self.pdonetoday = tk.Label(self.f, text ="Words learned today : {}".format(self.learnedtoday))
		self.pdonetoday.pack()
		
		# stretch enough to get all data items in
		x_stretch = 35
		x_width = 35
		# gap between left canvas edge and y axis
		x_gap = 35
		text_height = 100
		
		l = 0
		for j in self.days:
			self.controller.update()
			if len(self.days[j]) > l:
				l = len(self.days[j])
		y_stretch = c_height/(l+text_height)
		
		s = 0
		t = 0
		m = 0
		for x, j in enumerate(self.days):
			self.controller.update()
			y = len(self.days[j])
			x = x-t
			if y == 0:
				t += 1
				continue

			p = (self.convertStrTimeAddDays(j), self.convertStrTimeAddDays(mycsv.curdate))
			if (p[0][1] - p[1][1]).days > consts.month():
				break
			else:
				m = m + 1
				s = s + len(self.days[j])

			#calculate reactangle coordinates (integers) for each bar
			x1 = x * x_stretch + x * x_width + x_gap
			y1 = c_height - (y * y_stretch)
			x0 = x * x_stretch + x * x_width + x_width + x_gap
			y0 = c_height
			
			# draw the bar
			self.c.create_rectangle(x0, y0, x1, y1, fill="lime")
			# put the y value above each bar
			self.c.create_text(x0-40, y0+15, anchor=tk.SW, text=str(j))
			self.c.create_text(x1+2, y1, anchor=tk.SW, text=str(y))

		m = consts.month()
		if s/m > (len(self.controller.toReview) + self.donetoday):
			s = (len(self.controller.toReview) + self.donetoday) *m
		self.recommendedDaily = math.ceil(s/m)
		self.lrecommendedDaily = tk.Label(self.f, text ="Today you should review {} words".format(self.recommendedDaily))
		self.lrecommendedDaily.pack()

		self.c.config(scrollregion=self.c.bbox("all"))
		self.c.config(xscrollcommand=self.v.set)
		self.v.config(command=self.c.xview)

	def createWidgets(self):
		self.historyBrowser = tk.Listbox(self,  selectmode = "BROWSE", exportselection=0)

		self.buttonGoBack = tk.Button(self, text = "Go Back", command = self.goMainMenu)
		self.buttonGoBack.grid(row = 0, column=1)

	def on_show_frame(self, event):
		for widget in self.winfo_children():
			widget.destroy()
		self.controller.geometry(self.size)
		load = self.controller.Splash(self)
		load.grid()

		if self.controller.Analynew == True:
			self.historyFiles()
			self.controller.Analynew = False
		self.controller.update()
		self.createWidgets()
		self.drawBar()
		
		load.destroy()

	def goMainMenu(self):
		self.controller.show_frame("Mainmenu", me = self)