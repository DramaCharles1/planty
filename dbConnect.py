import mysql.connector

class DBConnect:
	#static DB
	
	def __init__(self,host,user,password):
		self.host = host
		self.user = user
		self.password = password
		
	
	def connectDB(self):
		try:
			self.MySQL.connector.connect(
			host=self.host,
			user=self.user,
			password=self.password
			)
			
		except MySQL.connector.Error as e:
			print("Something went wrong: {}".format(err))

		
			
		
