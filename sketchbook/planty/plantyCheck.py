import cv2
import numpy as np
import sys
import os

#python plantyCheck.py path image
#python3 plantyCheck.py /home/richard green_duck.jpg
imagePath = sys.argv[1] 
imageFile = sys.argv[2]

try:
	os.chdir(imagePath)
	
	if(os.path.isfile(imageFile) == False):
		raise FileNotFoundError("Could not find image")
except FileExistsError:
	print("Could not find image")
	sys.exit(0)	
	
#test
dirpath = os.getcwd()
print("current directory is : " + dirpath)
foldername = os.path.basename(dirpath)
print("Directory name is : " + foldername) 

src = cv2.imread(imagePath + "/" + imageFile)
original = src

#get size
dimensions = original.shape
height = dimensions[0]
width = dimensions[1]

size = height*width

print('Image Height       : ',height)
print('Image Width        : ',width) 

hsv = cv2.cvtColor(src,cv2.COLOR_BGR2HSV)

#lower_green = np.array([65,60,60])
lower_green = np.array([65,60,60])
#upper_green = np.array(80,255,255])
upper_green = np.array([80,255,255])
mask1 = cv2.inRange(hsv, lower_green, upper_green)

res1 = cv2.bitwise_and(src,src,mask=mask1)

org_pixel = np.count_nonzero(original)
#org_pixel = cv2.countNonZero(original)
green_pixel = np.count_nonzero(res1)
#green_pixel = cv2.countNonZero(res1)

green_percentage = round((1-(org_pixel-green_pixel)/org_pixel)*100,3)

print(org_pixel)
print(green_pixel)
print(green_percentage)

cv2.imwrite('3'+imageFile, res1)

##Test
#cv2.imshow('imageres',res1)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
