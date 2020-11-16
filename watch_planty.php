<?php
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

//$sql="SELECT * FROM plantyLog";
$plantsql="SELECT * FROM plantyLog order by datetime desc limit 48";
$plantresult = $conn->query($plantsql);
$plantrow_cnt = $plantresult->num_rows;

//$sql="SELECT * FROM plantyLog";
$camerasql="SELECT * FROM cameraLog order by datetime desc limit 10";
$cameraresult = $conn->query($camerasql);
$camerarow_cnt = $cameraresult->num_rows;

$moisQuery="SELECT * FROM plantyLog order by datetime desc limit 24";
$moisResult = $conn->query($moisQuery);
$moisrow_cnt = $moisResult->num_rows;

?>

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
 	
 	<label for="year">year:</label>
	<select name="year" id="year">
		<option value="2020">2020</option>
		<option value="2019">2019</option>
	</select> 
	
	<label for="month">month:</label>
	<select name="month" id="month">
		<option value="1">1</option>
		<option value="2">2</option>
		<option value="3">3</option>
		<option value="4">4</option>
		<option value="5">5</option>
		<option value="6">6</option>
		<option value="7">7</option>
	</select> 
	
	<label for="day">day:</label>
	<select name="day" id="day">
		<option value="1">1</option>
		<option value="2">2</option>
		<option value="3">3</option>
		<option value="4">4</option>
		<option value="5">5</option>
		<option value="6">6</option>
		<option value="7">7</option>
		<option value="8">8</option>
		<option value="9">9</option>
	</select> 
	
</body>
