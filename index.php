
<?php
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
$plantsql="SELECT * FROM plantyLog order by datetime desc limit 48";
$plantresult = $conn->query($plantsql);
$plantrow_cnt = $plantresult->num_rows;

//$sql="SELECT * FROM plantyLog";
$camerasql="SELECT * FROM cameraLog order by datetime desc limit 10";
$cameraresult = $conn->query($camerasql);
$camerarow_cnt = $cameraresult->num_rows;

//$dir="/media/savestuff";
$temp = "/var/www/html/Images/hej.jpg";
$image = "2020-02-23T12:00:12.jpg";
$dir="/var/www/html/Images";
$images = glob($dir . "/*.jpg");

$test = ("Images/" . $image);

$image1 = str_replace("/var/www/html/","",$images[count($images)-1]); 
$image2 = str_replace("/var/www/html/","",$images[count($images)-2]); 
$image3 = str_replace("/var/www/html/","",$images[count($images)-3]); 
$image4 = str_replace("/var/www/html/","",$images[count($images)-4]); 

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
	
	<img src="<?php echo $image1 ?>" width="512" height="384" alt="image 1" align="top"/>
	<img src="<?php echo $image2 ?>" width="512" height="384" alt="image 2" align="top"/>
	<img src="<?php echo $image3 ?>" width="512" height="384" alt="image 3" align="top"/>
	<img src="<?php echo $image4 ?>" width="512" height="384" alt="image 3" align="top"/>

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
		for ($x = 0; $x < $plantrow_cnt; $x++) {
			
			$row = $plantresult->fetch_array(MYSQLI_BOTH);
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
		$plantresult->free();
 	?>
 	
 	<h2>Planty Camera</h2>
 	
 	<?php 
		echo "<table style=\"width:75%\">
				<tr> 
					<th>Date and time</th>
					<th>Original pixels</th>
					<th>Green pixels</th>
					<th>Green percentage</th>
				</tr>";
		for ($x = 0; $x < $camerarow_cnt; $x++) {
			
			$row = $cameraresult->fetch_array(MYSQLI_BOTH);
			$tempdate = $row["datetime"];
			$temporgpixel = $row["orgpixel"];
			$tempgreenpixel = $row["greenpixel"];
			$temppercent = $row["greenpercent"];
			echo 
			"<tr>
				<td>$tempdate</td>
				<td>$temporgpixel</td>
				<td>$tempgreenpixel</td>
				<td>$temppercent</td>
			</tr>";
		}		
		echo "</table>";
		$cameraresult->free();
 	?>
 	
 	<img src="https://s3.amazonaws.com/codecademy-content/courses/web-101/web101-image_brownbear.jpg" />
	
</body>

</html>
