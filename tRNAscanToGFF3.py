#!/usr/bin/env python3
'''
tRNAscanToGFF3 -- convert tRNAscan-SE output BED file to gff3 file.

DATE:
    2020-10-17
BUGS:
    Any bugs should be send to 764022822@qq.com
'''

import sys
import argparse
import fileinput


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('input',
        metavar='<bed-file>',
        type=str,
        help='input file in BED format, allowed stdin')
        
    args = parser.parse_args()
    return args

def bed_to_5_column(arg_bedfile):
    '''Convert bed file to five-column column.

    @parameter: arg_bedfile -- tRANscan-SE output file.

    SRR10641223_mt  692     761     SRR10641223_mt.tRNA1-IleGAT     997     +       692     761     0       1       69,     0,
    SRR10641223_mt  758     829     SRR10641223_mt.tRNA21-GlnTTG    892     -       758     829     0       1       71,     0,
    SRR10641223_mt  828     897     SRR10641223_mt.tRNA2-MetCAT     1000    +       828     897     0       1       69,     0,
    SRR10641223_mt  1941    2010    SRR10641223_mt.tRNA20-AlaTGC    966     -       1941    2010    0       1       69,     0,
    SRR10641223_mt  2015    2081    SRR10641223_mt.tRNA19-CysGCA    699     -       2015    2081    0       1       66,     0,
    ...
    '''
    source = 'tRNAscan-SE'
    feature = 'tRNA'
    score = '.'
    phase = '.'

    for line in fileinput.input(files=arg_bedfile, mode='r'):

        line_lst = line.split('\t')
        sequence, start, end, product = line_lst[0:4]
        strand, exon_s, exon_e = line_lst[5:8]
        product = product.lstrip(sequence + '.').split('-')[1][:3]
        product = 'tRNA-' + product
        attributes = 'product=' + product

        if int(start) > int(end):
            start, end = end, start

        if int(exon_s) > int(exon_e):
            exon_s, exon_e = exon_e, exon_s

        tRNA_line_list = [sequence, source, feature, start, end, score, strand, phase, attributes]
        tRNA_line = '\t'.join(tRNA_line_list)

        exon_line_lst = [sequence, source, 'exon', exon_s, exon_e, score, strand, phase, attributes]
        exon_line = '\t'.join(exon_line_lst)
        print(tRNA_line)
        print(exon_line)

    fileinput.close()

if __name__ == '__main__':
    args = parse_args()
    bed_to_5_column(args.input)