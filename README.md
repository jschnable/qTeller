qTeller
=======

RNA-seq processing pipeline and modular web interface

For an examples of MaizeGDB's qTeller web interfaces visit 
<a href="http://qteller2.usda.iastate.edu">http://http://qteller2.usda.iastate.edu</a>


## Virtual Machine ##

The MaizeGDB qTeller VM can be found under MaizeGDB's vSphere:

```
blade3.usda.iastate.edu
└── Dev
    └── qteller2
```

### VM Specs

```
Hostname: qteller2.usda.iastate.edu
Operating System: CentOS release 6.9 (Final)
VM Version: 8
Memory: 4096 MB
Memory Overhead: 44.05 MB
CPU: 1 vCPU
```

### Access
For username / password details, please contact [Carson Andorf](carson.andorf@ars.usda.gov).


## Environment Requirements ##

#### PHP Version 5.3.3
* No additional libraries required.

#### Python Version 2.7.13
* See [requirements.txt](requirements.txt) and [python modules](python_modules.txt) for a list of dependencies.
* **Note**: The host VM has Python 2.6.6 installed by default, and this should not be removed! See [Installation](#installation) for details.

#### Apache Web Server Version 2.2.15
* No untypical customization is needed. See [an example](https://support.rackspace.com/how-to/centos-6-apache-and-php-install/) of installing Apache on CentOS 6.
* For an example of a working `httpd.conf` file, please consult `/etc/httpd/conf/httpd.conf` on the VM.


## Installation ##


## Adding new data ##

