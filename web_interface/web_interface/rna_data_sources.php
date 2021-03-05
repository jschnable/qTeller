<html>
<body>
<html>
<body>
<link rel="stylesheet" type="text/css" media="all" href="css/common.css_Gene" />

<div id="mainContainer">
	<?php require('header.php'); ?>
<div id="pageContents">
<?php require('welcome_navigation.html'); ?>
<div id="contentContainer">
<p><h3><font color="green">Methods</font></h3></p>
<p>Describe methods here. </p>
<br>
<p><h3><font color="green">Dataset sources and authors/labs</font></h3></p>
<p>The following papers [by lab] were the sources of the RNA-seq datasets included in these qTeller datasets (sources link to publications):</p>
<p><b>Single Genome:</b></p>
<?php
class MyDB extends SQLite3
{
        function __construct()
        {
                $this->open('./singledb');
        }
}
$db = new myDB();
$result = $db->query("SELECT DISTINCT source_id,link from data_sets");
    while($row = $result->fetchArray(SQLITE3_ASSOC)) {
echo " <a href=\"" . $row['link'] . "\">" . $row['source_id'] . "</a><br>";
 }
?>
<p><b>Multiple Genomes:</b></p>
<?php
class MyDB2 extends SQLite3
{
        function __construct()
        {
                $this->open('./multidb');
        }
}
$db2 = new myDB2();
$result = $db2->query("SELECT DISTINCT source_id,link from data_sets");
    while($row = $result->fetchArray(SQLITE3_ASSOC)) {
echo " <a href=\"" . $row['link'] . "\">" . $row['source_id'] . "</a><br>";
 }
?>
<p><b>Protein Abudances:</b></p>
<?php
class MyDB3 extends SQLite3
{
        function __construct()
        {
                $this->open('./proteindb');
        }
}
$db3 = new myDB3();
$result = $db3->query("SELECT DISTINCT source_id,link from data_sets");
    while($row = $result->fetchArray(SQLITE3_ASSOC)) {
echo " <a href=\"" . $row['link'] . "\">" . $row['source_id'] . "</a><br>";
 }
  ?>
</div>
</div>
</div>
</body>
</html>

