#!/usr/bin/env python3
'''
stat_intergenic_length.py -- obtain distance between two different genes (intergenic length)

Bugs: any bug should reported to yanpengch@qq.com
Date: 2022-11-25
'''
import os
import sys
import argparse


parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('-g', '--gff3',
                    metavar='<gff3>',
                    type=str,
                    required=True,
                    help='input gff3. Required.')
args = parser.parse_args()


def sort_gff3(gff3):
    '''sort gff3 by contig, gene start position
    '''
    command = f"grep -v '#' {gff3} | awk -F '\t' '$3==\"gene\"'| sort -k1,1 -k4,4n > {gff3}_gene_line_tmp"
    p = os.system(command)
    if p != 0:
        sys.exit(f'Error: {command}', file=sys.stderr, flush=True)

    return gff3 + '_gene_line_tmp'


def get_contig_gene_start_lst(gff3_gene_line):
    '''parse gene start and end positions in python dictionary as the following:
            {contig_id:[[g1_start,g1_end], [g2_start, g2_end]...]}

    remove tmp file
    '''
    contig_gene_stat_dict = {}
    with open(gff3_gene_line, 'rt') as infh:
        for line in infh:
            line_lst = line.split('\t')
            contig_id = line_lst[0]
            gene_start_end = [int(line_lst[3]), int(line_lst[3])]
            if contig_id not in contig_gene_stat_dict:
                contig_gene_stat_dict[contig_id] = [gene_start_end]
            else:
                contig_gene_stat_dict[contig_id].append(gene_start_end)

    # reomve temporary file
    command = f'rm {gff3_gene_line}'
    p = os.system(command)
    if p != 0:
        sys.exit(f'Error: {command}')
    return contig_gene_stat_dict


if __name__ == "__main__":
    gff3_gene_line = sort_gff3(args.gff3)
    contig_gene_stat_dict = get_contig_gene_start_lst(gff3_gene_line)
    for contig, gene_start_lst in contig_gene_stat_dict.items():
        if len(gene_start_lst) <= 1:
            continue
        else:
            start_num = len(gene_start_lst)
            for i in range(start_num - 1):
                intergenic_len = gene_start_lst[i +
                                                1][0] - gene_start_lst[i][1] - 1
                print(f"{args.gff3}\t{intergenic_len}",
                      file=sys.stdout, flush=True)
    sys.exit(0)
