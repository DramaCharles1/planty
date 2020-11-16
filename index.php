<?php
//phpinfo();

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

//$dir="/media/savestuff";
$dir="/var/www/html/Images";
$images = glob($dir . "/*.jpg");

$image1 = str_replace("/var/www/html/","",$images[count($images)-1]); 
$image2 = str_replace("/var/www/html/","",$images[count($images)-2]); 
$image3 = str_replace("/var/www/html/","",$images[count($images)-3]); 
$image4 = str_replace("/var/www/html/","",$images[count($images)-4]); 

$moisPlot = "MoisturePlot.png";
$greenPlot = "GreenPlot.png";
$lightPlot = "LightPlot.png";

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
<!--
	<img src="<?php echo $image2 ?>" width="512" height="384" alt="image 2" align="top"/>
	<img src="<?php echo $image3 ?>" width="512" height="384" alt="image 3" align="top"/>
	<img src="<?php echo $image4 ?>" width="512" height="384" alt="image 3" align="top"/>
-->


	<img src="<?php echo $moisPlot ?>" width="512" height="384" alt="Moisture plot" align="top"/>
 	<img src="<?php echo $greenPlot ?>" width="512" height="384" alt="Growth plot" align="top"/>
 	<img src="<?php echo $lightPlot ?>" width="512" height="384" alt="Growth plot" align="top"/>
 	 	
 	<form action="subpages/watch_planty.php">
    <input type="submit" value="Two day data" />
	</form>
	
	<form action="subpages/graph.php">
    <input type="submit" value="Another graph" />
	</form>
	
	<form action="subpages/planty_pics.php">
    <input type="submit" value="Show daily pictures" />
	</form>
	
<!--
	<form action="subpages/planty_pics.php" method="get">
	How many days to show: <input type="text" name="amount">
	</form>
-->
	
 	<img src="https://s3.amazonaws.com/codecademy-content/courses/web-101/web101-image_brownbear.jpg" />
	
</body>

</html>
