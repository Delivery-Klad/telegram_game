from cx_Freeze import setup, Executable

base = None
executables = [Executable("bot.py", base=base)]

packages = ["datetime", "telebot", "psycopg2", "os", "PIL", "base64"]
options = {'build_exe': {'packages': packages, }, }

setup(name="bot", options=options, version="2.28",
      description='description', executables=executables)
