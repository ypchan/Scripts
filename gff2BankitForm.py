#!/usr/bin/env python
'''
Name:
    gff2BankitForm.py written by chenyanpeng@dnastories.com, 2020-06-19
Synopsis:
    Create a five-column, tab-delimited feature table for submission through BankIt or for the update an existing GenBank entry.
Inputfile:
    sample.gff[3] # input file must be in gff3 format
Outputfile:
    sample.bankit.tsv # a tab-separated file
    ##headline
    >Feature SeqID ## SeqID must corrsepond to the fasta id:>SeqID
Example:
    1: ./gff3BankitForm.py input.gff -t Name > out.tsv
    2: cat input.gff | ./gff2BankitFormPy2.py - -t product > out.tsv
'''
from __future__ import print_function
import sys
import argparse
import fileinput

def parse_args():
    parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("gff3", metavar='gff3file', type=str,
            help='input annotation file that must be in gff3 format, allowed stdin')
    parser.add_argument('-t', '--tag', metavar='<Name>', type=str, default='Name',
            help='annotation tag in the 9 column [default: Name]. Example 1: ...;Name=hypothetical protein...; Example 2: ;product=hypothetical protein')
    args = parser.parse_args()
    return args

def parse_gff3_2_bankit_form(gff3file, tag):
    gff3_fh = fileinput.input(files=gff3file)

    last_seq_id = ''
    print('>Feature SeqID', file=sys.stdout)
    for line in gff3_fh:
        if line.startswith('#'):
            continue
        else:
            line = line.rstrip('\n')
            line_lst = line.split('\t')
            if len(line_lst) != 9:
                continue

            seq_id = line_lst[0]
            feature = line_lst[2]
            feature_l = line_lst[3]
            feature_r = line_lst[4]
            strand = line_lst[6]
            product = [product.lstrip(tag + '=') for product in line_lst[8].split(';') if product.startswith(tag)][0]

        if strand == '-':
            feature_l, feature_r = feature_r, feature_l

        print('%s\t%s\t%s' % (feature_l, feature_r, feature), file=sys.stdout)
        print('\t\t\tproduct\t%s' % product, file=sys.stdout)
    gff3_fh.close()

if __name__ == '__main__':
    args = parse_args()
    parse_gff3_2_bankit_form(args.gff3, args.tag)
