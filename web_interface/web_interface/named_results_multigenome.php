
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
$mynames = str_replace("\n","dummy",$_POST['gene_names']);
$mynames = preg_replace('/\s+/','',$mynames);
$myinclude = $_POST['info'];
$mycommand = "python3 interval_handling/make_spreadsheet_named_multigenome.py --names $mynames";
$mycommand = $mycommand . " --included_vals " . implode(",", $myinclude) . " 2>&1";
$cmd_output = array();
exec($mycommand, $cmd_output);
echo "<a href=\"tmp/custom.html\">View results on your web browser</a><br>";
echo "<a href=\"tmp/custom.csv\">Download Results as a .csv spreadsheet</a>";
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

