#!/usr/bin/env python3
'''
find_bases_index_in_alignment.py -- find bases cordinate in alignment file that must be in FASTA format

USAGE:
    find_bases_index_in_alignment.py <bases> <representtative_seq>
Example:
    grep "ATGCG" alignment.fasta | head -n 1 | find_bases_index_in_alignment.py "ATGCG" - # please confirm one-line fasta
DATE:
    2021-02-05
BUGS：
    Any bugs should be sent to chenyanpeng1992@outlook.com
'''

import sys
import fileinput

if len(sys.argv) != 3 or '-h' in sys.argv or '--h' in sys.argv or '--help' in sys.argv or '-help' in sys.argv:
    print(__doc__, file=sys.stderr, flush=True)
    sys.exit(1)

seq = fileinput.input(files=sys.argv[2])
fileinput.close()

bases = sys.argv[1]
if not isinstance(bases, str):
    sys.exit(f'Error: {bases} is not valid bases')

bases = bases.strip("\"\'")

start = seq.find(bases) + 1
end = start + len(bases) - 1

if len(bases) > 1:
    print(start, file=sys.stdout, flush=True)
else:
    print(f'{start}-{end}', file=sys.stdout, flush=True)