#!/usr/bin/env python

from time import sleep
from plantyData import PlantyData
import serial
import sys
import mysql.connector
from mysql.connector import errorcode

motor=-1
mois = -1
temp = -1
hum = -1
ALS = -1
plant = "default"

#plantycom.py duration power samples moisThres nightMode

try: 
	if(len(sys.argv) < 6):
		raise Exception("Not enough arguements")
	if(len(sys.argv) > 6):
		raise Exception("Too many arguements")

	#duration = 10000 #ms
	duration = int(sys.argv[1])
	#power = 99 #%
	power = int(sys.argv[2])
	#samples = 3
	samples = int(sys.argv[3])
	#moisThres = 400
	moisThres = int(sys.argv[4])
	nightMode = False
	
	if(int(sys.argv[5]) == 1):
		nightMode = True
	elif(int(sys.argv[5]) == 0):
		nightMode = False
	else:
		raise ValueError("nightMode must be equal to 0 or 1")	

except ValueError, e:
	print str(e)
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
	
except serial.SerialException, e:
	
	if "could not open port" in str(e):
		print "Port busy! Please change port"
		sys.exit()
	else:
		print str(e)
		
data = PlantyData(motor,mois,temp,hum,plant,ALS)
		
print "Plant: " + data.plant
#print type(data.plant)
print "Moisture: " + data.moisture
#print type(data.moisture)
print "Temperature: " + data.temperature
#print type(data.temperature)
print "Humidity: " + data.humidity
#print type(data.humidity)
print "Motor: " + data.motor
#print type(data.motor)
print "ALS: " + data.ALS
#print type(data.ALS)
print "Time stamp: " + str(data.timeStamp)
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
	

