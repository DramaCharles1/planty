<?php
//phpinfo();
require_once ('/etc/php/7.3/jpgraph/src/jpgraph.php');
require_once ('/etc/php/7.3/jpgraph/src/jpgraph_line.php');

//$ydata = array(11,3,8,12,5,1,9,13,5,7);

//$graph = new Graph(350,250);
//$graph->SetScale('textlin');

//$lineplot=new LinePlot($ydata);
//$lineplot->SetColor('blue');

//$graph->Add($lineplot);

//$graph->Stroke();
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

$x_axis = array();
$y_axis = array();
$i = 0;

$moisQuery="SELECT * FROM plantyLog order by datetime desc limit 24";
$moisResult = $conn->query($moisQuery);
$moisrow_cnt = $moisResult->num_rows;


while($row = mysqli_fetch_array($moisResult)) {
$x_axis[$i] =  $row["datetime"];
$y_axis[$i] = $row["moisture"];
    $i++;
 
}

$y_axisRev = array();
for ($x = 0; $x < $i; $x++) {
	$y_axisRev[$x] = $y_axis[$i - $x - 1];
			
	}

$moisThresQuery="SELECT * FROM inputData order by datetime desc limit 1";
$moisThresResult = $conn->query($moisThresQuery);
$moisThresrow_cnt = $moisThresResult->num_rows;

$y_axisMoisThres = array();

$i_moisThresCount = 0;
while($row = mysqli_fetch_array($moisThresResult)) {
	$y_axisMoisThres[$i_moisThresCount] = $row["moisThres"];
	$i_moisThresCount++;
}

for ($x = 1; $x < $i; $x++) {
	$y_axisMoisThres[$x] = $y_axisMoisThres[0];
	}

$moisGraph = new Graph(600,500);
$moisGraph->img->SetMargin(40,40,40,40);  
$moisGraph->img->SetAntiAliasing();
$moisGraph->SetScale('textlin');
//$moisGraph->yscale->SetGrace(3);
$moisGraph->SetYScale(0,'lin');
$moisGraph->SetYScale(1,'lin');
$moisGraph->SetShadow();
$moisGraph->title->Set("Moisture");
//$tempgraph->title->SetFont(FF_FONT1,FS_BOLD);

$moisLineplot=new LinePlot($y_axisRev);
$moisLineplot->SetColor('blue');
$moisGraph->AddY(0,$moisLineplot);

$moisThresLinePlot = new LinePlot($y_axisMoisThres);
$moisThresLinePlot->SetColor('red');
$moisGraph->AddY(1,$moisThresLinePlot);


$moisGraph->Add($moisThresLinePlot);

//$moisGraph->Stroke();
//Spara bild till fil

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
