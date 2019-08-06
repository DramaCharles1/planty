import sys
import os
from picamera import PiCamera
from time import sleep

class plantyCamera:
	def __init__(self, picDir, picName):
		self.picDir = picDir
		self.picName = picName
		self.takePic = True
		
	def checkPicDir(self):
		if not(os.path.isdir(self.picDir)):
			self.takePic = False
			
	def getPic(self):
		try:
			camera = PiCamera()

			camera.start_preview()
			sleep(3)
			camera.capture(os.path.join(self.picDir, self.picName))

			camera.stop_preview()
			
		except Exception, e:
			print str(e)
