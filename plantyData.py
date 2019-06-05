#Data class
from datetime import datetime

class PlantyData:
	
	def __init__(self, motor, moisture, temperature, humidity, plant):
		self.motor = motor
		self.moisture = moisture
		self.temperature = temperature
		self.humidity = humidity
		self.plant = plant
		self.timeStamp = datetime.now().replace(microsecond=0).isoformat()
		
		#self.dateAndTime = DateTime.now()
		
					
