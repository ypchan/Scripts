#!/usr/bin/env python3

'''
check_start_stop_codon.py -- check whether the CDS contain start and stop codon

DATE:
    2021-01-07
BUGS：
    Any bugs should be sent to chenyanpeng1992@outlook.com
'''

import sys
import argparse

def parse_args():
    '''Parse command-line parameters

    Return:
        object : args.<args>
    '''
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('fasta',
        metavar='<fasta>',
        type=str,
        help='input fasta filename')
    
    parser.add_argument('gff3',
        type=str,
        metavar='<gff3file>',
        help='gff3 file')

    args = parser.parse_args()
    return args


