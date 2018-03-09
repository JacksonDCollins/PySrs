import tkinter as tk
import tkinter.ttk as ttk
import ctypes
import unicodedata as u
#from alphabet_detector import AlphabetDetector
import time
import configparser
import helpLibs.consts as consts

class mEntry(tk.Entry):
	def __init__(self, master, *args, **kwargs):
		tk.Entry.__init__(self, master, validate = 'all')
		self.vcmd = (self.register(self.validate), '%S', '%d', '%i', '%P', '%s', '%v', '%V', '%W')
		self['validatecommand'] = self.vcmd
		self.last = self.get()
		for i in kwargs:
			self[i] = kwargs[i]
		self.bind('<Key>', self.eventText)
		self.nullKeys()
		self.updateEntry()

	def updateEntry(self):
		if not self.last == self.get():
			self.last = self.get()
			self.raiseEvent()
				
		self.insert(tk.INSERT, self.answerChar)
		self.insert(tk.INSERT, self.charAfter)
		self.answerChar = ""
		self.charAfter = ""
		self.after(1, self.updateEntry)

	def eventText(self, e):
		keys = (83, 89, 74, 67)	
		if self.getKLayout() == "0x419": #russian keyboard	
			self.lastchar = self.thischar
			self.thischar = e.keycode

		if e.state == 12:
			if e.keycode == 65:
				self.select_range(0,tk.END)

		if self.lastchar == self.thischar:
			self.validate()	
		if self.lastchar in keys and self.thischar in keys:
			self.validate()

	def nullKeys(self):
		self.lastchar = None
		self.thischar = None
		self.answerChar = ""
		self.charAfter = ""
		self.entryEditing = None

	def getKLayout(self):
		# For debugging Windows error codes in the current thread
		user32 = ctypes.WinDLL('user32', use_last_error=True)
		curr_window = user32.GetForegroundWindow()
		thread_id = user32.GetWindowThreadProcessId(curr_window, 0)

		# Made up of 0xAAABBBB, AAA = HKL (handle object) & BBBB = language ID
		klid = user32.GetKeyboardLayout(thread_id)

		# Language ID -> low 10 bits, Sub-language ID -> high 6 bits
		# Extract language ID from KLID
		lid = klid & (2**16 - 1)

		# Convert language ID from decimal to hexadecimal
		lid_hex = hex(lid)
		return lid_hex

	def validate(self, *arg):
		keys = (83, 89, 74, 67)
		if self.getKLayout() == "0x409": #english keyboard
			return True
		if self.getKLayout() == "0x419": #russian keybaord
			if not self.lastchar in keys:
				return True
			
			key = {}
			key[83] = "с"
			key[89] = "ы"
			key[74] = "й"
			key[67] = "ц"

			key[83, 32] = "с"
			key[83, 83] = "сс"
			key[89, 32] = "ы"
			key[89, 89] = "ыы" 
			key[74, 32] = "й"
			key[74, 74] = "йй"
			key[67, 32] = "ц"
			key[67, 67] = "цц"
			
			key[83, 72] = "ш"
			key[83, 67] = "щ"
			key[67, 72] = "ч"
			key[89, 65] = "я"
			key[89, 79] = "ё"
			key[89, 69] = "э"
			key[89, 85] = "ю"
			key[74, 65] = "я"
			key[74, 79] = "ё"
			key[74, 69] = "э"
			key[74, 85] = "ю"

			if self.thischar == 8:
				self.answerChar = key[self.lastchar]
				self.lastchar = None
				self.thischar = None
				return False
			
			if (self.lastchar, self.thischar) in key:
				self.answerChar = key[self.lastchar, self.thischar]
				self.lastchar = None
				self.thischar = None
				return False

			if self.lastchar in key and self.thischar in key:
				self.answerChar = key[self.lastchar]
				self.charAfter = key[self.thischar]
				self.lastchar = None
				self.thischar = None
				return False
			
			self.answerChar = key[self.lastchar]
			self.charAfter = arg[0]
			self.lastchar = None
			return False

	def raiseEvent(self):
		self.event_generate("<<textEntered>>")

