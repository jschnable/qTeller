
<?php
header("Pragma-directive: no-cache");
header("Cache-directive: no-cache");
header("Cache-control: no-cache");
header("Pragma: no-cache");
header("Expires: 0");

if (array_key_exists("Tissues",$_POST)) { $mytissue = trim($_POST["Tissues"]); } else { $mytissue = trim($_GET["Tissues"]);}
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
if(isset($_POST['gene_names'])){
$mynames = str_replace("\n","dummy",$_POST['gene_names']);
$mynames = preg_replace('/\s+/','',$mynames);
}else if (isset($_GET['gene_names'])){
$mynames = str_replace("\n","dummy",$_GET['gene_names']);
$mynames = preg_replace('/\s+/','',$mynames);

}
putenv("MPLCONFIGDIR=/tmp/");

$mytissue1 = '"'.$mytissue.'"';
$mynames1 = '"'.$mynames.'"';
echo exec("python3 image_handling/make_Multi_ProteinvsGene_chart.py --names $mytissue1 --exps $mynames1 ");
echo "<p><i>Click image to enlarge. Move your mouse over a bar to see details about that expression datapoint.</i></p>";

$Nam1 = "Gene_".$mytissue."_GeneExpression";
$Nam2 = "Gene_".$mytissue."_ProteinAbundance";

require("./tmp/$Nam1-$Nam2-$mynames-map.html");
echo "<br>";
echo "Download this image as <a href=\"tmp/$Nam1-$Nam2-$mynames.png\">a high resolution PNG</a> or <a href=\"tmp/$Nam1-$Nam2-$mynames.svg\">a SVG</a> (best option editing in Inkscape/Illustrator)<br>";
echo "<a href=\"Mutli_ProteinvsGene_chart.php?Tissues=$mytissue&gene_names=$mynames\">Regenerate this particular analysis</a> <-- copy this link to share this result.<br>";
?>
</div>
</body>
</html>
