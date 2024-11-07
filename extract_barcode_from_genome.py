#!/usr/bin/env python3
'''
ftk_extract_barcode_from_genome -- extract barcode sequences from genome sequence.

Date:
    2023-07-03
Bugs: 
    Any bugs should be reported to yanpengch@qq.com.
'''
import os
import sys
import argparse

def parse_args():
    '''Parse command-line arguments.
    '''
    parser = argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('-i', '--input',
                        metavar='<genome.fa>',
                        required=True,
                        type=str,
                        nargs='+',
                        help='genome file(s) in FASTA format, or multi-fasta folder(s)')

    parser.add_argument('-b', '--barcode',
                        choices=['SSU', 'ITS', 'LSU', 'TEF', 'RPB2', 'TUB', 'RPB1', 'ACT', 'CAL', 'GAPDH', 'HIS'],
                        type=str,
                        args='+',
                        help='print sizes in human readable format,k,M,G')
    
    parser.add_argument('-p', '--prefix',
                        metavar='<int>',
                        type=int,
                        help='specify the number of decimal places (default: 2)')

    parser.add_argument('-l', '--flank_length',
                        metavar='<int>',
                        type=int,
                        default=100,
                        help='length of flanking sequences of matched region. Default=100')
    
    args = parser.parse_args()
    return args