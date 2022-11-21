#!/usr/bin/env python3
'''
ftk_gc_content.py -- gc-content percentage is calculated as the following
                     count(G + C) / count(A + T + G + C) * 100%

DATE: 2020-10-10
BUGS: Any bugs should be reported to yanpengch@qq.com
'''

import sys
import argparse
import multiprocessing

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)

input_item = parser.add_mutually_exclusive_group(required=True)
input_item.add_argument(
    '-g',
    '--genome',
    type=str,
    metavar='GENOME',
    help='specify a genome file in FASTA format')

input_item.add_argument(
    '-G',
    '--genome_list',
    type=str,
    metavar='GENOME_LIST',
    help='a text file, one record per line')

parser.add_argument(
    '-t',
    '--genome_type',
    type=str,
    metavar='GENOME_TYPE',
    default='normal',
    choices=['normal', 'hardmasked', 'softmasked'],
    help='genome type can be normal/hardmasked/softmasked. \
        if it is normal or hardmasked, only GC content;\
             else GC(overall) GC(norepeat) GC(repeat)')

parser.add_argument(
    '-c',
    '--cpu',
    type=int,
    metavar='INT',
    default=4,
    help='#cpu to use, only applies with --genome_list')

args = parser.parse_args()


def calculate_gc_content(genome, genome_type):
    '''Check whether the genome caontains unknown or masked character 'N'
    '''
    A_base_count = []
    T_base_count = []
    G_base_count = []
    C_base_count = []

    a_base_count = []
    t_base_count = []
    g_base_count = []
    c_base_count = []

    with open(genome) as fh:
        for line in fh:
            line = line.rstrip('\n')
            if line.startswith('>'):
                continue
            else:
                A_base_count.append(line.count('A'))
                T_base_count.append(line.count('T'))
                G_base_count.append(line.count('G'))
                C_base_count.append(line.count('C'))
                a_base_count.append(line.count('a'))
                t_base_count.append(line.count('t'))
                g_base_count.append(line.count('g'))
                c_base_count.append(line.count('c'))

    total_base = sum(A_base_count) \
        + sum(T_base_count) \
        + sum(G_base_count) \
        + sum(C_base_count) \
        + sum(a_base_count) \
        + sum(t_base_count) \
        + sum(g_base_count) \
        + sum(c_base_count)

    clear_base = sum(A_base_count) \
        + sum(T_base_count) \
        + sum(G_base_count) \
        + sum(C_base_count) \

    if genome_type == 'softmasked':
        total_gc_content = (sum(G_base_count)
                            + sum(C_base_count)
                            + sum(g_base_count)
                            + sum(c_base_count)) / total_base * 100

        clear_gc_content = (sum(G_base_count)
                            + sum(C_base_count)) / clear_base * 100

        repeat_gc_content = (sum(g_base_count)
                             + sum(c_base_count)) / (total_base - clear_base) * 100

        print(genome, total_gc_content, clear_gc_content,
              repeat_gc_content, sep='\t', file=sys.stdout, flush=True)
    else:
        print(genome, total_gc_content, sep='\t', file=sys.stdout, flush=True)


def main():
    if args.genome:
        calculate_gc_content(args.genome, args.genome_type)
        sys.exit(0)

    if args.genome_list:
        with open(args.genome_list) as listfh:
            genome_path_lst = [genome_path.strip().rstrip('\n')
                               for genome_path in listfh.readlines()]

        # multiple cpu
        pool = multiprocessing.Pool(args.cpu)
        pool.map(calculate_gc_content, genome_path_lst)
        pool.close()
        pool.join()


if __name__ == '__main__':
    main()
    sys.exit(0)
