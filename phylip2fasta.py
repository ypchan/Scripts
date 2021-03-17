#!/usr/bin/env python3
'''
fasta2phylip.py -- convert FASTA format alignment file to phylip format

DATE: 2021-02-05
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

    parser.add_argument('inphy',
        metavar='<in.phy>',
        type=str,
        help='input file must be in PHYLIP format')

    parser.add_argument('-f', '--format',
        metavar='<phylip_interleaved|phylip_sequential>',
        type=str,
        choices=['interleaved','sequential'],
        default='interleaved',
        help='specify the PHYLIP format')
    args = parser.parse_args()
    return args

args = parse_args()

if __name__ == '__main__':
    args = parse_args()
    if args.format == 'interleaced':
        args.format = 'phylip'
    else:
        args.format = 'phylip-sequential'
    records = AlignIO.parse(sys.argv[1], args.format)
    AlignIO.write(records, sys.stdout, 'fasta')