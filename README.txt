Automatic watering system using Arduino Uno

Install mysql
pip3 install mysql-connector-python
sudo apt-get install php-mysql
sudo apt-get install mariadb-client-10.0
sudo apt-get install mariadb-server-10.0

Create new user mariadb, grants permission for php scripts
DROP USER 'root'@'localhost';
CREATE USER 'root'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION;

Create database
CREATE DATABASE planty;
CREATE TABLE plantyLog(plant VARCHAR(10) NOT NULL, motor VARCHAR(10) NOT NULL, temperature VARCHAR(10) NOT NULL, humidity VARCHAR(10) NOT NULL, ALS VARCHAR(10) NOT NULL, moisture VARCHAR(10) NOT NULL, datetime DATETIME NOT NULL)
CREATE TABLE cameraLog(orgpixel INT NOT NULL, greenpixel INT NOT NULL, greenpercent FLOAT NOT NULL, datetime DATETIME NOT NULL)
create table inputData(duration INT NOT NULL, power INT NOT NULL, samples INT NOT NULL, moisThres INT NOT NULL, lightSetPoint INT NOT NULL, maxLight INT NOT NULL, datetime DATETIME NOT NULL);
Example: 
INSERT INTO table_name (plant,motor,temperature,humidity,ALS,moisture,datetime) VALUES ("Basil","-1","24.00","46.00","69","43.00","2019-12-19T22:07:25") 

install apache
sudo apt install apache2
sudo chown -R pi:www-data /var/www/html/
sudo chmod -R 775 /var/www/html/

install php7
apt-get -y install php7.0 libapache2-mod-php7.0

Arduino 
Install latest Linux ARM 32bit version

Install matplotlib
pip install matplotlib

##plantycom.py duration power samples moisThres nightMode
#SAVE image handling to log!
#*/60 * * * * python planty/plantycom.py >> ~/cron.log 2>&1
*/60 8-23 * * * python planty/plantycom.py 10000 99 3 400 1 >> ~/cron.log 2>&1
*/60 0-7 * * * python planty/plantycom.py 10000 99 3 400 0 >> ~/cron.log 2>&1
