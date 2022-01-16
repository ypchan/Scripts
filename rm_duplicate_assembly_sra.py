#!/usr/bin/env python3
'''
rm_duplicate_assembly_sra.py -- manipulate assembly and sra records table

Date: 2021-05-13
Bugs: Any bugs should be reported to chenyanpeng1992@outlook.com
'''

import sys
import argparse

parser = argparse.ArgumentParser(
    	description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('file1',
    metavar='<file1.txt>',
    type=str,
    help='SRA or assembly records table')

parser.add_argument('--field1',
    type=int,
    required=True,
    metavar='<int>',
    help='biosample id field')

parser.add_argument('--header1',
    action='store_true',
    help='if the file1 includes heder line, please use this option')

parser.add_argument('file2',
    type=str,
    metavar='<file2.txt>',
    help='Assembly or SRA records table')

parser.add_argument('--field2',
    type=int,
    required=True,
    metavar='<int>',
    help='biosample id field')

parser.add_argument('--header2',
    action='store_true',
    help='if the file2 includes heder line, please use this option')

parser.add_argument('--reverse',
    action='store_true',
    help='if you want to output duplicate records, please use this option')

args = parser.parse_args()

# obtain biosample id from file1
biosampleid_lst = []
with open(args.file1) as f1fh:
    count = 0
    for line in f1fh:
        count += 1
        if args.head1 and count == 1:
            continue
        line_lst = line.rstrip('\n').split('\t')
        biosampleid = line_lst[args.field1 - 1]
        biosampleid_lst.append(biosampleid)

biosampleid_lst = list(set(biosampleid_lst))

# manipulate file2 records according to biodample id list
with open(args.file1) as f2fh:
    count = 0
    for line in f2fh:
        count += 1
        line_lst = line.rstrip('\n').split('\t')
        if args.head2 and count == 1:
            print(line, end='')
            continue
        biosampleid = line_lst[args.field2 - 1]
        if biosampleid in biosampleid_lst:
            if args.reverse:
                print(line, end ='')
            else:
                continue
        else:
            print(line, end='')