#!/usr/bin/env python3
'''
gc_content.py -- gc-content percentage is calculated as Count(G + C)/Count(A + T + G + C) * 100%

Date: 2020-10-10
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
input_item.add_argument('--genome',
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
                    help='No. cpu to query NCBI nucleotide database. Only useful with --genome_list')

args = parser.parse_args()

def calculate_gc_content(genome):
    '''Check whether the genome includes character 'N'
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
    GC_base_sum = sum(G_base_count) + sum(C_base_count)
    gc_conttent = GC_base_sum / total_base * 100
    print(genome, gc_conttent, sep = '\t', file = sys.stdout, flush = True)

if __name__ == '__main__':
    if args.genome:
        calculate_gc_content(args.genome)
        sys.exit(0)

    if args.genome_list:
        with open(args.genome_list) as listfh:
            genome_path_lst = [genome_path.strip().rstrip('\n') for genome_path in listfh.readlines()]
        
        # multiple cpu
        pool = multiprocessing.Pool(args.cpu)
        pool.map(calculate_gc_content, genome_path_lst)
        pool.close()
        pool.join()
    sys.exit(0)