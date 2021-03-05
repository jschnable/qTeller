import sys
import argparse
from datetime import datetime
db_file = '/var/www/html/qTeller_python3/web_interface/multidb'
header = ['gene_name','chromosome','start','stop','filtered']
parser = argparse.ArgumentParser(description="Retrieve genes from a specificed genomic interval.")
parser.add_argument("--chr")
parser.add_argument("--start")
parser.add_argument("--stop")
parser.add_argument("--filtered")
parser.add_argument("--link",action="store_true")
parser.add_argument("--included_vals")
args = parser.parse_args()
import sqlite3
mystart = int(args.start)
mystop = int(args.stop)
mychr = args.chr
myfiltered = args.filtered
header.extend(args.included_vals.split(','))
all_info = str(args.included_vals).replace(",", "|")
conn = sqlite3.connect(db_file)
conn.row_factory = sqlite3.Row
c = conn.cursor()
p_dict = {}
p_start = {}
p_stop = {}
p_chr = {}
p_filtered = {}
fh2 = open('./tmp/%s.%i.%i.%s.csv' % (mychr,mystart,mystop,myfiltered),'w')
fh3 = open("./tmp/%s.%i.%i.%s.html" % (mychr,mystart,mystop,myfiltered),'w')
header2 = []
for h in header:
    header2.append(h.replace(" ",'_'))
if not 'all' in mychr and mystop != 0:
    c.execute("select * from gene_table where chromosome=? and start>? and stop<? and filtered=?",(mychr,mystart,mystop,myfiltered))
elif not 'all' in mychr and mystop == 0:
    c.execute("select * from gene_table where chromosome=? and start>? and filtered=?", (mychr, mystart,myfiltered))
else:
    c.execute("select * from gene_table where start>? and filtered=?",(mystart,myfiltered))
for row in c:
    myname = row['gene_name']
    p_start[myname] = int(row['start'])
    p_stop[myname] = int(row['stop'])
    p_chr[myname] = row['chromosome']
    p_filtered[myname] = row['filtered']
    if row['chromosome'] in set(['chrMt','chr0','chrPt']): continue
    p_dict[myname] = []
    for v in header:
        if not v in row:
          print(v)
        p_dict[myname].append(str(row[v]))
    p_dict[myname].append("<a href='http://yourwebsite/bar_chart_multigenome.php?name=%s&info=%s'>http://yourwebsite/bar_chart_multigenome.php?name=%s&info=%s</a>" % (myname,all_info,myname,all_info))
fh2.write("This spreadsheet was generated using qTeller on %s.\n" % (datetime.today()))
fh2.write(",".join(header2) + "\n")
fh3.write("<table border=\"1\"><tr><td>" + "</td> <td>".join(header2) + "</td></tr>")
genes = list(p_dict)
genes.sort(key=lambda g: p_start[g])
for gene in sorted(genes,key=lambda g: p_chr[g]):
    fh3.write("<tr><td>" + "</td> <td>".join(p_dict[gene]) + "</td></tr>")
    fh2.write(",".join(p_dict[gene]) + "\n")
fh3.write("</table>")
fh2.close()
fh3.close()

