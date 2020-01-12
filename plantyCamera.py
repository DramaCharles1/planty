import sys
import os
from picamera import PiCamera
from time import sleep
from shutil import copyfile

import cv2
import numpy as np

class plantyCamera:
	def __init__(self, picDir, picName, picCopyDir, lowGreen, highGreen):
		self.picDir = picDir
		self.picName = picName
		self.picCopyDir = picCopyDir
		self.fullPath = os.path.join(self.picDir, self.picName)
		self.fullCopyPath = os.path.join(self.picCopyDir, self.picName)
		self.takePic = False
		
		self.lowGreen = lowGreen
		self.highGreen = highGreen
		
		self.org_pixel = -1
		self.green_pixel = -1
		self.green_percentage = -1 
		
	# def __checkPicDir(self):
		# if not(os.path.isdir(self.picDir)):
			# self.takePic = False
		# else:
			# self.takePic = True
			
	def __checkPic(self):
		if not(os.path.isfile(self.fullPath)):
			self.takePic = False
		else:
			self.takePic = True
			
	def getPic(self):
		try:
			camera = PiCamera()

			camera.start_preview()
			sleep(3)
			camera.capture(self.fullPath)

			camera.stop_preview()
			
			self.__checkPic()
			
			if not(self.takePic):
				raise Exception("Could not find file: " + self.fullPath)
			
		except Exception as e:
			print(str(e))
			
	def copyPic(self):
		try:
			copyfile(self.fullPath ,self.fullCopyPath)
		except Exception as e:
			print(str(e))
			
	def greenCheck(self):	
		src = cv2.imread(self.fullPath)
		original = src
		
		hsv = cv2.cvtColor(src,cv2.COLOR_BGR2HSV)
		
		lower_green = np.array(self.lowGreen)
		upper_green = np.array(self.highGreen)
		
		mask1 = cv2.inRange(hsv, lower_green, upper_green)
		
		res1 = cv2.bitwise_and(src,src,mask=mask1)
		
		self.org_pixel = np.count_nonzero(original)
		self.green_pixel = np.count_nonzero(res1)
		self.green_percentage = round((1-(self.org_pixel-self.green_pixel)/self.org_pixel)*100,3)
		
		cv2.imwrite(self.picDir + '/' + 'res_'+self.picName, res1)
		#print(self.picDir + '/' + 'res_'+self.picName)
