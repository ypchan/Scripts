#!/usr/bin/env python3
'''
fasta2nexus.py -- convert FASTA format alignment file to NEXUS format

DATE: 2021-02-26
BUGS: Any bugs should reported to 764022822@qq.com
'''

import sys
from Bio import AlignIO

import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('inalignedfile',
        metavar='<alignment.fasta>',
        type=str,
        help='input file must be in FASTA format')

    parser.add_argument('outalignedfile',
        metavar='<alignment.nex>',
        type=str,
        help='output file in NEXUS format')
    args = parser.parse_args()
    return args

args = parse_args()

if __name__ == '__main__':
    args = parse_args()
    records = AlignIO.parse(args.inalignedfile, 'fasta', alphabet=IUPAC.ambiguous_dna)
    with open(args.outalignedfile, 'w') as outfh:
        AlignIO.write(records, outfh, 'nexus')