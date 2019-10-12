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
$row_cnt = $result->num_rows;

//$dir="/media/savestuff";
$temp = "/var/www/html/Images/hej.jpg";
$dir="var/www/html/Images";
$images = glob($dir . "/*.jpg");
 
//echo $images[count($images)-1]; 

?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
	<style>
		table, th, td {
			border: 1px solid black;
			border-collapse: collapse;
		}
	
	</style>
	<title>Planty</title>
	<meta http-equiv="content-type" content="text/html;charset=utf-8" />
	<meta name="generator" content="Geany 1.29" />
</head>

<body>
	<h1>Planty McPlantface</h1>
 	
 	<?php 
		echo "<table style=\"width:75%\">
				<tr> 
					<th>Date and time</th>
					<th>Plant</th>
					<th>Temperature</th>
					<th>Humidity</th>
					<th>Moisture</th>
					<th>Light</th>
					<th>Motor</th>
				</tr>";
		for ($x = 0; $x < $row_cnt; $x++) {
			
			$row = $result->fetch_array(MYSQLI_BOTH);
			$tempdate = $row["datetime"];
			$tempplant = $row["plant"];
			$temptemp = $row["temperature"];
			$temphum = $row["humidity"];
			$tempmois = $row["moisture"];
			$templight = $row["ALS"];
			$tempmotor = $row["motor"];
			echo 
			"<tr>
				<td>$tempdate</td>
				<td>$tempplant</td>
				<td>$temptemp</td>
				<td>$temphum</td>
				<td>$tempmois</td>
				<td>$templight</td>
				<td>$tempmotor</td>
			</tr>";
		}		
		echo "</table>";
		$result->free();
 	?>
	
</body>

</html>
