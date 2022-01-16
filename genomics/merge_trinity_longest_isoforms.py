#!/usr/bin/env python3
'''
merge_longest_trinity_isoforms.py -- merge multiple trinity longest isorform fasta file

DATE:
    January 9, 2021
BUGS：
    Any bugs should be sent to chenyanpeng1992@outlook.com
'''

import os
import sys
import argparse

def parse_args():
    '''
    Parse command-line arguments

    Parameter
    ---------
    NULL

    Return
    ------
    NULL
    '''
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('indir',
        metavar='<directory>',
        type=str,
        help='input directory')

    args = parser.parse_args()
    return args

def merge_and_output(indir):
    '''
    Merge multiple fasta, and prefix fasta seq id with filename

    Parameter
    ---------
    indir : str
        input directory consists of multiple longets isoforms fasta file

    Return
    ------
    NULL
    '''
    fa_lst  = os.listdir(indir)
    fa_lst = [indir + '/' + fa for fa in fa_lst]

    for fa in fa_lst:
        prefix_id = os.path.basename(fa).rstrip('_longest.fna')
        with open(fa) as fafh:
            for line in fafh:
                if line.startswith('>'):
                    line = line.replace('TRINITY', prefix_id)
                print(line, end='', file=sys.stdout)

if __name__ == '__main__':
    args = parse_args()
    merge_and_output(args.indir)