#!/usr/bin/env python3
import sys
import fileinput

with fileinput.input(sys.argv[1]) as fh:
    tmp_lst = []
    for line in fh:
        if line.startswith('>Cluster'):
            if tmp_lst:
                represnetative = tmp_lst[0]
                for item in tmp_lst:
                    print(represnetative,item, sep='\t', file=sys.stdout, flush=True)
            tmp_lst = []
            continue
        else:
            gene_id = line.split()[2].rstrip('...')
            if '*' in line:
                tmp_lst.insert(0, gene_id)
            else:
                tmp_lst.append(gene_id)
    sys.exit(0)