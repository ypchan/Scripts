#!/usr/bin/env python3
'''
fastaSegment.py -- get intervals according bed file.

DATE:
    2020-10-30
BUGS：
    Any bugs should be sent to chenyanpeng1992@outlook.com
'''

import os
import sys
import gzip
import argparse
import fileinput

def parse_args():
    '''Parse command-line arguments.
    '''
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('fasta',
        metavar='<fasta-file>',
        type=str,
        help='input bed file')

    parser.add_argument('bed',
        metavar='<bed-file>',
        type=str,
        help='input bed file')
    args = parser.parse_args()
    return args

def fa2dict(fafile):
    '''Parse fasta file into dict.
    '''
    fafh = gzip.open(fafile, 'rt') if fafile.endswith('.gz') else open(fafile, 'rt')

    fa_dict = {}
    for line in fa:
        line = line.rstrip('\n')

        if line.startswith('>'):
            ID = line.split()[0]
            fa_dict[ID] = []
        else:
            fa_dict[ID].append(line)
    fafh.close()

    fa_dict = {ID:''.join(line_lst) for ID, line_lst in fa_dict.items()}
   return fa_dict

def bed2dict(bedfile):
    '''Parse bed file to dict.

    #ID     ITS1.start      ITS2.end
    NR_073212       31      585
    NR_073222       31      586
    NR_073235       31      436
    NR_073272       31      532
    '''
    bedfh = open(bedfile, 'rt')
    
    bed_dict ={}
    for line in bedfh:
        line = line.rstrip('\n')
        if line.startswith('>'):
            continue

        bed_lst = line.split()
        ID, start, end = bed_lst
        bed_dict[ID] = (int(start), int(end))
    bedfh.close()

    return bed_dict

def out_intervals(fa_dict, bed_dict):
    for ID in bed_dict:
        start, end = bed_dict[ID]
        interval = fa_dict[start - 1:end]
        print(f'>{ID}', file=sys.stdout, flush=True)
        print(f'{interval}', file=sys.dtdout, flush=True)

if __name__ == '__main__':
    args = parse_args()
    fa_dict = fa2dict(args.fasta)
    bed_dict = bed2dict(args.bed)
    out_intervals(fa_dict, bed_dict)