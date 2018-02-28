import importlib
import subprocess

def installMod(i):
	#pip.main(['install', i])
	process = subprocess.Popen(["pip", "install", i], shell=False)
	process.wait()