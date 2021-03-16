qTeller
=======

The MaizeGDB Python 3 update of James Schnable's RNA-seq processing pipeline and modular web interface

For an examples of MaizeGDB's qTeller web interfaces visit 
<a href="https://qteller.maizegdb.org/">https://qteller.maizegdb.org/</a>

## Overview ##

| Directory Name   | Description |
|------------------|:---------------------:|
| [build_db](/qteller/build_db) | Scripts for constructing the SQLite DB|
| [web_interface](/qteller/web_interface) | Public facing files that are served by the Apache Server.|
| [qteller_python2.7](/qteller/qteller_python2.7) | Old MaizeGDB Python 2.7 instance.|


### Access
For username / password details, please contact [Carson Andorf](mailto:carson.andorf@ars.usda.gov).

## Environment Requirements ##

#### PHP Version 7
* No additional libraries required.

#### Python Version 3.6
* See [requirements.txt](requirements.txt) and [python modules](python_modules.txt) for a list of dependencies.

#### Apache Web Server Version 2.2.15
* No untypical customization is needed.


## Installation ##

### Apache / PHP
See [an example](https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-centos-8) of installing Apache on CentOS 8.

### Python

Centos 8 comes with Python 3, which includes PIP.

To install [additional libraries](requirements.txt):

```
$ 'pip install -r requirements.txt'
```



### Additional Instructions

Upon successful installation of Python, PHP, and Apache, you can `git clone` this project into your Apache directory. The public-facing directories are located in the [web_interface](/qteller/web_interface) directory. Assuming a default Apache installation, the DocumentRoot in the `httpd.conf` would look like this:

```
DocumentRoot "/var/www/html/qTeller/web_interface"
```

See [Adding new data](#adding-new-data) on final steps for generating the DB.

## Adding new data ##

The qTeller database generation script requires the following 3 files:
  1. RNA-seq and/or protein abundance files
      * If it doesn't exist already, create the **build_db/abundance** directory (the abundance directory can be whatever name you want):
      `$ mkdir build_db/abundance`
      * Drop your fpkm_tracking files in the **build_db/abundance** directory. They must end with either the **.fpkm_tracking** file extension from a Cufflinks output, or if you are submitting RNA-seq or protein abundances with only the gene model ID (column 1) and abundance data (column 2), the file extension should be **.txt** .
  2. GFF or bed file
      * Download a GFF file for your desired genome and place it in the [build_db](/qteller/build_db) directory. Alternately, a bed file can be used, where the gene model ID is in column 4. A bed file is REQUIRED for multi-genome qTeller; the gene model ID is in column 4, and the genome ID is in column 5. Here is an [example](qteller/build_db/test_multigenome_NAM_merged_IDs.bed).
  3. CSV file
      * Create a metadata file in CSV format so the script knows how to interpret the fpkm_tracking files. Here is an [example](qteller/build_db/test_singlegenome_metadata.csv).
      * **NOTE:** The *File_handle* column specifies the name of the abundance file to load **(minus the .fpkm_tracking or .txt file extension)**
    
Assuming you have the required files, you can create the SQLite DB for single-genome and/or protein abundance data using the following command: 

```
$ cd build_db
$ python 'build_qt_db_gene_protein.py <METADATA.CSV> --gff_file <GFF.gff3> --info_dir ./abundance' # creates qt5db
```

where <METADATA.CSV> is the CSV file (3), <GFF.gff3> is the GFF file (2), and fpkm_tracking is the directory where the FPKM_TRACKING files are kept (1) as described above. This will create a `singledb` SQLite file.

To create the SQLite DB for multi-genome data using the following command: 

```
$ cd build_db
$ python 'multigenome_build_qt_db.py <METADATA.CSV> --gff_file <GFF.gff3> --info_dir ./fpkm_tracking' # creates multidb
```

* *Fun fact:* you can use the [SQLite Viewer](http://inloop.github.io/sqlite-viewer/) to easily look inside the DB and experiment with queries.

Finally, the last step is to move the generated `singledb` or `multidb` file into the [web_interface](/qteller/web_interface) directory:

```
$ mv singledb ../web_interface/
```

You should now be able to access qTeller through your browser.
