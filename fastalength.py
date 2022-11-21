#!/usr/bin/env python3

'''
fastalength.py -- calucate the fasta length

AUTHOR: yanpengch@qq.com
DATE  : 2022-09-24
USAGE : 
    fastalength.py input.fa
    cat input.fa | fastalength.py -  
'''

import sys
import fileinput


if len(sys.argv) <= 1:
    print(__doc__, file=sys.stderr, flush=True)
    sys.exit(1)

if (sys.argv[1] in ['-h', '--h', '-help', '--help']) or (len(sys.argv) > 2):
    print(__doc__, file=sys.stderr, flush=True)
    sys.exit(1)


with fileinput.FileInput(sys.argv[1]) as infh:
    count = 0
    for line in infh:
        if line.startswith('>') and count == 0:
            print(line.lstrip('>') + '\t', end='', file=sys.stdout, flush=True)

        elif line.startswith('>') and count != 0:
            print(count, file=sys.stdout, flush=True)
            print(line.lstrip('>') + '\t', end='', file=sys.stdout, flush=True)
            count = 0

        else:
            count += len(line.rstrip('\n'))
    print(count, file=sys.stdout, flush=True)
sys.exit(0)
