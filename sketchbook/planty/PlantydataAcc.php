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

$username="root";
$password="password";
$database="planty";
  
mysql_connect(localhost,$username,$password);
@mysql_select_db($database) or die( "Unable to select database");
  
$query="SELECT * FROM plantyLog";
$result=mysql_query($query);
  
$num=mysql_numrows($result);
  
mysql_close();
  
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

?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
	<title>untitled</title>
	<meta http-equiv="content-type" content="text/html;charset=utf-8" />
	<meta name="generator" content="Geany 1.27" />
</head>

<body>
	
</body>

</html>
