#!/usr/bin/env python3
'''
split_multifasta2signlefasta_file.py -- split multi-FASTA file to multiple single-FASTA files.

Date: 2021-05-10
Bugs: Any bugs should be reported to chenyanpeng1992@outlook.com
Usage:
    split_multifasta2singlefasta_file.py mapfile.txt multifasta.fna

Input:
    ##mapfile.txt:
    groupid      fastaid
    GO00001      NR1243243
Out：
    groupid-named single-fasta file with original fastaid as defline
'''

import os
import sys
import fileinput

def groupid_fastaid(mapfile, header=True):
    '''group id and the corresponding single-fasta id
        ##mapfile.txt:
        groupid      fastaid
        GO00001      NR1243243

        header：specify whether the mapping file includes a head line
    '''
    mapdict = {}
    for line in fileinput.input(mapfile):
        groupid, fastaid = line.rstrip('\n').split()
        mapdict[fastaid] = groupid
    fileinput.close()
    return mapdict

def fasta2dict(multifastafile):
    '''Parse fasta file into python3 dictionary
    '''
    fadict = {}
    with open(sys.argv[2]) as multifastafh:
        for line in multifastafh:
            if line.startswith('>'):
                fastaid = line.lstrip('>').split()[0].rstrip('\n')
                fadict[fastaid] = []
            else:
                fadict[fastaid].append(line)
    fadict = {k:''.join(v) for k,v in fadict.items()}
    return fadict

def single2multiple_line(singleline, width=80):
    '''Convert single-line characteis into multiple lines and return a multiple line list

        singleline: single line character
        width:      how many characters per line (default: 80)
    '''
    start = 0
    end = start + width
    short_line_lst = []
    while end < len(singleline):
        short_line = singleline[start:end]
        short_line_lst.append(short_line)
        start += width
        end += width

    the_last_short_line = singleline[start:end]
    short_line_lst.append(the_last_short_line)

    return short_line_lst

if __name__ == '__main__':
    if len(sys.argv) == 1 or (sys.argv[1] in ['-h', '--help', '-help']):
        sys.exit(__doc__)

    mapdict = groupid_fastaid(sys.argv[1], header=True)
    fadict = fasta2dict(sys.argv[2])
    for k,v in fadict.items():
        line_list = single2multiple_line(v)
        line = '\n'.join(line_list)
        singlefsata_filename = mapdict[k] + '.fna'
        with open(singlefsata_filename, 'wt') as outfh:
            outfh.write(f'>{k}\n{v}')