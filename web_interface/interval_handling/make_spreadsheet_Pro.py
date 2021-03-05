import sys
import argparse
from datetime import datetime
header = ['gene_name','chromosome','start','stop',]
parser = argparse.ArgumentParser(description="Retrieve genes from a specificed genomic interval.")
parser.add_argument("--chr")
parser.add_argument("--start")
parser.add_argument("--stop")
parser.add_argument("--filtered",action="store_true")
parser.add_argument("--link",action="store_true")
parser.add_argument("--included_vals")
args = parser.parse_args()


import sqlite3

db_file = '/var/www/html/qTeller_python3/web_interface/proteindb'
mystart = int(args.start)
mystop = int(args.stop)
mychr = args.chr
header.extend(args.included_vals.split(','))
all_info = str(args.included_vals).replace(",", "|")
conn = sqlite3.connect(db_file)
conn.row_factory = sqlite3.Row
c = conn.cursor()
p_dict = {}
p_starts = {}
p_stops = {}
p_chrs = {}
fh2 = open('./tmp/%s.%i.%i.csv' % (mychr,mystart,mystop),'w')
fh3 = open("./tmp/%s.%i.%i.html" % (mychr,mystart,mystop),'w')
header2 = []
for h in header:
    header2.append(h.replace(" ",'_'))
if not 'all' in mychr and mystop != 0:
    c.execute("select * from protein_table where chromosome=? and start>? and stop <?",(mychr,mystart,mystop))
elif not 'all' in mychr and mystop == 0:
    c.execute("select * from protein_table where chromosome=? and start>?", (mychr, mystart))
else:
    c.execute("select * from protein_table")
for row in c:
    myname = row['gene_name']
    if args.filtered:
        if row['filtered'] == 0: continue
    p_starts[myname] = int(row['start'])
    p_stops[myname] = int(row['stop'])
    p_chrs[myname] = row['chromosome']
    if row['chromosome'] in set(['chrMt','chr0','chrPt']): continue
    p_dict[myname] = []
    for v in header:
        if not v in row:
          print(v)
        p_dict[myname].append(str(row[v]))
    p_dict[myname].append("<a href='http://yourwebsite/Rna_Protein_bar_chart.php?name=%s&protein=Submit for Protein Abundance!&info=%s'>http://yourwebsite/Rna_Protein_bar_chart.php?name=%s&protein=Submit for Protein Abundance!&info=%s</a>" % (myname,all_info,myname,all_info))
fh2.write("This spreadsheet was generated using qTeller on %s.\n" % (datetime.today()))
fh2.write(",".join(header2) + "\n")
fh3.write("<table border=\"1\"><tr><td>" + "</td> <td>".join(header2) + "</td></tr>")
genes = list(p_dict)
genes.sort(key=lambda g: p_starts[g])
for gene in sorted(genes,key=lambda g: p_chrs[g]):
    fh3.write("<tr><td>" + "</td> <td>".join(p_dict[gene]) + "</td></tr>")
    fh2.write(",".join(p_dict[gene]) + "\n")
fh3.write("</table>")
fh2.close()
fh3.close()

