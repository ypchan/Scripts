#!/usr/bin/env python3
'''
filter_protein_by_length.py -- filter protein sequences by length

DATE:
    2021-01-07
BUGS：
    Any bugs should be sent to chenyanpeng1992@outlook.com
'''

import sys
import gzip
import argparse

def parse_args():
    '''Parse command-line arguments.
    '''
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('input',
        metavar='<in-fasta>',
        type=str,
        help='input fasta filename')

    parser.add_argument('output',
        type=str,
        metavar='<out-fasta>',
        help='output fasta filename (suffix .gz for gzipped out)')
    
    parser.add_argument('-l', '--length',
        type=int,
        metavar='<int>',
        default=50,
        help='minimal length of the protein sequence (default to 50)')

    args = parser.parse_args()
    return args

def fasta_2dict(infile):
    '''
    Parse fasta into python dictionary

    Parameter
    ---------
    infile : str
        input file in FASTA format

    Return
    ------
    fa_dict : dict
        python dictionary, keys represent protein names and values represent sequence lst
    '''
    fa_fh = gzip.open(infile, 'rt') if infile.endswith('.gz') else open(infile, 'rt')

    fa_dict = {}
    for line in fa_fh:
        if line.startswith('>'):
            protein_id = line
            fa_dict[protein_id] = []
        else:
            fa_dict[protein_id].append(line)
    fa_fh.close()
    return fa_dict

def filter_by_length(fa_dict, length):
    '''
    Removed protein if the it's length short than given length

    Parameter
    ---------
    fa_dict : dict
        python dictionary, keys represent contig names and values represent sequence list
    length : int
        the minimal length of protein sequences.

    Return
    ------
    filtered_dict : dict
        Filtered protein dict
    [num_before, num_after] : list
        num_before and num_after represent the number of proteins before filtering and after respectively
    '''
    filtered_dict = {}
    for protein_id, seq_lst in fa_dict.items():
        line_width_lst = [len(line) - 1 for line in seq_lst]
        seq_length = sum(line_width_lst)
        if seq_length >= length:
            filtered_dict[protein_id] = seq_lst

    num_before = len(fa_dict)
    num_after = len(filtered_dict)
    return filtered_dict, [num_before, num_after]


def out_fasta(filtered_dict, outfile):
    '''
    Out filtered protein sequences in FASTA format

    Parameters
    ----------
    filtered_dict : dict
        Filtered protein dict
    outfile : str
        outfilename (suffix .gz for gzipped out)
    '''
    ofh = gzip.open(outfile, 'w') if outfile.endswith('.gz') else open(outfile, 'w')
    for protein_id, seq_lst in filtered_dict.items():
        ofh.write(protein_id)
        for line in seq_lst:
            ofh.write(line)
    ofh.close()

if __name__ == '__main__':
    args = parse_args()
    fa_dict = fasta_2dict(args.input)
    filtered_dict, [num_before, num_after] = filter_by_length(fa_dict, args.length)
    print(f'Before filtering: {num_before}', file=sys.stdout, flush=True)
    print(f'After  filtering: {num_after}', file=sys.stdout, flush=True)
    out_fasta(filtered_dict, args.output)