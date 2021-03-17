#!/usr/bin/env python3
'''
beast_label_change.py -- change beast summary result labels

DATE : 2021-03-14
AUTOR: chenyanpeng1992@outlook.com
USAGE:
    beast_label_change.py mapfile.txt beastSummary.tree >  beastSummary.nex
'''
import sys
import argparse

def parse_args():
    '''Parse command-line arguments.
    '''
    parser = argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('beasttree',
                        metavar='<beastSummary.tree>',
                        type=str,
                        help='beast summary tree file')

    parser.add_argument('mapfile',
                        metavar='<map.txt>',
                        type=str,
                        help='tow-column file. oldid and newid')

    parser.add_argument('-c', '--oldidcolumn',
                        metavar='<int>',
                        choices=[1,2],
                        default=1,
                        type=int,
                        help='specify the column of oldid (default: 1)')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    map_dict = {}
    with open(args.mapfile) as mapfh:
        for line in mapfh:
            if args.oldidcolumn == 1:
                oldid, newid = line.rstrip('\n').split()
            else:
                newid, oldid = line.rstrip('\n').split()
            map_dict[oldid] = newid

    replace = False
    with open(args.beasttree) as beastfh:
        for line in beastfh:
            line = line.rstrip('\n')
            if line.endswith('Taxlabels'):
                print(line, file=sys.stdout, flush=True)
                replace = True
                continue

            if line.endswith(';'):
                print(line, file=sys.stdout, flush=True)
                relpace = False
                continue

            if line.endswith('Translate'):
                print(line, file=sys.stdout, flush=True)
                replace = True
                continue

            if line.endswith('Translate'):
                print(line, file=sys.stdout, flush=True)
                replace = True
                continue

            if replace:
                # Taxlabels
                if len(line.split()) == 1:
                    oldid = line.strip()

                    if oldid in map_dict:
                        newid = map_dict[oldid]
                        newline = line.replace(oldid, newid)
                        print(newline, file=sys.stdout, flush=True)
                        continue
                    else:
                        sys.exit(f'Error message:\n    {oldid} not in mapfile')

                # Translate
                if len(line.split()) == 2:
                    oldid = line.split()[1].rstrip(',')
                    newid = map_dict[oldid]
                if oldid in map_dict:
                    newid = map_dict[oldid]
                    newline = line.replace(oldid, newid)
                    print(newline, file=sys.stdout, flush=True)
                    continue
                else:
                    sys.exit(f'Error message:\n    {oldid} not in mapfile')
            else:
                print(line, file=sys.stdout, flush=True)