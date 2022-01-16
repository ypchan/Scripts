#!/usr/bin/env python3
'''
extract_ITS_sequences.py -- extracte ITS sequences according ITSx result

Date: 2021-06-21
Bugs: Any bugs should be reported to chenyanpeng1992@outlook.com
'''
import os
import sys
import argparse

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('fasta',
    metavar='<ITS.fasta>',
    type=str,
    help='a multiple fasta file')

parser.add_argument('itsxposition',
    metavar='<txt>',
    type=str,
    help='ITSx position result' )
args = parser.parse_args()


def parse_fa2dict(fasta):
    fadict = {}
    with open(fasta) as fafh:
        for line in fafh:
            line = line.rstrip('\n')
            if line.startswith('>'):
                seqid = line.split()[0].lstrip('>')
                fadict[seqid] = []
            else:
                fadict[seqid].append(line)
    fadict = {k:''.join(v) for k,v in fadict.items()}
    return fadict

def parse_itsx_positionfile(itsxposition):
    positiondict = {}
    with open(itsxposition) as pfh:
        for line in pfh:
            line_lst = line.split('\t')
            seqid = line_lst[0]
            its1_start = int(line_lst[3].split(': ')[1].split('-')[0])
            its2_end = int(line_lst[5].split(': ')[1].split('-')[1])
            positiondict[seqid] = [its1_start, its2_end]
    return positiondict

if __name__ == '__main__':
    fadict = parse_fa2dict(args.fasta)
    positiondict = parse_itsx_positionfile(args.itsxposition)
    for seqid,poss in positiondict.items():
        start, end = poss
        print(f'>{seqid}')
        sequence = fadict[seqid][start - 1: end]
        print(f'{sequence}')