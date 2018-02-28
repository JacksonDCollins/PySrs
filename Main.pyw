from helpLibs import Maingui
from tkinter import messagebox
print("test")
def start(debug = False):
	try:
		if debug:
			app = Maingui.MainFrame()
			app.mainloop()
		else:
			app = Maingui.MainFrame()
			app.mainloop()
			Maingui.makeBackup()
	except Exception as e:
		messagebox.showinfo("Error", e)


if __name__ == '__main__': start()