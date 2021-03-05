
<html>
<head>
<script type="text/javascript">

function copyToClipboard(elementId,TextId) {

  // Create a "hidden" input
  var aux = document.createElement("input");

  // Assign it the value of the specified element
  aux.setAttribute("value", document.getElementById(elementId).innerHTML);

  // Append it to the body
  document.body.appendChild(aux);

  // Highlight its content
  aux.select();

  // Copy the highlighted text
  document.execCommand("copy");

  // Remove it from the body
  document.body.removeChild(aux);

  let textarea = document.getElementById(TextId);
  textarea.focus();
  textarea.value += document.getElementById(elementId).innerHTML + "\n";
}

</script>
</head>
<body>
<link rel="stylesheet" type="text/css" media="all" href="css/common.css_Gene" />
<div id="mainContainer">
<?php require('header.html'); ?>
<div id="pageContents">
<?php require('welcome_navigation.html'); ?>
<div id="contentContainer">
<h2><font color="green">Multi-Genome Visualize Expression</font></h2>
<p>View all dataset FPKM expression graphs for a query gene model, or compare expression graphs between two gene models from the same or different genomes. (To select only specific datasets, go to Advanced Options below.)</p>
<p>qTeller takes a little while to generate  figures. Don't panic if nothing happens for 30 seconds after you click Submit.</p>
<div id="subheaderContainer">
<p><h3><font color="white">Single-Gene Expression</font></h3></p>
        </div>

<br>
<form action="bar_chart_multigenome.php" method="post">
<a href="web_images/qT_bc2.png"><img src="web_images/qT_bc2.png" class="image1" width=500 /></a><br>
<br>
<div id="tool2Container">
	<br>
<b><font color="green">Gene Name: <input id = "geneName" type="text" name='name' /> </font></b><br>
<p>To select only specific datasets, go to <a href="advanced_barchart_options_multigenome.php">Advanced options</a></p>
<input type="submit" style="font-face: 'Comic Sans MS'; font-size: larger; color: white; background-color: #cc0000; border: 3pt ridge lightgrey" value=" Submit! " name = "gene">
<br>
</div>
<br>
<div id="subheaderContainer">
<p><h3><font color="white">Two-Gene Scatterplot</font></h3></p>
        </div>

<br>
</form>
<form action="scatter_plot_multigenome.php" method="post">
<a href="web_images/qT_sc2.png"><img src="web_images/qT_sc2.png" class="image1" width=430 /></a><br>
<br>
<div id="tool2Container">
	<br>
<b><font color="green">
Gene1 Name: <input id = 'geneName1' type="text" name='name1' /><br>
Gene2 Name: <input id = 'geneName2' type="text" name='name2' /><br></font></b>
<br>
<p>To select only specific datasets, go to <a href="advanced_scatterplot_options_multigenome.php">Advanced options</a></p>
<input type="submit" style="font-face: 'Comic Sans MS'; font-size: larger; color: white; background-color: #cc0000; border: 3pt ridge lightgrey" value=" Submit! " name = "gene">
<br>
<br>
</div>
</body>
</html>

