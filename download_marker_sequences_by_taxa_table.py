#!/usr/bin/env python3
'''
download_marker_sequences_by_taxa_table.py -- to download marker sequence according to taxa table

Date: 2020-08-16
Bugs: Any bugs should be reported to yanpengch@qq.com

Input Template:
Species                  Collection   No.         TaxaLabel                              Type   Country  Host                ITS         TUB       TEF        CAL         
Diaporthe lithocarpus    CGMCC        3.15175     Diaporthe_lithocarpus_CGMCC_3.15175    1      China    Lithocarpus glabra  KC153104    KF576311  KC153095   KF576236
Diaporthe lithocarpus    CGMCC        3.15178     Diaporthe_lithocarpus_CGMCC_3.15178    0      China    Smilax china        KC153103    NA        KC153094   NA        
Diaporthe mahothocarpus  CGMCC        3.15181     Diaporthe_mahothocarpus_CGMCC_3.15181  1      China    Lithocarpus glabra  KC153096    KF576312  KC153087   NA         
Diaporthe mahothocarpus  GMCC         3.15182     Diaporthe_mahothocarpus_CGMCC_3.15182  0      China    Mahonia bealei      KC153097    NA        KC153088   NA         

'''

import os
import sys
import pandas as pd
import argparse
import subprocess

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('--table',
    required=True,
    type=str,
    metavar='<taxa_table.txt>',
    help='taxa table with head line')

parser.add_argument('--column',
    type=str,
    nargs='+',
    required=True,
    metavar='SSU LSU ITS',
    help='specify column index')

parser.add_argument('--labelcolumn',
    type=str,
    metavar='TaxaLabel',
    help='specify label column')

args = parser.parse_args()

if __name__ == '__main__':
    table = pd.read_table(args.table, sep = '\t')
    # mkdir
    for dirname in args.column:
        if not os.path.exists(dirname):
            os.mkdir(dirname)

    # map dict accession 2 TaxaLabel
    accession2taxalabel_dict = {}
    if args.labelcolumn:
        try:
            taxa_label_lst = table[args.labelcolumn]
        except:
            print(f'Wrong lablecolumn: {args.labelcolumn}')
        
        for marker in args.column:
            accession_lst = list(table[marker])
            accession_lst = [str(i) for i in accession_lst]
            for index,accession in enumerate(accession_lst):
                if accession == 'NA' or accession == 'na':
                    continue
                accession2taxalabel_dict[accession] = taxa_label_lst[index]

    # collect wrong GenBank accession
    wrong_accession_dict = {}
    # download
    for marker in args.column:
        wrong_accession_dict[marker] = []

        accession_lst = list(set(table[marker]))
        accession_lst = [str(i) for i in accession_lst]

        for accession in accession_lst:
            if accession == 'NA' or accession == 'na':
                continue
            command = f'esearch -db nucleotide -query {accession} | efetch -format fasta'
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()
            if stdout:
                sequence_lst = stdout.decode('utf-8').splitlines()
                if args.labelcolumn:
                    sequence_lst[0] = '>' + accession2taxalabel_dict[accession]
                    with open(f'{marker}/{accession}.fasta', 'wt') as faoutfh:
                        print('\n'.join(sequence_lst), file=faoutfh, flush=True)
                else:
                    with open(f'{marker}/{accession}.fasta', 'wt') as faoutfh:
                        print('\n'.join(sequence_lst), file=faoutfh, flush=True)
            else:
                wrong_accession_dict[marker].append(accession)
                wrong_accession_dict[marker].append(command)
                
    for marker,wrong_accession_lst in wrong_accession_dict.items():
        if wrong_accession_dict:
            print(f'Wrong accession:', file = sys.stderr, flush=True)
            print(f'{marker}:', file = sys.stderr, flush=True)
            for accession, cmd in wrong_accession_lst:
                print(f'{accession}\t{cmd}', file = sys.stderr, flush=True)
    sys.exit(0)