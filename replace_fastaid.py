#!/usr/bin/env python3
'''
replace_fastaid.py -- replace fastaid.

Date: 2021-05-10
Bugs: Any bugs should be reported to chenyanpeng1992@outlook.com
Usage:
    replace_fastaid.py mapfile.txt multifasta.fna out.fna
'''
import sys
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('map',
                        metavar='<map.txt>',
                        type=str,
                        help='input filename, amino acid codons should be abbreviated or completed.')

    parser.add_argument('fasta',
                        metavar='<multifasta.fna>',
                        type=str,
                        help='input file must be in FASTA format')

    parser.add_argument('out',
                        metavar='<out.fna>',
                        type=str,
                        help='output file name')

    parser.add_argument('--map_header',
                        action='store_true',
                        help='if --map_header, the map file with header line')

    parser.add_argument('--oldid_field',
                        metavar='<int>',
                        type=int,
                        help='specify old field')

    parser.add_argument('--new_id_field',
                        metavar='<int>',
                        type=int,
                        help='specify new id field')
    args = parser.parse_args()
    return args


def fastaid_map(mapfile, header=True):
    '''group id and corresponding single-fasta id
    '''
    mapdict = {}
    with open(mapfile) as mapfh:
        counter = 0
        for line in mapfh:
            counter += 1
            if header:
                if counter == 1:
                    continue
            new, _, raw = line.rstrip('\n').split()
            mapdict[raw] = new
    return mapdict


def fasta2dict(multifastafile):
    fadict = {}
    with open(sys.argv[2]) as multifastafh:
        for line in multifastafh:
            if line.startswith('>'):
                fastaid = line.lstrip('>').split()[0].rstrip('\n')
                fadict[fastaid] = []
            else:
                fadict[fastaid].append(line)
    fadict = {k: ''.join(v) for k, v in fadict.items()}
    return fadict


if __name__ == '__main__':
    args = parse_args()

    mapdict = fastaid_map(args.map, args.map_header)
    fadict = fasta2dict(args.fasta)
    with open(sys.argv[3], 'wt') as outfh:
        for k, v in fadict.items():
            outfh.write(f'>{mapdict[k]}\n{v}')