class Entry(tk.Entry):
	def __init__(self, master, *args, **kwargs):
		tk.Entry.__init__(self, master, *args, **kwargs)
		self.bind('<Key>', self.check)
		self.bind('<Shift-Key-Multi_key>', lambda e: self.check(e, True))
		self.bind('<Shift-Key>', lambda e: self.check(e, True))
		self.bind('<Control-Key-question>', self.CKey)
		self.bind('<Control-Key-Multi_key>', self.CKey)
		
		confile = consts.cwd() + '\layoutMaps.ini'
		config = configparser.ConfigParser()
		config.read(confile, encoding = 'utf-8')
		
		self.keys = {}
		for k in config:
			keyset = {}
			for i in config[k]:
				if ', ' in i:
					j = i.split(', ')
					keyset[int(j[0]), int(j[1])] = config[k][i]
				else:
					keyset[int(i)] = config[k][i]
			self.keys[k] = keyset
		self.last = None

	def CKey(self,e):
		if e.keycode == 65:
			self.select_range(0,tk.END)
		if e.keycode == 67:
			self.clipboard_clear()
			self.clipboard_append(self.selection_get())
		if e.keycode == 86:	
			self.insert(tk.INSERT, self.clipboard_get())
			self.selection_clear()

	def check(self, e, upper=False):
		self.raiseEvent()
		up = False
		if str(self.getKLayout()) in self.keys:
			key = self.keys[str(self.getKLayout())]
		else:
			self.last = None
			return

		if isinstance(self.last, str):
			self.last = int(self.last.replace('-UP',''))
			up = True

		if True:
			if self.last == e.keycode:
				t = key[self.last].upper() if up else key[self.last]
				p = key[e.keycode].upper() if upper else key[e.keycode]
				self.insert(tk.INSERT, t+p)
				self.last = None
				return
			elif (self.last, e.keycode) in key:
				t =  key[self.last]+e.char if upper and not up else key[self.last, e.keycode].upper() if up else key[self.last, e.keycode]
				self.insert(tk.INSERT, t)
				self.last = None
				return 'break'
			elif not (self.last, e.keycode) in key and self.last in key and e.keycode in key:
				t = key[self.last].upper() if up else key[self.last]
				p = key[e.keycode].upper() if upper else key[e.keycode]
				self.insert(tk.INSERT, t+p)
				self.last = None
				return
			elif e.keycode in (8,32):
				try:
					t = key[self.last].upper() if up else key[self.last]
					self.insert(tk.INSERT, t)
					self.last = None
					return 'break'
				except: return
			elif self.last in key and not e.keycode in key:
				if 'Shift' in e.keysym: return
				t = key[self.last].upper() if up else key[self.last]
				self.insert(tk.INSERT, t+e.char)
				self.last = None
				return 'break'

		if e.keysym == "Multi_key":
			self.last = (str(e.keycode) + '-UP' if upper else e.keycode)

	def getKLayout(self):
		
		# For debugging Windows error codes in the current thread
		user32 = ctypes.WinDLL('user32', use_last_error=True)
		curr_window = user32.GetForegroundWindow()
		thread_id = user32.GetWindowThreadProcessId(curr_window, 0)

		# Made up of 0xAAABBBB, AAA = HKL (handle object) & BBBB = language ID
		klid = user32.GetKeyboardLayout(thread_id)
		# Language ID -> low 10 bits, Sub-language ID -> high 6 bits
		# Extract language ID from KLID
		lid = klid & (2**16 - 1)

		# Convert language ID from decimal to hexadecimal
		lid_hex = hex(lid)
		return klid

	def raiseEvent(self):
		self.event_generate("<<textEntered>>")

if __name__ == "__main__":
	app = tk.Tk()
	frame = tk.Frame(app)
	frame.grid()
	e = Entry(frame)
	print([chr(x) if not isinstance(x, tuple) else (chr(x[0]),chr(x[1])) for x in e.key ])
	print(e.getKLayout())
	e.grid()
	#e.bind('<Multi_key>',lambda x: print(x), '<Key>')
	app.mainloop()