#!/usr/bin/env python

from time import sleep
from plantyData import PlantyData
from plantyCamera import plantyCamera
import os
import serial
import serial.tools.list_ports
import sys
import mysql.connector
from mysql.connector import errorcode
from xml.dom import minidom
from shutil import copyfile
from plots import Plots
import matplotlib.pyplot as plt

motor=-1
mois = -1
temp = -1
hum = -1
ALS = -1
plant = "default"

nightMode = False
takePic = False

#python plantycom.py /home/pi/Repo/planty cameraData.xml 1 0
#python plantycom.py xmlPath xmlFile takepic nightmode

try:
	
	if(len(sys.argv) < 5):
		raise Exception("Not enough arguements")
	if(len(sys.argv) > 5):
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
	setpoint = plantyDatas[0].getElementsByTagName("setpoint")[0].firstChild.data.strip()
	maxControl = plantyDatas[0].getElementsByTagName("max_control")[0].firstChild.data.strip()

	#nightModetmp = plantyDatas[0].getElementsByTagName("nightmode")[0].firstChild.data.strip()
	
	if(int(sys.argv[4]) == 1):
		nightMode = True
	elif(int(sys.argv[4]) == 0):
		nightMode = False
	else:
		raise ValueError("Nightmode option must be set to 0 or 1")	
		
	if(int(sys.argv[3]) == 1):
		#Take Pic
		takePic = True
		CameraDatas = mydoc.getElementsByTagName('cam_data') 
		picDir = CameraDatas[0].getElementsByTagName("pic_dir")[0].firstChild.data.strip()
		picCopyDir = CameraDatas[0].getElementsByTagName("pic_copy_dir")[0].firstChild.data.strip()
		
		#l1 = CameraDatas[0].getElementsByTagName("lower_green")[0].getAttribute("l1")
		lowerGreen = [int(CameraDatas[0].getElementsByTagName("lower_green")[0].getAttribute("l1")), int(CameraDatas[0].getElementsByTagName("lower_green")[0].getAttribute("l2")), int(CameraDatas[0].getElementsByTagName("lower_green")[0].getAttribute("l3"))]
		upperGreen = [int(CameraDatas[0].getElementsByTagName("upper_green")[0].getAttribute("u1")), int(CameraDatas[0].getElementsByTagName("upper_green")[0].getAttribute("u2")), int(CameraDatas[0].getElementsByTagName("upper_green")[0].getAttribute("u3"))]
		
	elif(int(sys.argv[3]) == 0):
		#Do not take Pic
		CameraDatas = 0
	else:
		raise ValueError("Camera option must be set to 0 or 1")	
	
	
except ValueError as e:
	print(str(e))
	sys.exit()	

def checkOK(rec):
	ok = "OK"
	err = "ERR"
	
	if("OK" in str(rec)):
		return True
	elif ("ERR" in str(rec)):
		return False
	else:
		raise Exception("Not a valid command recieved" + "rec: " + rec)
	
def getCommandValue(rec):
	separator = ['=',',','\n']
	
	rec = str(rec).replace('=',',')
	value = str(rec).split(',')
	
	return value[1]

