<?php
/*
 * PlantydataAcc.php
 * 
 * Copyright 2019 Richard <richard@Henry>
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
echo "Connected successfully \n";
  
//$sql="SELECT * FROM plantyLog";
$sql="SELECT * FROM plantyLog order by datetime desc limit 24";
$result = $conn->query($sql);

echo "Plant Motor Temperature Humidity ALS Moisture Datetime\n";

while ($row = $result->fetch_assoc()) {
        printf ("%s %s %s %s %s %s %s\n", $row["plant"], $row["motor"], $row["temperature"], $row["humidity"], $row["ALS"], $row["moisture"], $row["datetime"]);
    }

$result->free();
  
$conn->close();
/*  
$tempValues = array();
  
$i=0;
while ($i < $num)
{
        $dateAndTemps = array();
        $datetime = mysql_result($result,$i,"datetime");
        $temp = mysql_result($result,$i,"temperature");
  
        $dateAndTemps["datetime"] = $datetime;
        $dateAndTemps["Temp"] = $temp;
  
        $tempValues[$i]=$dateAndTemps;
        $i++;
}
  
echo json_encode($tempValues);
*/
?>
