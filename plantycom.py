from time import sleep
from plantyData import PlantyData
import serial


ser = serial.Serial('/dev/ttyACM0', 9600) # Establish the connection on a specific port
#counter = 32 # Below 32 everything in ASCII is gibberish
ser.flush()
sleep(1)

data = PlantyData(0,0,25,40)

print "motor: " + data.motor

	

while ser.in_waiting > 0:
	print ser.readline()
	sleep(1)
	
ser.write("MOIS"+'\n')
sleep(1)

while ser.in_waiting > 0:
	print ser.readline()
	sleep(1)

#while True:
#     counter +=1
#     ser.write(str(chr(counter))) # Convert the decimal number to ASCII then send it to the Arduino
#     print ser.readline() # Read the newest output from the Arduino
#     sleep(1) # Delay for one tenth of a second
#     if counter == 255:
#		counter = 32
