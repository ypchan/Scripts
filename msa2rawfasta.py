#!/usr/bin/env python3
'''
msa2rawfasta.py -- delete gap symbol "-" from aligned fasta

Date: 2021-07-03
Bugs: Any bugs should be reported to chenyanpeng1992@outlook.com
'''

import sys
import argparse
import fileinput

parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('msa',
    metavar='<msa.fasta>',
    type=str,
    help='multiple sequence alignment file in fasta format, stdin allowed')

args = parser.parse_args()

fa_dict = {}

with fileinput.input(args.msa) as fafh:
    for line in fafh:
        line = line.rstrip('\n')
        if line.startswith('>'):
            seqid = line.lstrip('>')
            fa_dict[seqid] = []
        else:
            line = line.replace('-', '')
            fa_dict[seqid].append(line)

fa_dict = {k:''.join(v) for k,v in fa_dict.items()}

linewidth = 80
for seqid,sequence in fa_dict.items():
    print(f'>{seqid}')
    start = 0
    while len(sequence) > linewidth:
        print(sequence[start:start + linewidth])
        start += linewidth
        sequence = sequence[start:]
    print(sequence)