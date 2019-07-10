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

duration = 10000 #ms
power = 99 #%
samples = 5

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
	
	if(float(mois) < 400):
		
		#ser.write("MOTR=1,99,5000"+'\n')
		
		ser.write("MOTR=1,"+str(power)+","+str(duration)+'\n')
		
		#motor = "99,5000"
		motor = str(power)+","+str(duration)

		sleep(duration/1000)
		
		#while ser.in_waiting > 0:
		#	rec = ser.readline()
			
		#print rec
		
		#if not(checkOK(rec)):
		#	raise Exception("Command: " + rec + "returned an error")
	else:
		motor = "0"
	ser.flush()
	ser.close()
	
except serial.SerialException, e:
	
	if "could not open port" in str(e):
		print "Port busy! Please change port"
		sys.exit()
	else:
		print str(e)
	
#def __init__(self, motor, moisture, temperature, humidity, plant):			
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
	

