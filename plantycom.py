from time import sleep
from plantyData import PlantyData
import serial
import sys

motor=-1
mois = -1
temp = -1
hum = -1
plant = "default"

def checkOK(rec):
	ok = "OK"
	err = "ERR"
	
	if("OK" in rec):
		return True
	elif ("ERR" in rec):
		return False
	else:
		raise Exception("Not a valid command recieved")
	
def getCommandValue(rec):
	separator = ['=',',','\n']
	
	rec = rec.replace('=',',')
	value = rec.split(',')
	
	return value[1]

#Main
try:
	ser = serial.Serial('/dev/ttyACM1', 57600) 
	
	sleep(2)
	
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
	
	ser.write("MOIS"+'\n')
	sleep(0.5)

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
	
	ser.write("MOTR=2"+'\n')
	sleep(0.5)

	while ser.in_waiting > 0:
		rec = ser.readline()
		
	if not(checkOK(rec)):
		raise Exception("Command: " + rec + "returned an error")
		
	motor = getCommandValue(rec)
	
	rec = ""
	
	#def __init__(self, motor, moisture, temperature, humidity, plant):			
	data = PlantyData(motor,mois,temp,hum,plant)
	
	ser.flush()
	ser.close()
	
except serial.SerialException, e:
	
	if "could not open port" in str(e):
		print "Port busy! Please change port"
		sys.exit()
	else:
		print str(e)
		
print "Plant: " + data.plant
print "Moisture: " + data.moisture
print "Temperature: " + data.temperature
print "Humidity: " + data.humidity
print "Motor: " + data.motor
print "Time stamp: " + str(data.timeStamp)