#Main
try:
	
	portlist = serial.tools.list_ports.comports(include_links=False)
	arduinoport = ""
	
	for port in portlist:
		if "Genuino" in port.description:
			arduinoport = port.device
			
	if arduinoport == "":
		raise Exception("Could not find any arduino")
	
	ser = serial.Serial(arduinoport, 57600) 
	
	sleep(2)
	
	ser.write(("MOTR=0"+'\n').encode('utf-8'))
	sleep(0.5)
	
	ser.write(("TEMP=2"+'\n').encode('utf-8'))
	sleep(0.5)

	while ser.in_waiting > 0:
		rec = ser.readline()
		
	if not(checkOK(rec)):
		raise Exception("Command: " + rec + "returned an error")
		
	hum = getCommandValue(rec)
	
	rec = ""
	
	ser.write(("PLANT=1"+'\n').encode('utf-8'))
	sleep(0.5)

	while ser.in_waiting > 0:
		rec = ser.readline()
	
	if not(checkOK(rec)):
		raise Exception("Command: " + str(rec) + "returned an error")
				
	plant = getCommandValue(rec)
	
	rec = ""
	
	ser.write(("MOIS=" + str(samples) +'\n').encode('utf-8'))
	sleep(5)

	while ser.in_waiting > 0:
		rec = ser.readline()
		
	if not(checkOK(rec)):
		raise Exception("Command: " + rec + "returned an error")
		
	mois = getCommandValue(rec)
	
	rec = ""
	
	ser.write(("TEMP=1"+'\n').encode('utf-8'))
	sleep(0.5)

	while ser.in_waiting > 0:
		rec = ser.readline()
		
	if not(checkOK(rec)):
		raise Exception("Command: " + rec + "returned an error")
		
	temp = getCommandValue(rec)
	
	rec = ""	
	
	ser.write(("ALS"+'\n').encode('utf-8'))
	sleep(0.5)

	while ser.in_waiting > 0:
		rec = ser.readline()
		
	if not(checkOK(rec)):
		raise Exception("Command: " + rec + "returned an error")
		
	ALS = getCommandValue(rec)
	
	rec = ""
	
	
	if(float(mois) < float(moisThres) and nightMode == False):
		
		ser.write(("MOTR=1,"+str(power)+","+str(duration)+'\n').encode('utf-8'))
		motor = str(power)+","+str(duration)
		sleep(int(duration)/1000)

	elif (float(mois) >= float(moisThres) and nightMode == False):
		motor = "0"
	else:
		motor = "-1"
		
	data = PlantyData(motor,mois,temp,hum,plant,ALS)
	
	if(nightMode):
		ser.write(("PI=1"+'\n').encode('utf-8'))
		sleep(0.5)

		while ser.in_waiting > 0:
			rec = ser.readline()
		
		if not(checkOK(rec)):
			raise Exception("Command: " + rec + "returned an error")
		
		PI = getCommandValue(rec)
		
		if(int(PI) == 1):
			ser.write(("PI=2,0" + '\n').encode('utf-8'))
			sleep(0.5)

			while ser.in_waiting > 0:
				rec = ser.readline()
		
			if not(checkOK(rec)):
				raise Exception("Command: " + rec + "returned an error")
	else:
		maxControl
		ser.write(("PISET=2,1.0,1.75,200," + maxControl + '\n').encode('utf-8'))
		sleep(0.5)

		while ser.in_waiting > 0:
			rec = ser.readline()
		
		if not(checkOK(rec)):
			raise Exception("Command: " + rec + "returned an error")
		
		ser.write(("PI=2,1," + setpoint + '\n').encode('utf-8'))
		sleep(0.5)

		while ser.in_waiting > 0:
			rec = ser.readline()
		
		if not(checkOK(rec)):
			raise Exception("Command: " + rec + "returned an error")
	
	if(takePic):
		
		rec = ""
		
		ser.write(("PI=" + "2,0" +'\n').encode('utf-8'))
		sleep(5)
	
		ser.write(("LED=" + "1,2,255" +'\n').encode('utf-8'))
		sleep(5)

		while ser.in_waiting > 0:
			rec = ser.readline()
		
		if not(checkOK(rec)):
			raise Exception("Command: " + rec + "returned an error")
		
		cam = plantyCamera(str(picDir),str(data.timeStamp) + ".jpg",str(picCopyDir),lowerGreen,upperGreen)
		cam.getPic()
		cam.copyPic()
		cam.greenCheck()
		
		rec = ""
	
		ser.write(("LED=" + "1,0,0" +'\n').encode('utf-8'))
		sleep(5)
		
		ser.write(("PI=" + "2,1," + setpoint +'\n').encode('utf-8'))
		sleep(5)

		while ser.in_waiting > 0:
			rec = ser.readline()
		
		if not(checkOK(rec)):
			raise Exception("Command: " + rec + "returned an error")
	
	ser.flush()
	ser.close()
	
except serial.SerialException as e:
	
	if "could not open port" in str(e):
		print("Port busy! Please change port")
		sys.exit()
	else:
		print(str(e))
		
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

