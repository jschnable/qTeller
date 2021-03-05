
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
<h2><font color="green">Visualize Expression or Abundance</font></h2>
<p>View all dataset FPKM expression or NSAF abundance graphs for a query gene, or compare expression graphs between two genes. (To select only specific datasets, go to Advanced Options below.)</p>
<p>qTeller takes a little while to generate  figures. Don't panic if nothing happens for 30 seconds after you click Submit.</p>
<div id="subheaderContainer">
<p><h3><font color="white">Single-Gene Expression or Abundance</font></h3></p>
        </div>

<br>
<form action="Rna_Protein_bar_chart.php" method="post">
<a href="web_images/qT_bc2.png"><img src="web_images/qT_bc2.png" class="image1" width=500 /></a><br>
<br>
<div id="tool2Container">
	<br>
<b><font color="green">Gene Name: <input id = "geneName" type="text" name='name' /> </font></b>
<p>To select only specific datasets, go to <a href="Protein_advanced_barchart_options.php">Advanced options</a></p>
<input type="submit" style="font-face: 'Comic Sans MS'; font-size: larger; color: white; background-color: #cc0000; border: 3pt ridge lightgrey" value=" Submit for mRNA Abundance! " name = "gene">
<input type="submit" style="font-face: 'Comic Sans MS'; font-size: larger; color: white; background-color: #cc0000; border: 3pt ridge lightgrey" value=" Submit for Protein Abundance! " name = "protein">
<br>
</div>
<br>
<div id="subheaderContainer">
<p><h3><font color="white">Two-Gene Scatterplot</font></h3></p>
        </div>

<br>
</form>
<form action="Rna_Protein_scatter_plot.php" method="post">
<a href="web_images/qT_sc2.png"><img src="web_images/qT_sc2.png" class="image1" width=430 /></a><br>
<br>
<div id="tool2Container">
	<br>
<b><font color="green">
Gene1 Name: <input id = 'geneName1' type="text" name='name1' /><br>
Gene2 Name: <input id = 'geneName2' type="text" name='name2' /><br></font></b>
<br>
<p>To select only specific datasets, go to <a href="Protein_advanced_scatterplot_options.php">Advanced options</a></p>
<input type="submit" style="font-face: 'Comic Sans MS'; font-size: larger; color: white; background-color: #cc0000; border: 3pt ridge lightgrey" value=" Submit for mRNA Abundance! " name = "gene">
<input type="submit" style="font-face: 'Comic Sans MS'; font-size: larger; color: white; background-color: #cc0000; border: 3pt ridge lightgrey" value=" Submit for Protein Abundance! " name = "protein">
<br>
<br>
</div>
<div id="subheaderContainer">
<p><h3><font color="white">Single-Gene Expression vs Abundance</font></h3></p>
        </div>

<br>
</form>
<form action="ProteinvsGene_chart.php" method="post">
<a href="web_images/ProteinvsGene.png"><img src="web_images/ProteinvsGene.png" class="image1" width=500 /></a><br>
<br>
<div id="tool2Container">
	<br>
<b><font color="green">Gene Name: <input id = 'geneName7' type="text" name='name' /> </font></b>
<p>To select only specific datasets, go to <a href="advanced_GenevsProtein_options.php">Advanced options</a></p>
<input type="submit" style="font-face: 'Comic Sans MS'; font-size: larger; color: white; background-color: #cc0000; border: 3pt ridge lightgrey" value=" Submit! ">
<br>
</div>
<br>
<div id="subheaderContainer">
<p><h3><font color="white">Multi-Gene Expression vs Abundance in a single tissue</font></h3></p>
        </div>

<br>
</form>
<form action="Mutli_ProteinvsGene_chart.php" method="post">
<a href="web_images/B73 internode_6_7 GeneExpression-B73 internode_6_7 ProteinAbundance.png"><img src="web_images/B73 internode_6_7 GeneExpression-B73 internode_6_7 ProteinAbundance.png" class="image1" width=500 /></a><br>
<br>
<div id="tool2Container">
	<br>
<b><font color="green">Select Tissue: </font></b> <select name="Tissues">
    <option value="Mature Pollen"><b>Mature pollen</b></option>
    <option value="Mature Leaf 8"><b>Mature Leaf 8</b></option>
    <option value="Primary Root 5 Days"><b>Primary Root 5 Days</b></option>
    <option value="Vegetative Meristem 16-19 days"><b>Vegetative Meristem 16-19 days</b></option>	
		
  </select>
  <br><br>

<p>Paste gene IDs for expression vs abundance analysis in the box below. One gene per row. </p>

<TEXTAREA id="select-this" NAME=gene_names rows=25 cols=50 wrap=physical>
</TEXTAREA>
<br>
<input type="submit" style="font-face: 'Comic Sans MS'; font-size: larger; color: white; background-color: #cc0000; border: 3pt ridge lightgrey" value=" Submit! ">
<br>
</div>


</body>
</html>

