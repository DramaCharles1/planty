#Data class
from datetime import time

class PlantyData:
	
	def __init__(self, motor, moisture, temperature, humidity):
		self.motor = motor
		self.moisture = moisture
		self.temperature = temperature
		self.humidity = humidity
		self.dateAndTime = DateTime.now()
		
					
