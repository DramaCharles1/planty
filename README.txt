Automatic watering system using Arduino Uno

Install mysql
sudo apt-get install mysql-server
pip3 install mysql-connector-python

install apache
sudo apt install apache2
sudo chown -R pi:www-data /var/www/html/
sudo chmod -R 775 /var/www/html/

install php7
apt-get -y install php7.0 libapache2-mod-php7.0

Arduino 
Install latest Linux ARM 32bit version

##plantycom.py duration power samples moisThres nightMode
#SAVE image handling to log!
#*/60 * * * * python planty/plantycom.py >> ~/cron.log 2>&1
*/60 8-23 * * * python planty/plantycom.py 10000 99 3 400 1 >> ~/cron.log 2>&1
*/60 0-7 * * * python planty/plantycom.py 10000 99 3 400 0 >> ~/cron.log 2>&1