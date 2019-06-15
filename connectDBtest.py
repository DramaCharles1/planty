import mysql.connector
from datetime import datetime

try:
	conn = mysql.connector.connect(
			host= 'localhost',
			user= 'root',
			password= 'password',
			database= 'planty'
			)
			
			
	print(conn)
	myCursor = conn.cursor()
	
	#INSERT INTO plantyLog (plant,motor,temperature,humidity,ALS,moisture,datetime) VALUES ("Test","Test","Test","Test","Test","Test","Test");
	
	insert_stmt = "INSERT INTO plantyLog (plant,motor,temperature,humidity,ALS,moisture,datetime) VALUES (%s,%s,%s,%s,%s,%s,%s)"
	
	data = ("Test2", "1", "26.00", "46.00", "0", "200", "test")
	myCursor.execute(insert_stmt, data)
	conn.commit()
	
	conn.close()
			
except mysql.connector.Error as e:
			print("Something went wrong: {}".format(e))
