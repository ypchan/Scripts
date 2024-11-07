#!/usr/bin/env python3
'''
n50.py -- stat N50 of genome assembly

Date: 2022-11-25
Bugs: Any bugs should be reported to yanpengch@qq.com

Input:
../00_genome_data/Aciaci1.fna
../00_genome_data/Corma2.fna
'''
import sys
import argparse


parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument(
    '-i',
    '--input',
    type=str,
    required=True,
    help='genome file')


args = parser.parse_args()

fa_dict = dict()
with open(args.input, 'rt') as infh:
    for line in infh:
        line = line.rstrip('\n')
        if line.startswith('>'):
            contig_id = line.split()[0]
            fa_dict[contig_id] = []
        else:
            fa_dict[contig_id].append(line)

fa_dict = {k: ''.join(v) for k, v in fa_dict.items()}
fa_length = [len(v) for k, v in fa_dict.items()]
total_length = sum(fa_length)
fa_length.sort(reverse=True)
c_length = 0
for i in fa_length:
    c_length += i
    if c_length >= total_length / 2:
        print(args.input, i, sep='\t', file=sys.stdout, flush=True)
        break
sys.exit(0)
