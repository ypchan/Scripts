#!/usr/bin/env python3
'''
determine_genome_assemble_level.py -- determine the genome assemble level (contig or scaffold)


Date: 2020-10-9
Bugs: Any bugs should be reported to yanpengch@qq.com

**Principles:**
Contigs are continuous stretches of sequence containing only A, C, G, or T bases without gaps.
Scaffolds are created by chaining contigs together using additional information about the relative position and orientation of the contigs in the genome. Contigs in a scaffold are separated by gaps, which are designated by a variable number of ‘N’ letters.
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

def whether_genome_is_made_of_contigs(genome):
    '''Check whether the genome includes 'N'
    '''
    N_count_lst = []
    base_count_lst = []
    with open(genome) as fh:
        for line in fh:
            line = line.rstrip('\n').upper()
            if line.startswith('>'):
                continue
            else:
                base_count_lst.append(len(line))
                N_count_lst.append(line.count('N'))
    N_sum = sum(N_count_lst)
    base_sum = sum(base_count_lst)
    if N_sum / base_sum >= 0.0001:
        print(genome, "scaffolds", sep = '\t', file = sys.stdout, flush = True)
    else:
        print(genome, "contigs", sep = '\t', file = sys.stdout, flush = True)

if __name__ == '__main__':
    if args.genome_path:
        whether_genome_is_made_of_contigs(args.genome_path)
        sys.exit(0)

    if args.genome_list:
        with open(args.genome_list) as listfh:
            genome_path_lst = [genome_path.strip().rstrip('\n') for genome_path in listfh.readlines()]
        
        # multiple cpu
        pool = multiprocessing.Pool(args.cpu)
        pool.map(whether_genome_is_made_of_contigs, genome_path_lst)
        pool.close()
        pool.join()
    sys.exit(0)