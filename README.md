qTeller
=======

The MaizeGDB Python 3 version of James Schnable's RNA-seq processing pipeline and modular web interface.

For an examples of MaizeGDB's qTeller web interfaces visit 
<a href="https://qteller.maizegdb.org/">https://qteller.maizegdb.org/</a>

## Overview ##

| qTeller data types   | Description |
|------------------|:---------------------:|
| Genes in an Interval | Select a chromosome coordinate interval for a given genome to retrieve RNA/protein abundances.|
| Genes by Name | Paste a list of gene models of interest to retrieve their RNA/protein abundances.|
| Visualize Expression | Visualize RNA/protein abundances for a single gene, or compare abundances for two genes.|

Data types are optimized for single-genome RNA-seq data, single-genome RNA-seq and protein abundance data, or multi-genome RNA-seq data.

## Directories ##

| Directory Name   | Description |
|------------------|:---------------------:|
| [build_db](/build_db) | Scripts for constructing the SQLite DB.|
| [web_interface](/web_interface) | Public facing files that are served by the Apache Server.|
| [qteller_python2.7](/qteller_python2.7) | MaizeGDB Python 2.7 instance. This is the current public MaizeGDB qTeller instance.|



## Environment Requirements ##

#### PHP Version 7
* No additional libraries required.

#### Python Version 3.6
* See [python3_requirements.txt](python3_requirements.txt) and [python modules](python_modules.txt) for a list of dependencies.

#### Apache Web Server Version 2.4
* No untypical customization is needed.


## Installation ##

### Apache / PHP
See [an example](https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-centos-8) of installing Apache on CentOS 8.

### Python

Centos 8 comes with Python 3, which includes PIP.

To install [additional libraries](python3_requirements.txt):

```
$ 'pip install -r python3_requirements.txt'
```



### Additional Instructions

Upon successful installation of Python, PHP, and Apache, you can `git clone` this project into your Apache directory. The public-facing directories are located in the [web_interface](/qteller/web_interface) directory. Assuming a default Apache installation, the DocumentRoot in the `httpd.conf` would look like this:

```
DocumentRoot "/var/www/html/qTeller/web_interface"
```

See [Adding new data](#adding-new-data) on final steps for generating the DB.



### Special instructions for "Genes in an Interval" php files:

(1) Drop-down menu changes for chromosome IDs must be manually edited in index_singlegenome.php, index_multigenome.php, and Protein_index.php files. These files must be edited in each to reflect the chromosome IDs of the target genome(s). For instance, maize has ten chromosomes with the nomenclature chr1, chr2, etc; Sorghum also has ten chromosomes, but the chromosome nomenclature is Chr01, Chr02, etc. The index*.php files must be edited to reflect your target genome's chromosome information:

<img width="470" alt="php_dropdowns" src="https://user-images.githubusercontent.com/38228323/111347517-4ac59a80-864d-11eb-852f-6510a9374daa.png">

(2) For index_multigenome.php only, the Genome Version drop-down menu must be edited to reflect the genomes from the [multi-genome bed file](qteller/build_db/test_multigenome_NAM_merged_IDs.bed). Note that <option value= for the Genome Version dropdown menu in the php file corresponds to the genome ID listed in Column 5 of the bed file. [To see more in-depth examples of file formatting, click here](File_and_php_code_examples.pdf).

## Adding new data ##

The qTeller database generation script requires the following 3 files:
  1. RNA-seq and/or protein abundance files
      * If it doesn't exist already, create the **build_db/abundance** directory (the abundance directory can be whatever name you want):
      `$ mkdir build_db/abundance`
      * Drop your fpkm_tracking files in the **build_db/abundance** directory. They must end with either the **.fpkm_tracking** file extension from a Cufflinks output, or if you are submitting RNA-seq or protein abundances with only the gene model ID (column 1) and abundance data (column 2), the file extension should be **.txt** .
  2. GFF or bed file
      * Download a GFF file for your desired genome and place it in the [build_db](/build_db) directory. Alternately, a bed file can be used, where the gene model ID is in column 4. A bed file is REQUIRED for multi-genome qTeller; the gene model ID is in column 4, and the genome ID is in column 5. Here is an [example](qteller/build_db/test_multigenome_NAM_merged_IDs.bed).
  3. CSV file
      * Create a metadata file in CSV format so the script knows how to interpret the abundance files. Here is an [example](/build_db/test_singlegenome_metadata.csv).
      * **NOTE:** The *File_handle* column specifies the name of the abundance file to load **(minus the .fpkm_tracking or .txt file extension)**
    
Assuming you have the required files, you can create the SQLite DB for RNA and/or protein abundance data using the following command: 

```
$ cd build_db
$ python multigenome_build_qt_db.py <METADATA.CSV> --bed_file <BED.bed> --info_dir ./<ABUNDANCE> --dbname userdb # creates userdb
```

where <METADATA.CSV> is the CSV file (3), <GFF.gff3> is the GFF file (2), and <ABUNDANCE>  is the directory where the abundance files are kept (1) as described above. This will create a `userdb` SQLite file.


To build the SQLite DB for single-genome data (with no protein abundances) from the included test data, [download and uncompress this gff3 file](https://download.maizegdb.org/Zm-B73-REFERENCE-NAM-5.0/Zm-B73-REFERENCE-NAM-5.0_Zm00001eb.1.gff3.gz), move to build_db, then run this command:

```
$ cd build_db
$ python build_qt_db_gene_protein.py test_singlegenome_metadata.csv --gff_file Zm-B73-REFERENCE-NAM-5.0_Zm00001eb.1.gff3 --info_dir ./test_singlegenome_fpkm --dbname singledb # creates singledb
```

To build the SQLite DB for single-genome data with both RNA and protein abundances from the included test data, [download and uncompress this gff3 file](https://download.maizegdb.org/Zm-B73-REFERENCE-NAM-5.0/Zm-B73-REFERENCE-NAM-5.0_Zm00001eb.1.gff3.gz), move to build_db, then run this command:

```
$ cd build_db
$ python build_qt_db_gene_protein.py test_singlegenome_metadata.csv --gff_file Zm-B73-REFERENCE-NAM-5.0_Zm00001eb.1.gff3 --info_dir ./test_protein_abundance --dbname proteindb # creates proteindb
```

To create the SQLite DB for multi-genome data from the included test data, run this command: 

```
$ cd build_db
$ python multigenome_build_qt_db.py test_multigenome_metadata.csv --bed_file test_multigenome_NAM_merged_IDs.bed --info_dir ./test_multigenome_fpkm --dbname multidb # creates multidb
```

[To see more in-depth examples of file formatting, click here](File_and_php_code_examples.pdf).

* *Fun fact:* you can use the [SQLite Viewer](http://inloop.github.io/sqlite-viewer/) to easily look inside the DB and experiment with queries.

Finally, the last step is to move the generated `singledb`, `proteindb`, or `multidb` file into the [web_interface](/qteller/web_interface) directory:

```
$ mv singledb ../web_interface/
```

You should now be able to access qTeller through your browser.
