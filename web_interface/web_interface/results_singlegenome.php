
<html>
<head>
	<body>
<link rel="stylesheet" type="text/css" media="all" href="css/common.css_Gene" />
<div id="mainContainer">
<?php require('header.html'); ?>
<div id="pageContents">
<?php require('welcome_navigation.html'); ?>

<div id="contentContainer">
</head>
<div id="subheaderContainer">
<p><h2><font color="white">Results</font></h2></p>
  </div>
<?php
$myversion = $_POST['version'];
$mystart = trim($_POST['start']);
if (empty($mystart)) { $mystart=0; }
$mystop = trim($_POST['stop']);
if (empty($mystop)) { $mystop=0; }
$mystart = str_replace(',','',$mystart);
$mystop = str_replace(',','',$mystop);
$mychr = $_POST['chr'];
$myinclude = $_POST['info'];
$mycommand = "python3 interval_handling/make_spreadsheet_singlegenome.py --chr $mychr --start $mystart --stop $mystop";
if ($myversion == '2F') {
	$mycommand = $mycommand . " --filtered ";
	}
$mycommand = $mycommand . " --included_vals " . implode(",", $myinclude) . " 2>&1";
$cmd_output = array();
exec($mycommand, $cmd_output);
echo "<a href=\"tmp/$mychr.$mystart.$mystop.html\">View results on your web browser</a><br>";
echo "<a href=\"tmp/$mychr.$mystart.$mystop.csv\">Download Results as a .csv spreadsheet</a>";
?>
<br>
<br>
<br>
<br>
<div id="tool2Container">
<p><h3>Problems? Questions? Let us know through the Contact page!</h3></p>
</div>
</div>
<br>
<br>
</div>
</div>
</div>
</body>
</html>

