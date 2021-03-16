


<?php
header("Pragma-directive: no-cache");
header("Cache-directive: no-cache");
header("Cache-control: no-cache");
header("Pragma: no-cache");
header("Expires: 0");
#error_reporting(32767);
if (array_key_exists("name",$_POST)) { $mygene = trim($_POST["name"]); } else { $mygene = trim($_GET["name"]);}
if (array_key_exists("info",$_POST)) { $myinfo = $_POST["info"]; } elseif (array_key_exists("info",$_GET)) { $myinfo = $_GET["info"]; } else { $myinfo = 'all';}


?>
<html>
<body>
<link rel="stylesheet" type="text/css" media="all" href="css/common.css_Gene" />
<div id="mainContainer">
<?php require('header.html'); ?>
<div id="pageContents">
<?php require('welcome_navigation.html'); ?>
<body>
<div id="contentContainer">
<div id="tool2Container">
<?php
#echo exec("echo \$MPLCONFIGDIR");
putenv("MPLCONFIGDIR=/tmp/");
$output = "";
if (is_array($myinfo)  && (sizeof($myinfo) != 0)){ 
#print_r($myinfo);
$all_info = implode("|",$myinfo);
} elseif($myinfo != 'all'){
$all_info = $myinfo;
#print_r($all_info);
} else {
$all_info = 'all';
#print_r($all_info);
}

$expression = str_replace("|","_",$all_info);
if($all_info != 'all'){
echo exec("python3 image_handling/make_bar_chart_singlegenome.py --gene $mygene --exps \"$all_info\" ", $output);
}else {
echo exec("python3 image_handling/make_bar_chart_singlegenome.py --gene $mygene", $output);
}
#echo "<p>mygene = $mygene</p>";
#echo "<p>all_info = $all_info</p>";
#echo "<p>cmd output = <pre>". var_dump($output) ."</pre></p>";
echo "<p><i>Click image to enlarge. Move your mouse over a bar to see details about that expression or abundance datapoint.</i></p>";
require("./tmp/$mygene-$expression-map.html");
echo "<br>";
echo "<a href=\"advanced_barchart_options_singlegenome.php?name=$mygene&info=$all_info\">Advanced Options</a> <-- Allows you to chose which datasets to display.<br>";
echo "Download this image as <a href=\"tmp/$mygene-$expression.png\">a high resolution PNG</a> or <a href=\"tmp/$mygene-$expression.svg\">a SVG</a> (best option editing in Inkscape/Illustrator)<br>";
echo "<a href=\"bar_chart_singlegenome.php?name=$mygene&info=$all_info\">Regenerate this particular analysis</a> <-- copy this link to share this result.<br>";
?>
<br>
</div>
</body>
</html>