#!/usr/bin/env python3
'''
base_locate -- show bases by sequence name and position(s)

AUTHOR:
    chenyanpeng1992@outlook.com
DATE：
    2021-01-21
'''

import sys
import gzip
import argparse

def parse_args():
    '''Parse command-line arguments

    Return:
        args (object) : args.<args>
    '''
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('fasta',
        metavar='<fasta>',
        type=str,
        help='input fasta filename')

    parser.add_argument('seqid',
        type=str,
        metavar='<seqid>',
        help='sequence identifier')

    parser.add_argument('loc',
        type=str,
        metavar='<loc ...>',
        nargs='+',
        help='position or pos-range. Eg. 11 11-15')

    args = parser.parse_args()
    return args

def parse_fa_2dict(fafile):
    '''Parse fasta file(.gz allowed) into python3 dictionary, without '>' and newline signs(\n)
    {'id':'seq', ...}

    Args:
        fafile (str): A file name with corresponding path, and the file must be in FASTA format

    Return:
        fa_dict (dict) :A python3 dictionary without '>' and newline signs(\n). {'id':'seq', ...}
    '''
    fa_dict = {}

    fa_fh = gzip.open(fafile, 'rt') if fafile.endswith('.gz') else open(fafile, 'rt')
    for line in fa_fh:
        if not line:
            continue
        line = line.rstrip('\n')
        if line.startswith('>'):
            seq_id = line.lstrip('>').rstrip('\n').split()[0]
            fa_dict[seq_id] = []
        else:
            fa_dict[seq_id].append(line)
    fa_dict = {seq_id:''.join(seq_lst) for seq_id,seq_lst in fa_dict.items()}
    return fa_dict

def base_locater(fa_dict, seq_id, position_tuple):
    '''Get the base according position(s)

    Input:
        position_tuple : 11-15, 11, 12, 12-13
    Result:
        Flag | Bases
        -----|-------
        11-15: ATGCA
        11   : A
        12   : T
        12-13: TG

    Args:
        fa_dict (dict) : a genome fasta. Keys represent seq identifiers, and values represent sequences
        seq_id (str) : sequence identifier
        position_tuple (tuple) : a int tuple

    Return:
        NULL
    '''
    max_len_of_flag = max([len(a) for a in position_tuple])
    for pos in position_tuple:
        if '-' in pos:
            pos_start, pos_end = [int(i) for i in pos.split('-')]
            show_bases = fa_dict[seq_id][pos_start - 1: pos_end]
            print(f'{pos:<{max_len_of_flag}} : {show_bases}', file=sys.stdout, flush=True)
        else:
            pos = int(pos)
            show_base = fa_dict[seq_id][pos]
            print(f'{pos:<{max_len_of_flag}} : {show_base}', file=sys.stdout, flush=True)

if __name__ == '__main__':
    args = parse_args()
    fa_dict =parse_fa_2dict(args.fasta)
    base_locater(fa_dict, args.seqid, args.loc)