#!/usr/bin/env python3

import sys


all_dict = {}
with open(sys.argv[1], 'rt') as infh:
    for line in infh:
        line_lst = line.rstrip('\n').split('\t')
        genome_assembly = line_lst[0]
        gene_length = int(line_lst[2])
        if genome_assembly not in all_dict:
            all_dict[genome_assembly] = [gene_length]
        else:
            all_dict[genome_assembly].append(gene_length)

print(f'Assembly\tMin\tMax\tMean', file=sys.stdout, flush=True)
for genome_assmebly, length_lst in all_dict.items():
    print(f'{genome_assmebly}\t{min(length_lst)}\t{max(length_lst)}\t{mean(length_lst)}',
          file=sys.stdout, flush=True)
sys.exit(0)
