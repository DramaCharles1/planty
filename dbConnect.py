from mysql.connector import MySQLConnection, Error

class DBConnect:
	#static DB
	
	def __init__(self,host,user,password,table):
		self.host = host
		self.user = user
		self.password = password	
		self.table = table
			
	
	def connectDB(self):
		try:
			self.MySQL.connector.connect(
			host=self.host,
			user=self.user,
			password=self.password
			table=self.table
			)
			
		except MySQL.connector.Error as e:
			print("Something went wrong: {}".format(err))

		
			
		
