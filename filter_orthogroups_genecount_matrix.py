#!/usr/bin/env python3
'''
filter_orthogroups_genecount_matrix.py -- filter  gene count matrix (Orthofinder Result) according given arguments.

Bugs : Any bugs should be reported to chenyanpeng1992@outlook.com
Date : 2021-04-30
'''
import sys
import argparse

def parse_args():
    '''Parse command-line arguments
    '''
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('input',
        metavar='<orthogroups_genecount.tsv>',
        type=str,
        help='OrthoFinder result file')

    parser.add_argument('coverage',
        type=float,
        metavar='<percent_cov>',
        help='percent of species coverage')

    parser.add_argument('-o', '--out',
        type=str,
        metavar='<outname>',
        help='output filename')

    args = parser.parse_args()
    return args

def filter_by_species_coverage(genecount_matrix, percent_coverage):
    '''filter orthofroups according species coverage
    '''
    after_orthogroup_dict = {}
    with open(genecount_matrix) as matrixfh:
        n = 0
        num_orthogroup_filtered = 0
        for line in matrixfh:
            n += 1
            line_lst = line.rstrip('\n').split('\t')
            if n == 1:
                head_line_lst = line_lst
                continue

            orthogroup_name = line_lst[0]
            orthogroup_gene_count_lst = line_lst[1:]
            # percent of genomes share this orthogroup
            if orthogroup_gene_count_lst.count('0') / len(orthogroup_gene_count_lst) > percent_coverage:
                num_orthogroup_filtered += 1
            else:
                after_orthogroup_dict[orthogroup_name] = orthogroup_gene_count_lst
    print("==================Summary==================", file=sys.stdout)
    print(f"Number of orthogroups         : {n}", file=sys.stdout)
    print(f'Number of filtered orthogroups: {num_orthogroup_filtered}', file=sys.stdout)
    return head_line_lst, after_orthogroup_dict

if __name__ == '__main__':
    args = parse_args()
    head_line_lst, after_orthogroup_dict = filter_by_species_coverage(args.input, args.coverage)
    with open(args.out, 'wt') as outfh:
        outfh.write('\t'.join(head_line_lst) + '\n')
        for orthogroup, orthogroup_genecount_lst in after_orthogroup_dict.items():
            outfh.write(orthogroup + '\t' + '\t'.join(orthogroup_genecount_lst) + '\n')
