#setup.py
import sys, os
from cx_Freeze import setup, Executable
import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

__version__ = "1.1.0"

include_files = [os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'), os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),'helpLibs/phantomjs.exe','helpLibs/audLight.jpg', 'helpLibs/audDark.jpg']
excludes = ["pip"]
packages = ['idna',"pygame","gtts","bs4",'helpLibs','guiLibs', 'lxml', 'win32process']

setup(
    name = "PySrs",
    description='Python Srs',
    version=__version__,
    options = {"build_exe": {
    'packages': packages,
    'include_files': include_files,
    'excludes': excludes,
    'include_msvcr': True,
}},
executables = [Executable("PySrs.pyw",base="Win32GUI")]
)