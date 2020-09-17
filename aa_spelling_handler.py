#!/usr/bin/env python3
'''
aa_abbreviation_2whole.py -- Transforming an amino acid three-letter abbreviation to one-letter or its intact spelling.

DATE:
    2020-05-26
BUGS:
    Any bugs should be send to chenyanpeng1992@outlook.com
'''

import sys
import argparse
import fileinput

amino_acids_13dict = {
'G': 'Gly', 'A': 'Ala', 'V': 'Val', 'L': 'Leu', 'I': 'Ile', 'F': 'Phe','W': 'Trp', 
'Y': 'Tyr', 'D': 'Asp', 'H': 'His', 'N': 'Asn', 'E': 'Glu', 'K': 'Lys', 'Q': 'Gln',
'M': 'Met', 'R': 'Arg', 'S': 'Ser', 'T': 'Thr','C': 'Cys', 'P': 'Pro'
}

amino_acids_30dict = {
'Gly': 'Glycine', 'Ala': 'Alanine', 'Val': 'Valine', 'Leu': 'Leucine', 'Ile': 'Isoleucine', 'Phe': 'Phenylalanine',
'Trp': 'Tryptophan', 'Tyr': 'Tyrosine', 'Asp': 'Aspartate', 'His': 'Histidine', 'Asn': 'Asparagine', 'Glu': 'Glutamate',
'Lys': 'Lysine', 'Gln': 'Glutamine', 'Met': 'Methionine', 'Arg': 'Arginine', 'Ser': 'Serine', 'Thr': 'Threonine',
'Cys': 'Cysteine', 'Pro': 'Proline'
}

amino_acids_10dict = {
'G': 'Glycine','A': 'Alanine','V': 'Valine','L': 'Leucine','I': 'Isoleucine','F': 'Phenylalanine','W': 'Tryptophan','Y': 'Tyrosine',
'D': 'Aspartate','H': 'Histidine','N': 'Asparagine','E': 'Glutamate','K': 'Lysine','Q': 'Glutamine','M': 'Methionine','R': 'Arginine',
'S': 'Serine','T': 'Threonine','C': 'Cysteine','P': 'Proline'
}

def parse_args():
    parser = argparse.ArgumentParser(
    	description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('input',
        metavar='<infile>',
        type=str,
        help='input filename, amino acid codons should be abbreviated or completed.')

    parser.add_argument('-a', '--action',
        metavar="['01', '03', '10', '13', '30', '31']",
        type=str,
        choices=['01', '03', '10', '13', '30', '31'],
        required=True,
        help='01:complete -> One-letter; 03:complete -> Three-letter; 13:One-letter -> Three-letter ...')
    parser.add_argument('-d', '--delimiter', 
        metavar='<str>',
        type=str,
        default='\t',
        help='delimiter of line [default: "\\t"]')
    parser.add_argument('-f', '--field',
        metavar='<int>',
        type=int,
        default=0,
        help='field of amino acid codons [default: entire line]')
    args = parser.parse_args()
    return args

def aa01(string):
    for a,b in amino_acids_10dict.items():
        string = string.replace(b, a)
    return string

def aa10(string):
    for a,b in amino_acids_10dict.items():
        string = string.replace(a, b)
    return string

def aa13(string):
    for a, b in amino_acids_13dict.items():
        string = string.replace(a, b)
    return  string

def aa31(string):
    for a, b in amino_acids_13dict.items():
        string = string.replace(b, a)
    return  string

def aa03(string):
    for a,b in amino_acids_30dict.items():
        string = string.replace(b, a)
    return string

def aa30(string):
    for a,b in amino_acids_30dict.items():
        string = string.replace(a, b)
    return string

def main():
    args = parse_args()
    infh = fileinput.input(files=args.input)

    for line in infh:
        line = line.rstrip('\n')
        if args.field:
            line_lst = line.split(args.delimiter)
            if args.action == '01':
                line_lst[args.field - 1] = aa01(line_lst[args.field - 1])
            elif args.action == '10':
                line_lst[args.field - 1] = aa01(line_lst[args.field - 1])
            elif args.action == '13':
                line_lst[args.field - 1] = aa13(line_lst[args.field - 1])
            elif args.action == '31':
                line_lst[args.field - 1] = aa31(line_lst[args.field - 1])
            elif args.action == '03':
                line_lst[args.field - 1] = aa03(line_lst[args.field - 1])
            elif args.action == '30':
                line_lst[args.field - 1] = aa30(line_lst[args.field - 1])
            else:
                sys.eixt('Error: invalid action.')
            line = args.delimiter.join([line_lst])
        else:
            if args.action == '01':
                line = aa01(line)
            elif args.action == '10':
                line = aa01(line)
            elif args.action == '13':
                line = aa13(line)
            elif args.action == '31':
                line = aa31(line)
            elif args.action == '03':
                line = aa03(line)
            elif args.action == '30':
                line = aa30(line)
            else:
                sys.eixt('Error: invalid action.')
        print(line, file=sys.stdout, flush=True)
    infh.close()

if __name__ == '__main__':
    sys.exit(main())