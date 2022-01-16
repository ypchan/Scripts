#!/usr/bin/env python3
'''
genome_size.py -- Genome size(bp) = No. A + No. T + No.G + No. C

Date: 2020-10-14
Bugs: Any bugs should be reported to yanpengch@qq.com
'''

import os
import sys
import argparse
import subprocess
import multiprocessing

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)

input_item = parser.add_mutually_exclusive_group(required=True)
input_item.add_argument('--genome_path',
                        type=str,
                        metavar='<genome.fasta>',
                        help='genome file in FASTA format')

input_item.add_argument('--genome_list',
                        type=str,
                        metavar='<genome_list.txt>',
                        help='a TXT file, one record per line')

parser.add_argument('--cpu',
                    type=int,
                    metavar='<int>',
                    default=4,
                    help='No. cpu to query NCBI nucleotide database. Only useful with --species_list')

args = parser.parse_args()

def count_genome_base(genome):
    '''Check whether the genome includes 'N'
    '''
    A_base_count = []
    T_base_count = []
    G_base_count = []
    C_base_count = []
    with open(genome) as fh:
        for line in fh:
            line = line.rstrip('\n').upper()
            if line.startswith('>'):
                continue
            else:
               A_base_count.append(line.count('A'))
               T_base_count.append(line.count('T'))
               G_base_count.append(line.count('G'))
               C_base_count.append(line.count('C'))
    total_base = sum(A_base_count) + sum(T_base_count) + sum(G_base_count) + sum(C_base_count)
   
    print(genome, total_base, sep = '\t', file = sys.stdout, flush = True)

if __name__ == '__main__':
    if args.genome_path:
        count_genome_base(args.genome_path)
        sys.exit(0)

    if args.genome_list:
        with open(args.genome_list) as listfh:
            genome_path_lst = [genome_path.strip().rstrip('\n') for genome_path in listfh.readlines()]
        
        # multiple cpu
        pool = multiprocessing.Pool(args.cpu)
        pool.map(count_genome_base, genome_path_lst)
        pool.close()
        pool.join()
    sys.exit(0)