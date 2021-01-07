#!/usr/bin/env python3
'''
filter_coantigs.py -- filter genome assemblies by length

DATE:
    2020-01-05
BUGS：
    Any bugs should be sent to chenyanpeng1992@outlook.com
'''

import os
import sys
import gzip
import argparse

def parse_args():
    '''
    Parse command-line arguments

    Parameter
    ---------
    NULL

    Return
    ------
    args : a python3 object, and arguments as args.<arg>
    '''
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('input',
                        metavar='<in-fasta>',
                        type=str,
                        help='input file in FASTA format')

    parser.add_argument('-l', '--length',
                        type=int,
                        default=1000,
                        metavar='<int>',
                        help='set minimal length of the contigs [default: 1000]')

    parser.add_argument('out',
                        type=str,
                        metavar='<out-fasta>',
                        help='output filename')
    args = parser.parse_args()
    return args

def fasta_2dict(infile):
    '''
    Parse fasta into python dictionary

    Parameter
    ---------
    infile : str
        input filename in FASTA format

    Return
    ------
    fa_dict : dict
        python dictionary, keys represent contig names and values represent sequences
    '''
    fa_fh = gzip.open(infile, 'rt') if infile.endswith('.gz') else open(infile, 'rt')

    fa_dict = []
    for line in fa_fh:
        if line.startswith('>'):
            contig_id = line
            fa_dict[contig_id] = []
        else:
            fa_dict[contig_id].append(line)
    fa_fh.close()
    return fa_dict

def filter_by_length(fa_dict, length):
    '''
    Removed contigs that short than length

    Parameter
    ---------
    fa_dict : dict
        python dictionary, keys represent contig names and values represent sequences
    length : int
        the minimal length of contigs

    Return
    ------
    filtered_dict : dict
        filtered fasta dictionary
    '''
    filtered_dict = {}
    for contig_id, seq_lst in fa_dict.items():
        num_newline = len(seq_lst)
        seq_len = len(''.join(seq_lst)) - num_newline
        if seq_len >= length:
            filtered_dict[contig_id] = seq_lst
    return seq_lst

def out_fasta(filtered_dict, outfile):
    '''
    Output filtered fasta file. If outfile not be specified, output will be redirected to stdout

    Parameter
    --------
    filtered_dict : dict
        filtered fasta dictionary

    Return
    ------
    NULL
    '''
    with open(outfile, 'wt') as outfa_fh:
        for contig_id,seq_lst in filtered_dict.items():
            outfa_fh.write(contig_id)
            outfa_fh.write(''.join(seq_lst))

if __name__ == '__main__':
    args = parse_args()
    fa_dict = fasta_2dict(args.input)
    filtered_dict = filter_by_length(fa_dict, args.length)
    out_fasta(filtered_dict, args.out)