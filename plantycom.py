#!/usr/bin/env python

from time import sleep
from plantyData import PlantyData
import os
import serial
import sys
#import mysql.connector
#from mysql.connector import errorcode
from xml.dom import minidom

motor=-1
mois = -1
temp = -1
hum = -1
ALS = -1
plant = "default"

#python3 plantycom.py /home/pi/Repo/planty cameraData.xml 1
#python3 plantycom.py xmlPath xmlFile takepic

try:
	
	if(len(sys.argv) < 4):
		raise Exception("Not enough arguements")
	if(len(sys.argv) > 4):
		raise Exception("Too many arguements")
		
	xmlPath = str(sys.argv[1])
	xmlFile = str(sys.argv[2])

	fullPath = os.path.join(xmlPath, xmlFile)
	
	mydoc = minidom.parse(fullPath)
	plantyDatas = mydoc.getElementsByTagName('planty_data') 
	
	duration = plantyDatas[0].getElementsByTagName("duration")[0].firstChild.data.strip()
	power = plantyDatas[0].getElementsByTagName("power")[0].firstChild.data.strip()
	samples = plantyDatas[0].getElementsByTagName("samples")[0].firstChild.data.strip()
	moisThres = plantyDatas[0].getElementsByTagName("mois_thres")[0].firstChild.data.strip()
	nightModetmp = plantyDatas[0].getElementsByTagName("nightmode")[0].firstChild.data.strip()
	
	if(nightModetmp == 1):
		nightMode = True
	elif(nightModetmp == 0):
		nightMode = False
		
	if(int(sys.argv[3]) == 1):
		#Take Pic
		CameraDatas = mydoc.getElementsByTagName('cam_data') 
		picDir = CameraDatas[0].getElementsByTagName("pic_dir")[0].firstChild.data.strip()
		picCopyDir = CameraDatas[0].getElementsByTagName("pic_copy_dir")[0].firstChild.data.strip()
		
		l1 = CameraDatas[0].getElementsByTagName("lower_green")[0].getAttribute("l1")
		lowerGreen = [CameraDatas[0].getElementsByTagName("lower_green")[0].getAttribute("l1"), CameraDatas[0].getElementsByTagName("lower_green")[0].getAttribute("l2"), CameraDatas[0].getElementsByTagName("lower_green")[0].getAttribute("l3")]
		upperGreen = [CameraDatas[0].getElementsByTagName("upper_green")[0].getAttribute("u1"), CameraDatas[0].getElementsByTagName("upper_green")[0].getAttribute("u2"), CameraDatas[0].getElementsByTagName("upper_green")[0].getAttribute("u3")]
		
	elif(int(sys.argv[3]) == 0):
		#Do not take Pic
		CameraDatas = 0
	else:
		raise ValueError("Camera option must be set to 0 or 1")	
	
	#Ta bort innan test!!!
	sys.exit()	
	
except ValueError as e:
	print(str(e))
	sys.exit()	

def checkOK(rec):
	ok = "OK"
	err = "ERR"
	
	if("OK" in rec):
		return True
	elif ("ERR" in rec):
		return False
	else:
		raise Exception("Not a valid command recieved" + "rec: " + rec)
	
def getCommandValue(rec):
	separator = ['=',',','\n']
	
	rec = rec.replace('=',',')
	value = rec.split(',')
	
	return value[1]

#Main
try:
	ser = serial.Serial('/dev/ttyACM0', 57600) 
	
	sleep(2)
	
	ser.write("MOTR=0"+'\n')
	sleep(0.5)
	
	ser.write("TEMP=2"+'\n')
	sleep(0.5)

	while ser.in_waiting > 0:
		rec = ser.readline()
		
	if not(checkOK(rec)):
		raise Exception("Command: " + rec + "returned an error")
		
	hum = getCommandValue(rec)
	
	rec = ""
	
	ser.write("PLANT=1"+'\n')
	sleep(0.5)

	while ser.in_waiting > 0:
		rec = ser.readline()
	
	if not(checkOK(rec)):
		raise Exception("Command: " + rec + "returned an error")
				
	plant = getCommandValue(rec)
	
	rec = ""
	
	ser.write("MOIS=" + str(samples) +'\n')
	sleep(5)

	while ser.in_waiting > 0:
		rec = ser.readline()
		
	if not(checkOK(rec)):
		raise Exception("Command: " + rec + "returned an error")
		
	mois = getCommandValue(rec)
	
	rec = ""
	
	ser.write("TEMP=1"+'\n')
	sleep(0.5)

	while ser.in_waiting > 0:
		rec = ser.readline()
		
	if not(checkOK(rec)):
		raise Exception("Command: " + rec + "returned an error")
		
	temp = getCommandValue(rec)
	
	rec = ""	
	
	#ser.write("MOTR=2"+'\n')
	#sleep(0.5)

	#while ser.in_waiting > 0:
	#	rec = ser.readline()
		
	#if not(checkOK(rec)):
	#	raise Exception("Command: " + rec + "returned an error")
		
	#motor = getCommandValue(rec)
	
	#rec = ""
	
	ser.write("ALS"+'\n')
	sleep(0.5)

	while ser.in_waiting > 0:
		rec = ser.readline()
		
	if not(checkOK(rec)):
		raise Exception("Command: " + rec + "returned an error")
		
	ALS = getCommandValue(rec)
	
	rec = ""	
	
	if(float(mois) < moisThres and nightMode == True):
		
		ser.write("MOTR=1,"+str(power)+","+str(duration)+'\n')
		motor = str(power)+","+str(duration)
		sleep(duration/1000)

	elif (float(mois) > moisThres and nightMode == True):
		motor = "0"
	else:
		motor = "-1"
	ser.flush()
	ser.close()
	
except serial.SerialException as e:
	
	if "could not open port" in str(e):
		print("Port busy! Please change port")
		sys.exit()
	else:
		print(str(e))
		
data = PlantyData(motor,mois,temp,hum,plant,ALS)
		
print("Plant: " + data.plant)
#print type(data.plant)
print("Moisture: " + data.moisture)
#print type(data.moisture)
print("Temperature: " + data.temperature)
#print type(data.temperature)
print("Humidity: " + data.humidity)
#print type(data.humidity)
print("Motor: " + data.motor)
#print type(data.motor)
print("ALS: " + data.ALS)
#print type(data.ALS)
print("Time stamp: " + str(data.timeStamp))
#print type(data.timeStamp)

try:

	conn = mysql.connector.connect(
			host= 'localhost',
			user= 'root',
			password= 'password',
			database= 'planty'
			)
			
	#print(conn)
	myCursor = conn.cursor()
	
	#INSERT INTO plantyLog (plant,motor,temperature,humidity,ALS,moisture,datetime) VALUES ("Test","Test","Test","Test","Test","Test","Test");
	
	insert_stmt = "INSERT INTO plantyLog (plant,motor,temperature,humidity,ALS,moisture,datetime) VALUES (%s,%s,%s,%s,%s,%s,%s)"
	
	data = (data.plant,data.motor,data.temperature,data.humidity,data.ALS,data.moisture,data.timeStamp)
	myCursor.execute(insert_stmt, data)
	myCursor.close()
	
	conn.commit()
	conn.close()
			
except mysql.connector.Error as e:
	print("Something went wrong: {}".format(e))
	

