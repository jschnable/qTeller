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
if (array_key_exists("name1",$_POST)) { $mygene1 = trim($_POST["name1"]); } else { $mygene1 = trim($_GET["name1"]);}
if (array_key_exists("name2",$_POST)) { $mygene2 = trim($_POST["name2"]); } else { $mygene2 = trim($_GET["name2"]);}
if (array_key_exists("info",$_POST)) { $myinfo = $_POST["info"]; } elseif (array_key_exists("info",$_GET)) { $myinfo = $_GET["info"]; } else { $myinfo = 'all';}
if (array_key_exists("xmax",$_POST)) { $xmax = $_POST["xmax"]; } elseif (array_key_exists("xmax",$_GET)) { $xmax = $_GET["xmax"]; } else { $xmax = 0; }
if (array_key_exists("ymax",$_POST)) { $ymax = $_POST["ymax"]; } elseif (array_key_exists("ymax",$_GET)) { $ymax = $_GET["ymax"]; } else { $ymax = 0; }
if (empty($ymax)) { $ymax = 0; }
if (empty($xmax)) { $xmax = 0; }
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

$genome = 'multi_genome';
$expression = str_replace("|","_",$all_info);
putenv("MPLCONFIGDIR=/tmp/");
$output = "";

if($all_info != 'all'){
exec("python3 image_handling/make_scatterplot_multigenome.py --gene1 $mygene1 --gene2 $mygene2 --exps \"$all_info\" --xmax $xmax --ymax $ymax", $output);
}else {
echo exec("python3 image_handling/make_scatterplot_multigenome.py --gene1 $mygene1 --gene2 $mygene2 --xmax $xmax --ymax $ymax", $output);
}
echo "<i>Move your mouse over a dot to see details about that expression and abundance datapoint.</i><br>";
echo "<br>";
require("./tmp/$mygene1-$mygene2-$expression-$genome-map.html");
echo "<br>";

echo "<form action=\"scatter_plot_multigenome.php\" method=\"post\"><i>Zoom in by entering smaller maximum values</i><br>Maximum X-Axis Value: <input type=\"text\" name=\"xmax\"/> Maximum Y-Axis Value: <input type=\"text\" name=\"ymax\"/><br><input type=\"hidden\" name=\"name1\" value=\"$mygene1\"><input type=\"hidden\" name=\"name2\" value=\"$mygene2\"><input type=\"hidden\" name=\"info\" value=\"$all_info\"><br>To restore the default scale click \"Submit\" without entering any values. <input type=\"submit\" value=\"Submit\" /></form>";

echo "<a href=\"advanced_scatterplot_options_multigenome.php?name1=$mygene1&name2=$mygene2&info=$all_info\">Advanced Options</a> <-- Allows you to chose which datasets to display.<br>";
echo "Download this image as <a href=\"tmp/$mygene1-$mygene2-$expression-$genome.png\">a high resolution PNG</a> or as <a href=\"tmp/$mygene1-$mygene2-$expression-$genome.svg\">a SVG</a> (best option editing in Inkscape/Illustrator)<br>";
echo "See the expression or abundance of <a href=\"bar_chart_multigenome.php?name=$mygene1&info=$all_info\">$mygene1</a> or <a href=\"bar_chart_multigenome.php?name=$mygene2&info=$all_info\">$mygene2</a> as a bar chart<br>";
echo "<a href=\"scatter_plot_multigenome.php?name1=$mygene1&name2=$mygene2&xmax=$xmax&ymax=$ymax&info=$all_info\">Regenerate this particular analysis</a> <-- copy this link to share this analysis.<br>";
echo "<a href=\"http://genomevolution.org/CoGe/GEvo.pl?accn1=$mygene1;accn2=$mygene2;prog=blastn;show_cns=1;autogo=1;skip_feat_overlap=0\" target=\"_blank\">Compare these genes in GEvo</a><br>";
?>
</div>
</body>
</html>

