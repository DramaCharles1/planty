
from datetime import datetime
from plantyCamera import plantyCamera
import os
from shutil import copyfile

datime = datetime.now().replace(microsecond=0).isoformat()

picd = '/media/pi/USB'
picCopy = '/var/www/html/Images'
picn = str(datime) + ".jpg"

plantCam = plantyCamera(picd, picn, picCopy)

#plantCam.checkPicDir()

# if(plantCam.takePic is True):
	# print "ok"
# else:
	# print "not ok"

plantCam.getPic()

print("ok")	

plantCam.copyPic()

print("done copy")
print("pic: " + plantCam.fullPath)
print("pic copy: " + plantCam.fullCopyPath)

plantCam.greenCheck()

print("Original pixel: " + str(plantCam.org_pixel))
print("Green pixel: " + str(plantCam.green_pixel))
print("Green pixel percentage: " + str(plantCam.green_percentage))

print(str(type(plantCam.org_pixel)))
print(str(type(plantCam.green_pixel)))
print(str(type(plantCam.green_percentage)))
