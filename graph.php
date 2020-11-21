<?php
require_once ('/etc/php/7.3/jpgraph/src/jpgraph.php');
require_once ('/etc/php/7.3/jpgraph/src/jpgraph_line.php');

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

$moisQuery="SELECT * FROM plantyLog order by datetime desc limit 24";
$moisResult = $conn->query($moisQuery);
$moisrow_cnt = $moisResult->num_rows;

$x_axis = array();
$y_axis = array();
$i = 0;

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
$moisGraph->Stroke();

?>
