#!/usr/bin/env python3

'''
ftk_blastn_barcode_subject_formatter.py -- calucate the fasta length

AUTHOR: yanpengch@qq.com
DATE  : 2022-09-24
'''

import sys
import fileinput

with fileinput.FileInput(sys.argv[1]) as infh:
    for line in infh:
        file_path, barcodetag = line.rstrip('\n').split()
        with open(file_path, 'rt') as infh, open(barcodetag + '.fna', 'wt') as outfh:
            count = 0
            for line in infh:
                if line.startswith('>'):
                    count += 1
                    outfh.write(f'>{barcodetag}_{count}\n')
                else:
                    outfh.write(line)
sys.exit(0)
