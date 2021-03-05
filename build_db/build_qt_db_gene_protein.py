# Edited by Shatabdi Sen October 2020.
# This is to build both individual gene or protein databases for version 5 genome or a combined database for having both
# gene or protein abundance data.The purpose of this code is to enable building databases as per the user need and data
# availabilty(protein or gene abundances data).
# This script works where the expression data is either a .txt file where: first column, gene name; second column, abundance value; or a genes.fpkm_tracking file where first column, gene name, ninth column, abundance value. Also edited to handle null FPKM values and bed file where column 5 is the genome prefix so as to select a
# particular genome in genes in an interval.

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

parser.add_argument('--gene_info_dir', default='None',
                    help='Directory containing any .syn, .anno. .fpkm_tracking, or .txt files to be included in the database')
parser.add_argument('--protein_info_dir', default='None',
                    help='Directory containing any .syn, .anno, .fpkm_tracking_protein, or .txt files to be included in the database')
parser.add_argument('meta_info',
                    help="The spreadsheet containing information on all expression, function, syntenic ortholog datasets to be included in the database")
parser.add_argument('--bed_file', default='None',
                    help="BED format file containing information on the genome of the organism being studied. Required unless --gff or --trascriptome is set")
parser.add_argument('--gff_file',default='None',
                    help="GFF format file containing information on the genome of the organism being studied. Required unless --trascriptome is set")
parser.add_argument('--transcriptome', action="store_true", default=False,
                    help="Fall to tell this script you have no information on the position of genes in the genome.")
parser.add_argument('--gene_def_tag', default="ID",
                    help="The tag to use as the gene name when parsing a gff file. Usually this is either 'ID' or 'Name' but people use all sorts of non-standard tags as well.")
parser.add_argument('--dbname', default='singledb',
                    help="Name of the SQLite database being created. The default name is the one the qteller webserver expects. Will overwrite other files in the same directory with the same name.")
args = parser.parse_args()

info_dir = 'None'
genome_info_file = 'None'

if (args.gff_file != 'None' and args.bed_file == 'None'):
    genome_info_file = args.gff_file

elif (args.gff_file == 'None' and args.bed_file != 'None'):
    genome_info_file = args.bed_file

elif (args.gff_file == 'None' and args.bed_file == 'None'):
    args.transcriptome = True

else:
    genome_info_file = 'Both'
    print(
        "You either need to provide a gff file with the \"--gff_file\" option or a bed file with the \"--bed_file\" option .Two files are not needed at the same time")

if (args.gene_info_dir != 'None' and args.protein_info_dir == 'None'):
    info_dir = args.gene_info_dir

elif (args.gene_info_dir == 'None' and args.protein_info_dir != 'None'):
    info_dir = args.protein_info_dir
elif(args.gene_info_dir != 'None' and args.protein_info_dir != 'None'):
    info_dir = 'Both'
    print("Both gene and protein FPKM directories are present creating combined database")
else:
    info_dir = 'None'

