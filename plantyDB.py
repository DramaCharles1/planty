#DB class
from plantyData import PlantyData
import mysql.connector
from mysql.connector import errorcode

class PlantyDB:
	
	def __init__(self, host, user, password, database, table, plantData):
		self.host = host
		self.user = user
		self.password = password
		self.database = database
		self.plantData = plantData
		
		try:
			self.conn = mysql.connector.connect(
					host= self.host,
					user= self.user,
					password= self.password,
					database= self.database
					)
			self.cursor = self.conn.cursor()
			
		except mysql.connector.Error as e:
			print("Something went wrong: {}".format(e))
		
	def dataToDB(self):
		try:
	
			#INSERT INTO plantyLog (plant,motor,temperature,humidity,ALS,moisture,datetime) VALUES ("Test","Test","Test","Test","Test","Test","Test");
	
			insert_stmt = "INSERT INTO self.table (self.plantData.plant,self.plantData.motor,self.plantData.temperature,self.plantData.humidity,self.plantData.ALS,self.plantData.moisture,self.plantData.datetime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
	
			data = (self.plantData.plant,self.plantData.motor,self.plantData.temperature,self.plantData.humidity,self.plantData.ALS,self.plantData.moisture,self.plantData.timeStamp)
			myCursor.execute(insert_stmt, data)
			
			
		except mysql.connector.Error as e:
			print("Something went wrong: {}".format(e))

		
	def readLastEntry(table):
		try:
			get_stmt = "SELECT * FROM self.table VALUES %s" #Ändra här!
		
	def closeConnection(self):
		self.cursor.close()
		self.conn.commit()
		self.conn.close()
