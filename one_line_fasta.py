#!/usr/bin/env python3

# update: 2024-01-26
# bugs: yanpengch@qq.com

import sys
import argparse
import fileinput

def read_fasta_file(fasta_filename):
    '''read mult-fasta file into python dict
    '''
    fa_dict = {}
    with fileinput.input(fasta_filename, 'rt') as fh:
        for line in fh:
            line = line.rstrip('\n')
            if line.startswith('>'):
                fa_id = line.lstrip('>').split()[0]
                fa_dict[fa_id] = []
            else:
                fa_dict[fa_id].append(line.upper())

    fa_dict = {k:''.join(v) for k,v in fa_dict.items()}
    return fa_dict

def output_one_line_fasta(fa_dict):
    '''write one line fasta
    '''
    for fa_id,fa_seq in fa_dict.items():
        print(f'>{fa_id}\n{fa_seq}', file=sys.stdout, flush=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert multi-line FASTA to one-line FASTA.')
    parser.add_argument('input_file', metavar='input_file', type=str, help='Path to the input multi-line FASTA file.')

    args = parser.parse_args()

    fa_dict = read_fasta_file(args.input_file)
    output_one_line_fasta(fa_dict)
    sys.exit(0)