if (info_dir != 'None' and info_dir != 'Both' and genome_info_file != 'Both'):
    if not os.path.exists(info_dir):
        print(("Invalid directory {0}. Dying now".format(info_dir)))
        1 / 0
    if not os.path.exists(args.meta_info):
        print(("No such file {0}. Dying now".format(args.meta_info)))
        1 / 0

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
    exp_val FLOAT,
    exp_low FLOAT,
    exp_high FLOAT)""")
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
            if os.path.exists(info_dir + "/" + myfh + ".fpkm_tracking"):
                gene_exp = cuff_parse(info_dir + "/" + myfh + ".fpkm_tracking")
            elif os.path.exists(info_dir + "/" + myfh + ".txt"):
                gene_exp = txt_parse(info_dir + "/" + myfh + ".txt")
            else:
                print(("Neither {0} nor {1} exist. Something is wrong.\nI'll quit and let you figure out what.".format(
                    (info_dir + "/" + myfh + ".txt"), (info_dir + "/" + myfh + ".fpkm_tracking"))))
                1 / 0
            for gene in gene_exp:
                c.execute("INSERT INTO exp_table(gene,experiment_id,source_id,exp_val) VALUES(?,?,?,?)",
                          (gene, myid, mysource, gene_exp[gene]['exp']))
#To include low and high values, comment out the below:
#                c.execute("INSERT INTO exp_table(gene,experiment_id,source_id,exp_val,exp_low,exp_high) VALUES(?,?,?,?,?,?)",
#                          (gene,myid,mysource,gene_exp[gene]['exp'],gene_exp[gene]['low'],gene_exp[gene]['high']))
            mygeneset = set(list(gene_exp))
        elif mytype == 'Synteny':
            syn_data[myfh] = {}
            synfh = open(info_dir + "/" + myfh + ".syn")
            for line in synfh:
                y = line.strip().split('\t')
                if len(y) < 2: continue
                syn_data[myfh][y[0]] = y[1]
        elif mytype == 'Anno':
            anno_data[myfh] = {}
            annofh = open(info_dir + "/" + myfh + ".anno")
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
    create_giant_table.append("filtered INT, ")
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
    elif (genome_info_file == args.gff_file):
        fh = open(args.gff_file)
        count = 0
        for x in fh:
            if x[0] == '#': continue
            y = x.strip().split('\t')
            if len(y) < 2: continue
            if y[2] != 'gene': continue
            mydefs = def_parse(y[-1])
            if not args.gene_def_tag.lower() in mydefs:
                if count < 100:
                    print(("I didn't detect {0} in the definition line of this gene:\n{1}".format(args.gene_def_tag,
                                                                                                 x.strip())))
                if count == 100:
                    print("more than a hundred problematic genes. not printing additional errror messages.")
            else:
                myname = mydefs[args.gene_def_tag.lower()]
                gene_list.append(["'" + myname + "'", "'" + y[0] + "'", int(y[3]), int(y[4]), sdict[y[6]], 1])
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
                insert_vals.append("0")
        final_command = ") VALUES (%s)" % ",".join(map(str, insert_vals))
        add2table[-1] = final_command
        c.execute(''.join(add2table).replace('None', 'null'))
    conn.commit()
    c.close()
elif (info_dir == 'Both' and genome_info_file != 'Both'):
    if not os.path.exists(args.gene_info_dir):
        print(("Invalid directory {0}. Dying now".format(args.gene_info_dir)))
        1 / 0
    if not os.path.exists(args.protein_info_dir):
        print(("Invalid directory {0}. Dying now".format(args.protein_info_dir)))
        1 / 0
    if not os.path.exists(args.meta_info):
        print(("No such file {0}. Dying now".format(args.meta_info)))
        1 / 0
    if os.path.exists(args.dbname):
        os.remove(args.dbname)
    conn = sqlite3.connect(args.dbname)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    secondc = conn.cursor()
    table_list = ['data_sets', 'gene_exp_table', 'gene_table', 'protein_exp_table', 'protein_table']
    c.execute("""create table data_sets
    (stub_id TEXT,
    experiment_id TEXT,
    source_id TEXT,
    type TEXT,
    link TEXT,
    description TEXT)""")
    c.execute("""create table gene_exp_table
    (gene TEXT,
    source_id TEXT,
    experiment_id TEXT,
    exp_val FLOAT)""")
    c.execute("""create table protein_exp_table
    (gene TEXT,
    source_id TEXT,
    experiment_id TEXT,
    exp_val FLOAT)""")
    conn.commit()
    fh = open(args.meta_info)
    fh.readline()
    gene_anno_data = {}
    gene_syn_data = {}
    gene_exp_data = {}
    protein_anno_data = {}
    protein_syn_data = {}
    protein_exp_data = {}
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
            gene_exp_data[myfh] = ''
            protein_exp_data[myfh] = ''
            if os.path.exists(args.gene_info_dir + "/" + myfh + ".fpkm_tracking") and os.path.exists(
                    args.protein_info_dir + "/" + myfh + ".fpkm_tracking"):
                gene_exp = cuff_parse(args.gene_info_dir + "/" + myfh + ".fpkm_tracking")
                protein_exp = cuff_parse(args.protein_info_dir + "/" + myfh + ".fpkm_tracking")
            elif os.path.exists(args.gene_info_dir + "/" + myfh + ".txt") and os.path.exists(
                    args.protein_info_dir + "/" + myfh + ".txt"):
                protein_exp = txt_parse(args.protein_info_dir + "/" + myfh + ".txt")
                gene_exp = txt_parse(args.gene_info_dir + "/" + myfh + ".txt")
            elif os.path.exists(args.gene_info_dir + "/" + myfh + ".fpkm_tracking"):
                gene_exp = cuff_parse(args.gene_info_dir + "/" + myfh + ".fpkm_tracking")
            elif os.path.exists(args.gene_info_dir + "/" + myfh + ".txt"):
                gene_exp = txt_parse(args.gene_info_dir + "/" + myfh + ".txt")
            elif os.path.exists(args.protein_info_dir + "/" + myfh + ".fpkm_tracking"):
                protein_exp = cuff_parse(args.protein_info_dir + "/" + myfh + ".fpkm_tracking")
            elif os.path.exists(args.protein_info_dir + "/" + myfh + ".txt"):
                protein_exp = txt_parse(args.protein_info_dir + "/" + myfh + ".txt")
            else:
                print(("Neither {0} nor {1} exist. Something is wrong.\nI'll quit and let you figure out what.".format(
                    (args.gene_info_dir + "/" + myfh + ".txt"), (args.gene_info_dir + "/" + myfh + ".fpkm_tracking"),
                    (args.protein_info_dir + "/" + myfh + ".txt"),
                    (args.protein_info_dir + "/" + myfh + ".fpkm_tracking"))))
                1 / 0

            for gene in gene_exp:
                c.execute("INSERT INTO gene_exp_table(gene,experiment_id,source_id,exp_val) VALUES(?,?,?,?)",
                          (gene, myid, mysource, gene_exp[gene]['exp']))
            mygeneset_gene = set(list(gene_exp))
            for protein in protein_exp:
                c.execute("INSERT INTO protein_exp_table(gene,experiment_id,source_id,exp_val) VALUES(?,?,?,?)",
                          (protein, myid, mysource, protein_exp[protein]['exp']))
            mygeneset_protein = set(list(protein_exp))
        elif mytype == 'Synteny':
            gene_syn_data[myfh] = {}
            protein_syn_data[myfh] = {}
            gene_synfh = open(args.gene_info_dir + "/" + myfh + ".syn")
            protein_synfh = open(args.protein_info_dir + "/" + myfh + ".syn")
            for line in gene_synfh:
                y = line.strip().split('\t')
                if len(y) < 2: continue
                gene_syn_data[myfh][y[0]] = y[1]
            for line in protein_synfh:
                y = line.strip().split('\t')
                if len(y) < 2: continue
                protein_syn_data[myfh][y[0]] = y[1]
        elif mytype == 'Anno':
            gene_anno_data[myfh] = {}
            protein_anno_data[myfh] = {}
            gene_annofh = open(args.gene_info_dir + "/" + myfh + ".anno")
            protein_annofh = open(args.protein_info_dir + "/" + myfh + ".anno")
            for line in gene_annofh:
                y = line.strip().split('\t')
                if len(y) < 2: continue
                gene_anno_data[myfh][y[0]] = y[1].replace(';', '').replace(',', '').replace("'", '').replace('"', '')
            for line in protein_annofh:
                y = line.strip().split('\t')
                if len(y) < 2: continue
                protein_anno_data[myfh][y[0]] = y[1].replace(';', '').replace(',', '').replace("'", '').replace('"', '')
        conn.commit()
    gene_create_giant_table = []
    gene_add2table = []
    protein_create_giant_table = []
    protein_add2table = []
    gene_key_list = {"anno": [], "exp": [], "synteny": []}
    protein_key_list = {"anno": [], "exp": [], "synteny": []}
    gene_create_giant_table.append("create table gene_table(")
    gene_add2table.append("INSERT INTO gene_table(")
    gene_create_giant_table.append("gene_name TEXT, ")
    gene_add2table.append("gene_name, ")
    gene_create_giant_table.append("chromosome TEXT, ")
    gene_add2table.append("chromosome, ")
    gene_create_giant_table.append("start INT, ")
    gene_add2table.append("start, ")
    gene_create_giant_table.append("stop INT, ")
    gene_add2table.append("stop, ")
    gene_create_giant_table.append("strand INT, ")
    gene_add2table.append("strand, ")
    gene_create_giant_table.append("filtered INT, ")
    gene_add2table.append("filtered, ")
    ########################################################################
    protein_create_giant_table.append("create table protein_table(")
    protein_add2table.append("INSERT INTO protein_table(")
    protein_create_giant_table.append("gene_name TEXT, ")
    protein_add2table.append("gene_name, ")
    protein_create_giant_table.append("chromosome TEXT, ")
    protein_add2table.append("chromosome, ")
    protein_create_giant_table.append("start INT, ")
    protein_add2table.append("start, ")
    protein_create_giant_table.append("stop INT, ")
    protein_add2table.append("stop, ")
    protein_create_giant_table.append("strand INT, ")
    protein_add2table.append("strand, ")
    protein_create_giant_table.append("filtered INT, ")
    protein_add2table.append("filtered, ")

    for x in sorted(list(gene_anno_data)):
        gene_create_giant_table.append("%s TEXT, " % x)
        gene_key_list["anno"].append(x)
        gene_add2table.append("%s, " % x)
    for x in sorted(list(gene_syn_data)):
        gene_create_giant_table.append("%s TEXT, " % x)
        gene_key_list['synteny'].append(x)
        gene_add2table.append("%s, " % x)
    for x in sorted(list(gene_exp_data)):
        gene_create_giant_table.append("%s FLOAT, " % x)
        gene_key_list['exp'].append(x)
        gene_add2table.append("%s, " % x)
    gene_create_giant_table[-1] = gene_create_giant_table[-1].replace(',', '')
    gene_create_giant_table.append(")")
    mycommand = "".join(gene_create_giant_table)
    print(mycommand)
    c.execute(mycommand)
    conn.commit()
    gene_add2table[-1] = gene_add2table[-1].replace(', ', '')
    gene_add2table.append(")")
    gene_create_giant_table.append('')
    ############################################################
    for x in sorted(list(protein_anno_data)):
        protein_create_giant_table.append("%s TEXT, " % x)
        protein_key_list["anno"].append(x)
        protein_add2table.append("%s, " % x)
    for x in sorted(list(protein_syn_data)):
        protein_create_giant_table.append("%s TEXT, " % x)
        protein_key_list['synteny'].append(x)
        protein_add2table.append("%s, " % x)
    for x in sorted(list(protein_exp_data)):
        protein_create_giant_table.append("%s FLOAT, " % x)
        protein_key_list['exp'].append(x)
        protein_add2table.append("%s, " % x)
    protein_create_giant_table[-1] = protein_create_giant_table[-1].replace(',', '')
    protein_create_giant_table.append(")")
    mycommand = "".join(protein_create_giant_table)
    print(mycommand)
    c.execute(mycommand)
    conn.commit()
    protein_add2table[-1] = protein_add2table[-1].replace(', ', '')
    protein_add2table.append(")")
    protein_create_giant_table.append('')

    ##############################################################

    c.execute("CREATE INDEX gene_name_index ON gene_exp_table(gene);")
    c.execute("CREATE INDEX protein_name_index ON protein_exp_table(gene);")
    conn.commit()

    gene_list_gene = []
    protein_gene_list = []
    sdict = {'-1': -1, '1': 1, '+': 1, '-': -1}
    if args.transcriptome:
        for g in mygeneset_gene:
            gene_list_gene.append(["'" + g + "'", "''", 0, 0, 1, 1])
        for g in mygeneset_protein:
            protein_gene_list.append(["'" + g + "'", "''", 0, 0, 1, 1])
    elif (genome_info_file == args.gff_file):
        fh = open(args.gff_file)
        count = 0
        for x in fh:
            if x[0] == '#': continue
            y = x.strip().split('\t')
            if len(y) < 2: continue
            if y[2] != 'gene': continue
            mydefs = def_parse(y[-1])
            if not args.gene_def_tag.lower() in mydefs:
                if count < 100:
                    print(("I didn't detect {0} in the definition line of this gene:\n{1}".format(args.gene_def_tag,
                                                                                                 x.strip())))
                if count == 100:
                    print("more than a hundred problematic genes. not printing additional errror messages.")
            else:
                myname = mydefs[args.gene_def_tag.lower()]
                gene_list_gene.append(["'" + myname + "'", "'" + y[0] + "'", int(y[3]), int(y[4]), sdict[y[6]], 1])
                protein_gene_list.append(["'" + myname + "'", "'" + y[0] + "'", int(y[3]), int(y[4]), sdict[y[6]], 1])
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
            gene_list_gene.append(
                ["'" + myname + "'", "'" + y[0] + "'", int(y[1]), int(y[2]), sdict[y[5]], "'" + mygenome + "'"])
            protein_gene_list.append(
                ["'" + myname + "'", "'" + y[0] + "'", int(y[1]), int(y[2]), sdict[y[5]], "'" + mygenome + "'"])

    ##############################################################################

    # print(gene_list_gene)
    for gene_insert_vals in gene_list_gene:
        mygene = gene_insert_vals[0].replace("'", '')
        for x in gene_key_list["anno"]:
            if mygene in gene_anno_data[x]:
                gene_insert_vals.append("'" + gene_anno_data[x][mygene] + "'")
            else:
                gene_insert_vals.append("''")
        for x in gene_key_list["synteny"]:
            if mygene in gene_syn_data[x]:
                gene_insert_vals.append("'" + gene_syn_data[x][mygene] + "'")
            else:
                gene_insert_vals.append("''")
        secondc.execute("Select * from gene_exp_table Where gene=?;", (mygene,))
        gene_exp_dict = {}
        for row in secondc:
            gene_exp_dict[id2stub[row['experiment_id']]] = row['exp_val']
        for x in gene_key_list['exp']:
            if x in gene_exp_dict:
                gene_insert_vals.append(str(gene_exp_dict[x]))
            else:
                gene_insert_vals.append("None")

        # print(gene_insert_vals)
        gene_final_command = ") VALUES (%s)" % ",".join(map(str, gene_insert_vals))
        # print(gene_final_command)
        gene_add2table[-1] = gene_final_command
        # print(gene_add2table)
        c.execute(''.join(gene_add2table).replace('None', 'null'))
    #################################################################################
    for protein_insert_vals in protein_gene_list:
        mygene = protein_insert_vals[0].replace("'", '')
        for x in protein_key_list["anno"]:
            if mygene in protein_anno_data[x]:
                protein_insert_vals.append("'" + protein_anno_data[x][mygene] + "'")
            else:
                protein_insert_vals.append("''")
        for x in protein_key_list["synteny"]:
            if mygene in protein_syn_data[x]:
                protein_insert_vals.append("'" + protein_syn_data[x][mygene] + "'")
            else:
                protein_insert_vals.append("''")

        secondc.execute("Select * from protein_exp_table Where gene=?;", (mygene,))

        protein_exp_dict = {}
        for row in secondc:
            protein_exp_dict[id2stub[row['experiment_id']]] = row['exp_val']
        for x in protein_key_list['exp']:
            if x in protein_exp_dict:
                protein_insert_vals.append(str(protein_exp_dict[x]))
            else:
                # protein_insert_vals.append("0")
                protein_insert_vals.append("None")
        protein_final_command = ") VALUES (%s)" % ",".join(map(str, protein_insert_vals))
        protein_add2table[-1] = protein_final_command
        c.execute(''.join(protein_add2table).replace('None', 'null'))
    conn.commit()
    c.close()
elif (info_dir == 'None'):
    print("Please enter either gene or protein FPKM files directory")

##Original

