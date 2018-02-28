import traceback

def start(debug = False):
	try:
		from tkinter import messagebox
		from helpLibs import installLibs
		from helpLibs import Maingui

		if debug:
			app = Maingui.MainFrame()
			app.mainloop()
		else:
			app = Maingui.MainFrame()
			app.mainloop()
			Maingui.makeBackup()
	except ImportError as e:
		installLibs.installMod(e.name)
		start()
	except Exception as e:
		messagebox.showinfo("Error", (traceback.format_exc()))

if __name__ == '__main__': start()