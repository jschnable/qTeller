# Edited by M. Woodhouse September 2020 and Shatabdi sen October 2020
# This script works where the expression data is either a .txt file where: first column, gene name; second column, abundance value; or a genes.fpkm_tracking file where first column, gene name, ninth column, abundance value. Also edited to handle null FPKM values and bed file where column 5 is the genome prefix so as to select a
# particular genome in genes in an interval. Also edited to take a bed file where column 5 is the genome prefix so as to select a particular genome in genes in an interval.

def txt_parse(fname):
    fh = open(fname)
    # fh.readline()
    results = {}
    for x in fh:
        y = x.strip().split('\t')
        results[y[0]] = {'exp': float(y[1])}
    return results


def cuff_parse(fname):
    fh = open(fname)
    fh.readline()
    results = {}
    for x in fh:
        y = x.strip().split('\t')
        results[y[0]] = {'exp': float(y[9])}
    return results

#If you want to include the low and high values from a Cufflinks .fpkm_tracking file, comment out the below: 
#def cuff_parse(fname):
#    fh = open(fname)
#    fh.readline()
#    results = {}
#    for x in fh:
#        y = x.strip().split('\t')
#        results[y[0]] = {'exp':float(y[9]),'low':float(y[10]),'high':float(y[11])}
#    return results


def def_parse(astr):
    y = astr.split(';')
    mydefs = {}
    for z in y:
        a = z.split('=')
        if len(a) != 2: continue
        mydefs[a[0].lower()] = a[1]
    return mydefs


import sqlite3, os, argparse

# Lots of options, most of which should never need to change
parser = argparse.ArgumentParser()
parser.add_argument('--info_dir', default='./',
                    help='Directory containing any .syn, .anno, .fpkm_tracking_1, or .txt files to be included in the database')
parser.add_argument('meta_info',
                    help="The spreadsheet containing information on all expression, function, syntenic ortholog datasets to be included in the database")
parser.add_argument('--gff_file',
                    help="GFF format file containing information on the genome of the organism being studied. Required unless --bed or --trascriptome is set")
parser.add_argument('--bed_file',
                    help="BED format file containing information on the genome of the organism being studied. Required unless --gff or --trascriptome is set")
parser.add_argument('--transcriptome', action="store_true", default=False,
                    help="Fall to tell this script you have no information on the position of genes in the genome.")
parser.add_argument('--gene_def_tag', default="ID",
                    help="The tag to use as the gene name when parsing a gff file. Usually this is either 'ID' or 'Name' but people use all sorts of non-standard tags as well.")
parser.add_argument('--dbname', default='qtdb',
                    help="Name of the SQLite database being created. The default name is the one the qteller webserver expects. Will overwrite other files in the same directory with the same name.")
args = parser.parse_args()
if not os.path.exists(args.info_dir):
    print("Invalid directory {0}. Dying now".format(args.info_dir))
    1 / 0
if not os.path.exists(args.meta_info):
    print("No such file {0}. Dying now".format(args.meta_info))
    1 / 0

if not args.transcriptome and not args.gff_file and not args.bed_file:
    print(
        "You either need to provide a gff file with the \"--gff_file\" option or set the \"--transcriptome\" option or \"--bed_file\" option so the script knows to ignore genomic positioning information. Dying now.")
    1 / 0

# Check if a database file already exists. If it does, delete it.
if os.path.exists(args.dbname):
    os.remove(args.dbname)
conn = sqlite3.connect(args.dbname)
conn.row_factory = sqlite3.Row
c = conn.cursor()
secondc = conn.cursor()
table_list = ['data_sets', 'exp_table', 'gene_table']
c.execute("""create table exp_table
(gene TEXT,
source_id TEXT,
experiment_id TEXT,
exp_val FLOAT)""")
c.execute("""create table data_sets
(stub_id TEXT,
experiment_id TEXT,
source_id TEXT,
type TEXT,
link TEXT,
description TEXT)""")
conn.commit()
fh = open(args.meta_info)
fh.readline()
anno_data = {}
syn_data = {}
exp_data = {}
id2stub = {}
for x in fh:
    y = x.strip().replace('"', '').split(',')
    if len(y) < 6:
        y.extend(['', '', '', '', ''])
    myfh = y[0]
    myid = y[1]
    mysource = y[2]
    mytype = y[3]
    mylink = y[4]
    mydescription = y[5]
    c.execute("INSERT INTO data_sets(stub_id,experiment_id,source_id,type,link,description) VALUES(?,?,?,?,?,?)",
              (myfh, myid, mysource, mytype, mylink, mydescription))
    id2stub[myid] = myfh
    if mytype == 'Expression':
        exp_data[myfh] = ''
        if os.path.exists(args.info_dir + "/" + myfh + ".txt"):
            gene_exp = txt_parse(args.info_dir + "/" + myfh + ".txt")
        elif os.path.exists(args.info_dir + "/" + myfh + ".fpkm_tracking_1"):
            gene_exp = cuff_parse(args.info_dir + "/" + myfh + ".fpkm_tracking_1")
        else:
            print("Neither {0} nor {1} exist. Something is wrong.\nI'll quit and let you figure out what.".format(
                (args.info_dir + "/" + myfh + ".txt"), (args.info_dir + "/" + myfh + ".fpkm_tracking_1")))
        for gene in gene_exp:
            c.execute("INSERT INTO exp_table(gene,experiment_id,source_id,exp_val) VALUES(?,?,?,?)",
                      (gene, myid, mysource, gene_exp[gene]['exp']))
