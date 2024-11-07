#!/usr/bin/env python3
'''
fishergene.py -- extract gene from gff3 according gene ids

DATE:
    2020-04-12
BUGS：
    Any bugs should be sent to chenyanpeng1992@outlook.com
'''
import re
import sys
import argparse
import fileinput
from collections import defaultdict

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('baits',
                        metavar='<genes.txt>',
                        type=str,
                        help='gene list (allowed stdin)')

    parser.add_argument('gff3',
                        type=str,
                        metavar='<gff3>',
                        help='the 2rd input file in bed format (.gz allowed)')
    args = parser.parse_args()

    gff3fh = open(args.gff3)
    gene_lst = [line.rstrip('\n') for line in fileinput.input(files=args.baits)]
    gene_mRNA_dict = defaultdict(list)
    for line in gff3fh:
        if line.startswith('#'):
            continue
        seqid, source, feature, start, end, score, strand, phase, attrs = line.split('\t')
        if feature == 'mRNA':
            mRNAid = re.search(r'ID=(.*?)[;\n]', attrs).group(1)
            parent_geneid = re.search(r'Parent=(.*?)[;\n]', attrs).group(1)
            if parent_geneid in gene_mRNA_dict:
                sys.exit(f'Error message: duplicate geneid {parent_geneid}')
            gene_mRNA_dict[parent_geneid].append(mRNAid)

    mRNA_lst = [mRNAid for gene in gene_lst for mRNAid in gene_mRNA_dict[gene]]

    gff3fh.seek(0)
    for line in gff3fh:
        if line.startswith('#'):
            print(line, end='')
            continue
        seqid, source, feature, start, end, score, strand, phase, attrs = line.split('\t')
        if feature == 'gene':
            geneid = re.search(r'ID=(.*?)[;\n]', attrs).group(1)
            if geneid in gene_lst:
                print(line, end='')
                continue
        if feature == 'mRNA':
            parent_geneid = re.search(r'Parent=(.*?)[;\n]', attrs).group(1)
            if parent_geneid in gene_lst:
                print(line, end='')
                continue
        if feature == 'exon':
            parent_mRNAid = re.search(r'Parent=(.*?)[;\n]', attrs).group(1)
            if parent_mRNAid in mRNA_lst:
                print(line, end='')
                continue

        if feature == 'CDS':
            parent_mRNAid = re.search(r'Parent=(.*?)[;\n]', attrs).group(1)
            if parent_mRNAid in mRNA_lst:
                print(line, end='')
                continue
    gff3fh.close()