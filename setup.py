import sys
from cx_Freeze import setup, Executable 

base = None
if sys.platform == "win32":
      base = "Win32GUI"

setup(name = "Server" , 
      version = "1.3" , 
      description = "A Support Application For Captain!!, A Simple Desktop Game." , 
      executables = [Executable("run.py", base=base)])
