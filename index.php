<?php
/*
 * index.php
 * 
 * Copyright 2019  <pi@raspberrypi>
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 * 
 * 
 */

//echo file_get_contents("/home/pi/planty/Header.html");

//echo "Hello World!";

$servername = "localhost";
$username="root";
$password="password";
$database="planty";
  
//mysql_connect(localhost,$username,$password);
$conn = new mysqli($servername, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
//echo "Connected successfully \n";
  
//$sql="SELECT * FROM plantyLog";
$sql="SELECT * FROM plantyLog order by datetime desc limit 24";
$result = $conn->query($sql);

$dir="/media/savestuff";
$images = glob($dir . "/*.jpg");
 
$images[count($images)-1]; 

//echo '<img src="file:///home/pi/image.jpg" />'

?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
	<title>Planty</title>
	<meta http-equiv="content-type" content="text/html;charset=utf-8" />
	<meta name="generator" content="Geany 1.29" />
</head>

<body>
	<h1>Planty McPlantface</h1>
	
	<p> <?php echo $images[count($images)-1];?></p>
	
	<img src="https://s3.amazonaws.com/codecademy-content/courses/web-101/web101-image_brownbear.jpg" />
	<img src="/image.jpg" />
	
	
</body>

</html>
