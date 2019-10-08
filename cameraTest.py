
from datetime import datetime
from plantyCamera import plantyCamera
import os
from shutil import copyfile

datime = datetime.now().replace(microsecond=0).isoformat()

picd = '/media/savestuff'
picCopy = '/var/www/html/Images'
picn = str(datime) + ".jpg"

plantCam = plantyCamera(picd, picn)

plantCam.checkPicDir()

if(plantCam.takePic is True):
	print "ok"
else:
	print "not ok"

plantCam.getPic()

print "end"	

copyfile(os.path.join(picd, picn),os.path.join(picCopy, picn))

print "done copy"
