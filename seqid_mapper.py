#!/usr/bin/env python3
'''
seqid_mapper -- change sequence ids according to given mapping file

DATE:
    2021-01-07
BUGS：
    Any bugs should be sent to chenyanpeng1992@outlook.com
'''

import sys
import gzip
import argparse

def parse_args():
    '''Parse command-line arguments

    Return
        object : args.<args>
    '''
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('input',
        metavar='<in-fasta>',
        type=str,
        help='input fasta filename')

    parser.add_argument('mapfile',
        type=str,
        metavar='<mapfile>',
        help='two-column mapfile, 1st column lists old ids, 2ed column lists new ids')

    parser.add_argument('--format',
        default='fasta',
        type=str,
        choices=['fasta', 'clustal'],
        metavar='<fasta|clustal>',
        help='specify the file format')

    parser.add_argument('--strip_minor',
        action='store_true',
        help='strip sequence minor version no.')

    args = parser.parse_args()
    return args

def mapping_dict(mapfile):
    '''Parse mapfile into python3 dictionary

    Args:
        mapfile (str) : input file, a tab-delimited file. 1st column lists old ids, 2nd column lists new ids

    Return:
        dict : a python dictionary, keys represent old ids, and values represent new ids
    '''
    map_dict = {}
    with open(mapfile, 'rt') as map_fh:
        for line in map_fh:
            [old_id, new_id] = line.rstrip('\n').split('\t')
            map_dict[old_id] = new_id

    return map_dict

def out_fasta(infile, map_dict, fileformat, strip):
    '''Out ids cahgned protein sequences in FASTA format

    Args:
        infile (str) : input file in FASTA format
        map_dcit (dict) : a python dictionary, keys represent old ids, and values represent new ids
    Rerutn:
        NULL
    '''
    if fileformat == 'fasta':
        infh = gzip.open(infile, 'rt') if infile.endswith('.gz') else open(infile, 'rt')
        for line in infh:
            # Skip blank line
            if not line:
                continue

            if line.startswith('>'):
                old_id = line.lstrip('>').rstrip('\n').split()[0]
                if strip:
                    old_id = '.'.join(old_id.split('.')[:-1])

                line = line.replace(old_id, map_dict.get(old_id, old_id), 1)
                print(line, end='', file=sys.stdout, flush=True)
            else:
                print(line, end='', file=sys.stdout, flush=True)
    else:
        infh = open(infile, 'rt')
        for line in infh:
            if line.startswith('CLUSTAL'):
                print(line, end='', file=sys.stdout, flush=True)
                continue
            if line == '\n':
                print(line, end='', file=sys.stdout, flush=True)
                continue

            try:
                old_id = line.split()[0]
                old_id = '.'.join(old_id.split('.')[:-1])
            except:
                print(line)
                sys.exit(1)
            line = line.replace(old_id, map_dict.get(old_id, old_id), 1)
            print(line, end='', file=sys.stdout, flush=True)

if __name__ == '__main__':
    args = parse_args()
    map_dict = mapping_dict(args.mapfile)
    out_fasta(args.input, map_dict, args.format, args.strip_minor)