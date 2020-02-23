from datetime import datetime
from plantyCamera import plantyCamera
import os
from shutil import copyfile
from xml.dom import minidom

xmlPath = "/home/pi/Repo/planty" 
xmlFile = "cameraData2.xml"

fullPath = os.path.join(xmlPath, xmlFile)

mydoc = minidom.parse(fullPath)

CameraDatas = mydoc.getElementsByTagName('cam_data') 
picd = CameraDatas[0].getElementsByTagName("pic_dir")[0].firstChild.data.strip()
picCopy = CameraDatas[0].getElementsByTagName("pic_copy_dir")[0].firstChild.data.strip()
		
lowerGreen = [int(CameraDatas[0].getElementsByTagName("lower_green")[0].getAttribute("l1")), int(CameraDatas[0].getElementsByTagName("lower_green")[0].getAttribute("l2")), int(CameraDatas[0].getElementsByTagName("lower_green")[0].getAttribute("l3"))]
upperGreen = [int(CameraDatas[0].getElementsByTagName("upper_green")[0].getAttribute("u1")), int(CameraDatas[0].getElementsByTagName("upper_green")[0].getAttribute("u2")), int(CameraDatas[0].getElementsByTagName("upper_green")[0].getAttribute("u3"))]
		

datime = datetime.now().replace(microsecond=0).isoformat()

picn = "2020-02-22T12:00:11.jpg"
picn = "2020-02-20T12:00:11.jpg"
picn = "2020-02-19T12:00:12.jpg"
#picn = "/media/pi/USB/2020-02-22T12:00:11.jpg"

plantCam = plantyCamera(picd, picn, picCopy, lowerGreen, upperGreen)

#plantCam.checkPicDir()

# if(plantCam.takePic is True):
	# print "ok"
# else:
	# print "not ok"

#plantCam.getPic()

#print("ok")	

#plantCam.copyPic()

#print("done copy")
print("pic: " + plantCam.fullPath)
print("pic copy: " + plantCam.fullCopyPath)

plantCam.greenCheck()

print("Original pixel: " + str(plantCam.org_pixel))
print("Green pixel: " + str(plantCam.green_pixel))
print("Green pixel percentage: " + str(plantCam.green_percentage))
