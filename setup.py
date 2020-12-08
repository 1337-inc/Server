from cx_Freeze import setup, Executable 
  
setup(name = "Server" , 
      version = "1.0" , 
      description = "" , 
      executables = [Executable("server.py")])

