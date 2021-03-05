<?php
header("Pragma-directive: no-cache");
header("Cache-directive: no-cache");
header("Cache-control: no-cache");
header("Pragma: no-cache");
header("Expires: 0");
#error_reporting(32767);
if (array_key_exists("name",$_POST)) { $mygene = trim($_POST["name"]); } else { $mygene = trim($_GET["name"]);}
if (array_key_exists("info",$_POST)) { $myinfo = $_POST["info"]; } elseif (array_key_exists("info",$_GET)) { $myinfo = $_GET["info"]; } else { $myinfo = 'all';}
if (is_array($myinfo)  && (sizeof($myinfo) != 0)){ 
#print_r($myinfo);
$all_info = implode("|",$myinfo);
} elseif($myinfo != 'all'){
$all_info = $myinfo;
#echo $all_info;
} else {
$all_info = 'all';
#echo $all_info;
}

#echo "\"$all_info\"";

$expression = str_replace("|","_",$all_info);
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
if($all_info != 'all'){
echo exec("python3 image_handling/make_ProteinvsGene_chart.py --gene $mygene --exps \"$all_info\" ");
}else {
echo exec("python3 image_handling/make_ProteinvsGene_chart.py --gene $mygene");
}
#echo "<p>$mygene</p>";
#echo "<p>$all_info</p>";
echo "<p><i>Click image to enlarge. Move your mouse over a bar to see details about that expression datapoint.</i></p>";

$Nam1 = "Gene_".$mygene."_GeneExpression";
$Nam2 = "Gene_".$mygene."_ProteinAbundance";

require("./tmp/$Nam1-$Nam2-$expression-map.html");
echo "<br>";
echo "<a href=\"advanced_GenevsProtein_options.php?name=$mygene&info=$all_info\">Advanced Options</a> <-- Allows you to chose which datasets to display.<br>";
echo "Download this image as <a href=\"tmp/$Nam1-$Nam2-$expression.png\">a high resolution PNG</a> or <a href=\"tmp/$Nam1-$Nam2-$expression.svg\">a SVG</a> (best option editing in Inkscape/Illustrator)<br>";
echo "<a href=\"ProteinvsGene_chart.php?name=$mygene&info=$all_info\">Regenerate this particular analysis</a> <-- copy this link to share this result.<br>";
?>
<br>
</div>
</body>
</html>