if(takePic):
	print("Original pixel: " + str(cam.org_pixel))
	print("Green pixels: " + str(cam.green_pixel))
	print("Green percentage: " + str(cam.green_percentage))

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
	logData = (data.plant,data.motor,data.temperature,data.humidity,data.ALS,data.moisture,data.timeStamp)
	myCursor.execute(insert_stmt, logData)	
	
	if(takePic):
		insert_stmt = "INSERT INTO cameraLog (orgpixel,greenpixel,greenpercent,datetime) VALUES (%s,%s,%s,%s)"
		logCamData = (cam.org_pixel,cam.green_pixel,cam.green_percentage,data.timeStamp)
		myCursor.execute(insert_stmt, logCamData)
		
		insertDataStmt = "INSERT INTO inputData(duration,power,samples,moisThres,lightSetPoint,maxLight,datetime) VALUES (%s,%s,%s,%s,%s,%s,%s)"
		logInputData = (duration,power,samples,moisThres,setpoint,maxControl,data.timeStamp)
		myCursor.execute(insertDataStmt, logInputData)	
	
	mois_query = "select moisture, datetime from plantyLog order by datetime desc limit 24"
	myCursor.execute(mois_query)	
	dataMois = myCursor.fetchall()
	
	xmois = []
	ymois = []
	for entry in dataMois:
		xmois.append(entry[1])
		ymois.append(float(entry[0]))
		
	mois_queryWeek = "select moisture, datetime from plantyLog order by datetime desc limit 168"
	myCursor.execute(mois_queryWeek)	
	dataMoisWeek = myCursor.fetchall()
	
	xmoisWeek = []
	ymoisWeek = []
	for entry in dataMoisWeek:
		xmoisWeek.append(entry[1])
		ymoisWeek.append(float(entry[0]))	
		
	MoisThres_query = "select moisThres from inputData order by datetime desc limit 1"
	myCursor.execute(MoisThres_query)
	moisThresVal = myCursor.fetchall()[0][0]
	
	y2mois = []
	for x in range(len(ymois)):
		y2mois.append(float(moisThresVal))
		
	y2moisWeek = []
	for x in range(len(ymoisWeek)):
		y2moisWeek.append(float(moisThresVal))
		
	Green_query = "select greenpercent, datetime from cameraLog order by datetime desc limit 7"
	myCursor.execute(Green_query)	
	dataGreen = myCursor.fetchall()
	
	xgreen = []
	ygreen = []
	for entry in dataGreen:
		xgreen.append(entry[1])
		ygreen.append(float(entry[0]))
		
	Green_queryMonth = "select greenpercent, datetime from cameraLog order by datetime desc limit 30"
	myCursor.execute(Green_queryMonth)	
	dataGreenMonth = myCursor.fetchall()
	
	xgreenMonth = []
	ygreenMonth = []
	for entry in dataGreenMonth:
		xgreenMonth.append(entry[1])
		ygreenMonth.append(float(entry[0]))
		
	dataLight_query = "select ALS, datetime from plantyLog order by datetime desc limit 24"
	myCursor.execute(dataLight_query)	
	dataLight = myCursor.fetchall()
	
	xlight = []
	ylight = []
	for entry in dataLight:
		xlight.append(entry[1])
		ylight.append(float(entry[0]))
		
	dataLight_queryWeek = "select ALS, datetime from plantyLog order by datetime desc limit 168"
	myCursor.execute(dataLight_queryWeek)	
	dataLightWeek = myCursor.fetchall()
	
	xlightWeek = []
	ylightWeek = []
	for entry in dataLightWeek:
		xlightWeek.append(entry[1])
		ylightWeek.append(float(entry[0]))
	
	myCursor.close()
	
	conn.commit()
	conn.close()
			
except mysql.connector.Error as e:
	print("Something went wrong: {}".format(e))
	
moisPlotName  = "/media/pi/USB/" + "MoisturePlot.png"
moisPlotCopy = "/var/www/html/" + "MoisturePlot.png"
moisPlot = Plots(xmois,y2mois,ymois,"24 hours","Moisture",moisPlotName,"moisture low limit","moisture")
moisPlot.Create2linePlot()
copyfile(moisPlotName,moisPlotCopy)

moisPlotNameWeek  = "/media/pi/USB/" + "MoisturePlotWeek.png"
moisPlotCopyWeek = "/var/www/html/" + "MoisturePlotWeek.png"
moisPlotWeek = Plots(xmoisWeek,y2moisWeek,ymoisWeek,"Week","Moisture",moisPlotNameWeek,"moisture low limit","moisture")
moisPlotWeek.Create2linePlot()
copyfile(moisPlotNameWeek,moisPlotCopyWeek)

greenPlotName  = "/media/pi/USB/" + "GreenPlot.png"
greenPlotCopy = "/var/www/html/" + "GreenPlot.png"
greenPlot = Plots(xgreen,ygreen,[],"Week","Growth (%)",greenPlotName,"Growth (%)","")
greenPlot.CreatelinePlot()
copyfile(greenPlotName,greenPlotCopy)

greenPlotNameMonth  = "/media/pi/USB/" + "GreenPlotMonth.png"
greenPlotCopyMonth = "/var/www/html/" + "GreenPlotMonth.png"
greenPlotMonth = Plots(xgreenMonth,ygreenMonth,[],"30 days","Growth (%)",greenPlotNameMonth,"Growth (%)","")
greenPlotMonth.CreatelinePlot()
copyfile(greenPlotNameMonth,greenPlotCopyMonth)

lightPlotName  = "/media/pi/USB/" + "LightPlot.png"
lightPlotCopy = "/var/www/html/" + "LightPlot.png"
lightPlot = Plots(xlight,ylight,[],"24 hours","Light",lightPlotName,"Light","")
lightPlot.CreatelinePlot()
copyfile(lightPlotName,lightPlotCopy)

lightPlotNameWeek  = "/media/pi/USB/" + "LightPlotWeek.png"
lightPlotCopyWeek = "/var/www/html/" + "LightPlotWeek.png"
lightPlotWeek = Plots(xlightWeek,ylightWeek,[],"Week","Light",lightPlotNameWeek,"Light","")
lightPlotWeek.CreatelinePlot()
copyfile(lightPlotNameWeek,lightPlotCopyWeek)
