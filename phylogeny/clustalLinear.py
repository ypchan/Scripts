#!/usr/bin/env python3
'''
clustalLinear.py -- present sequence per sequence per line.

DATE:
    2020-10-30
BUGS：
    Any bugs should be sent to chenyanpeng1992@outlook.com
'''

import os
import sys
import argparse
import fileinput

def parse_args():
    '''Parse command-line arguments.
    '''
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('input',
        metavar='<clw-file>',
        type=str,
        help='input clustal file')

    args = parser.parse_args()
    return args

def clw2_line(clwfile):
    '''Parse clw file into dict, and output each sequence per line.
    '''
    clwfh = fileinput.input(files=clwfile)

    clw_dict = {}
    for line in clwfh:
        if line.startswith('CLUSTAL format'):
            clustal_header = line.rstrip('\n')
            continue

        if not line.strip():
            continue

        line_lst = line.rstrip('\n').split()
        if len(line_lst) != 2:
            continue

        if '.' in line_lst[1] or '*' in line_lst[1]:
            continue

        ID, seq = line_lst
        if ID not in clw_dict:
            clw_dict[ID] = [seq]
        else:
            clw_dict[ID].append(seq)

    clw_dict = {ID:''.join(seq_lst) for ID, seq_lst in clw_dict.items()}

    # output
    print(clustal_header,file=sys.stdout, flush=True)
    print('',file=sys.stdout, flush=True)
    print('',file=sys.stdout, flush=True)

    max_id_len = max([len(ID) for ID in clw_dict])
    for ID, seq in clw_dict.items():
        line = f'{ID:<{max_id_len}}    {seq}'
        print(line, file=sys.stdout, flush=True)

    fileinput.close()

if __name__ == '__main__':
    args = parse_args()
    clw2_line(args.input)