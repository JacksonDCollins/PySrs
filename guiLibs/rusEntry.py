import tkinter as tk
import tkinter.ttk as ttk
import ctypes
import unicodedata as u
#from alphabet_detector import AlphabetDetector
import time

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
			key[83] = "б"
			key[89] = "б"
			key[74] = "аЙ"
			key[67] = "б"

			key[83, 32] = "б"
			key[83, 83] = "бб"
			key[89, 32] = "б"
			key[89, 89] = "бб" 
			key[74, 32] = "аЙ"
			key[74, 74] = "аЙаЙ"
			key[67, 32] = "б"
			key[67, 67] = "бб"
			
			key[83, 72] = "б"
			key[83, 67] = "б"
			key[67, 72] = "б"
			key[89, 65] = "б"
			key[89, 79] = "б"
			key[89, 69] = "б"
			key[89, 85] = "б"
			key[74, 65] = "б"
			key[74, 79] = "б"
			key[74, 69] = "б"
			key[74, 85] = "б"

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
		tk.Entry.__init__(self, master)
		for i in kwargs:
			self[i] = kwargs[i]
		self.bind('<Key>', self.check)
		self.bind('<Control-Key-question>', self.CKey)
		self.bind('<Control-Key-Multi_key>', self.CKey)
		self.allow = True
		self.last = None
		self['validate'] = 'key'
		self['validatecommand'] = self.register(lambda: self.allow)
		self.key = {}
		#self.getKLayout()

	def doAllow(self):
		#old = self.allow
		self.allow = True
		#return old

	def CKey(self,e):
		if e.keycode == 65:
			self.select_range(0,tk.END)
		if e.keycode == 67:
			self.clipboard_clear()
			self.clipboard_append(self.selection_get())
		if e.keycode == 86:	
			self.insert(tk.INSERT, self.clipboard_get())
			self.selection_clear()

	def check(self, e):
		self.after(1,self.raiseEvent)
		self.key[83] = "с"
		self.key[89] = "ы"
		self.key[74] = "й"
		self.key[67] = "ц"
		self.key[83, 72] = "ш"
		self.key[83, 67] = "щ"
		self.key[67, 72] = "ч"
		self.key[89, 65] = "я"
		self.key[89, 79] = "ё"
		self.key[89, 69] = "э"
		self.key[89, 85] = "ю"
		self.key[74, 65] = "я"
		self.key[74, 79] = "ё"
		self.key[74, 69] = "э"
		self.key[74, 85] = "ю"
		
		if self.allow == False:
			if self.last == e.keycode:
				self.allow = True
				self.insert(tk.INSERT, self.key[self.last]*2)
				self.last = None
				return
			elif (self.last, e.keycode) in self.key:
				self.allow = True
				self.insert(tk.INSERT, self.key[self.last, e.keycode])
				self.last = None
				self.allow = False
				self.after(1, self.doAllow)
				return
			elif not (self.last, e.keycode) in self.key and self.last in self.key and e.keycode in self.key:
				self.allow = True
				self.insert(tk.INSERT, self.key[self.last]+self.key[e.keycode])
				self.last = None
				return
			elif e.keycode in (8,32):
				self.allow = True
				try:
					self.insert(tk.INSERT, self.key[self.last])
					self.last = None
					self.allow = False
					self.after(1, self.doAllow)
				except: pass
				return
			elif self.last in self.key and not e.keycode in self.key:
				self.allow = True
				self.insert(tk.INSERT, self.key[self.last]+e.char)
				self.last = None
				self.allow = False
				self.after(1, self.doAllow)
				return

		#self.allow = True
		if e.keysym == "Multi_key":
			self.allow = False
			self.last = e.keycode

	def getKLayout(self):
		codes = []
		i = 0
		while i < 1114112 :
			try:

				codes.append((chr(i), i))
			except Exception as e:
				print(e, i)
			i += 1

		# print(ord('б'))
		# print("б".isalpha())
		print(u.name("ꚓ"))
		help(u.category)
		d = AlphabetDetector()
		for i in codes:
			try:
				if 'LATIN' in u.name(i[0]) and not u.combining(i[0]) and 'Ll' in u.category(i[0].lower()):#d.only_alphabet_chars(i[0],'CYRILLIC') and i[0].isalpha():
					print(i)
			except: 
				pass
		# # For debugging Windows error codes in the current thread
		# user32 = ctypes.WinDLL('user32', use_last_error=True)
		# curr_window = user32.GetForegroundWindow()
		# thread_id = user32.GetWindowThreadProcessId(curr_window, 0)

		# # Made up of 0xAAABBBB, AAA = HKL (handle object) & BBBB = language ID
		# klid = user32.GetKeyboardLayout(thread_id)

		# help(user32.GetKeyboardLayout)
		# # Language ID -> low 10 bits, Sub-language ID -> high 6 bits
		# # Extract language ID from KLID
		# lid = klid & (2**16 - 1)

		# # Convert language ID from decimal to hexadecimal
		# lid_hex = hex(lid)
		# return lid_hex

	def raiseEvent(self):
		self.event_generate("<<textEntered>>")

if __name__ == "__main__":
	app = tk.Tk()
	frame = tk.Frame(app)
	frame.grid()
	e = Entry(frame)
	e.grid()
	#e.bind('<Multi_key>',lambda x: print(x), '<Key>')
	app.mainloop()