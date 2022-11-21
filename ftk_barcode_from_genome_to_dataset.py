#!/usr/bin/env python3

'''
ftk_barcode_from_genome_to_dataset.py -- file contains all barcode to file only contain one barcode but cover all taxa.

AUTHOR: yanpengch@qq.com
DATE  : 2022-09-25
'''

import os
import sys
import fileinput

fa_dict = dict()
barcode_lst = []
with fileinput.FileInput(sys.argv[1]) as infh:

    for line in infh:
        file_name = line.rstrip('\n')
        base_name = os.path.basename(file_name)
        fa_dict[base_name] = dict()
        with open(file_name) as infh:
            for line in infh:
                line = line.rstrip('\n')
                if line.startswith('>'):
                    seq_id = line.lstrip('>').split()[0]
                    barcode_lst.append(seq_id)
                    fa_dict[base_name][seq_id] = []
                else:
                    fa_dict[base_name][seq_id].append(line)


barcode_lst = list(set(barcode_lst))

for barcode in barcode_lst:
    with open(barcode + '.fna', 'wt') as outfh:
        for file_name, sub_dict in fa_dict.items():
            try:
                seq_lst = sub_dict[barcode]
                seq = ''.join(seq_lst)
                outfh.write(f'>{file_name}\n{seq}')
            except KeyError:
                continue
sys.exit(0)