#To include low and high values, comment out the below:
#            c.execute("INSERT INTO exp_table(gene,experiment_id,source_id,exp_val,exp_low,exp_high) VALUES(?,?,?,?,?,?,?,?)",
#                      (gene ,myid, mysource ,gene_exp[gene]['exp'] ,gene_exp[gene]['low'] ,gene_exp[gene]['high']))
        mygeneset = set(list(gene_exp))
    elif mytype == 'Synteny':
        syn_data[myfh] = {}
        synfh = open(args.info_dir + "/" + myfh + ".syn")
        for line in synfh:
            y = line.strip().split('\t')
            if len(y) < 2: continue
            syn_data[myfh][y[0]] = y[1]
    elif mytype == 'Anno':
        anno_data[myfh] = {}
        annofh = open(args.info_dir + "/" + myfh + ".anno")
        for line in annofh:
            y = line.strip().split('\t')
            if len(y) < 2: continue
            anno_data[myfh][y[0]] = y[1].replace(';', '').replace(',', '').replace("'", '').replace('"', '')
    conn.commit()
create_giant_table = []
add2table = []
key_list = {"anno": [], "exp": [], "synteny": []}
create_giant_table.append("create table gene_table(")
add2table.append("INSERT INTO gene_table(")
create_giant_table.append("gene_name TEXT, ")
add2table.append("gene_name, ")
create_giant_table.append("chromosome TEXT, ")
add2table.append("chromosome, ")
create_giant_table.append("start INT, ")
add2table.append("start, ")
create_giant_table.append("stop INT, ")
add2table.append("stop, ")
create_giant_table.append("strand INT, ")
add2table.append("strand, ")
create_giant_table.append("filtered TEXT, ")
add2table.append("filtered, ")
for x in sorted(list(anno_data)):
    create_giant_table.append("%s TEXT, " % x)
    key_list["anno"].append(x)
    add2table.append("%s, " % x)
for x in sorted(list(syn_data)):
    create_giant_table.append("%s TEXT, " % x)
    key_list['synteny'].append(x)
    add2table.append("%s, " % x)
for x in sorted(list(exp_data)):
    create_giant_table.append("%s FLOAT, " % x)
    key_list['exp'].append(x)
    add2table.append("%s, " % x)
create_giant_table[-1] = create_giant_table[-1].replace(',', '')
create_giant_table.append(")")
mycommand = "".join(create_giant_table)
print(mycommand)
c.execute(mycommand)
conn.commit()
add2table[-1] = add2table[-1].replace(', ', '')
add2table.append(")")
create_giant_table.append('')
c.execute("CREATE INDEX gene_name_index ON exp_table(gene);")
conn.commit()
gene_list = []
sdict = {'-1': -1, '1': 1, '+': 1, '-': -1}
if args.transcriptome:
    for g in mygeneset:
        gene_list.append(["'" + g + "'", "''", 0, 0, 1, 1])
else:
    fh = open(args.bed_file)
    error_count = 0
    for x in fh:
        if x[0] == '#': continue
        y = x.strip().split('\t')
        if len(y) < 2: continue
        mydefs = def_parse(y[-1])
        myname = y[3]
        mygenome = y[4]
        gene_list.append(
            ["'" + myname + "'", "'" + y[0] + "'", int(y[1]), int(y[2]), sdict[y[5]], "'" + mygenome + "'"])
for insert_vals in gene_list:
    mygene = insert_vals[0].replace("'", '')
    for x in key_list["anno"]:
        if mygene in anno_data[x]:
            insert_vals.append("'" + anno_data[x][mygene] + "'")
        else:
            insert_vals.append("''")
    for x in key_list["synteny"]:
        if mygene in syn_data[x]:
            insert_vals.append("'" + syn_data[x][mygene] + "'")
        else:
            insert_vals.append("''")
    secondc.execute("Select * from exp_table Where gene=?;", (mygene,))
    exp_dict = {}
    for row in secondc:
        exp_dict[id2stub[row['experiment_id']]] = row['exp_val']
    for x in key_list['exp']:
        if x in exp_dict:
            insert_vals.append(str(exp_dict[x]))
        else:
            # insert_vals.append("0")
            insert_vals.append("None")
    final_command = ") VALUES (%s)" % ",".join(map(str, insert_vals))
    add2table[-1] = final_command
    c.execute(''.join(add2table).replace('None', 'null'))
    # c.execute(''.join(add2table))
conn.commit()
c.close()

