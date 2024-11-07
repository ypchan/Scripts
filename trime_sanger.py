#!/usr/bin/env python3

'''
trim_sanger.py -- trim sanger sequencing result: sanger.seq

DATE: 2023-06-05
BUGS: Any bugs should be reported to yanpengch@qq.com
'''
import os
import sys
import argparse


parser = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('--input',
                    required=True,
                    type=str,
                    nargs='+',
                    metavar='sanger.seq',
                    help = 'sanger sequencing result file: sanger.seq')
parser.add_argument('--head',
                    default=0,
                    type=int,
                    metavar='10',
                    help = 'trim #N bases from the left')
parser.add_argument('--tail',
                    default=0,
                    type=int,
                    metavar='10',
                    help = 'trim #N bases from the right')

args = parser.parse_args()

def read_seq(seq_file):
    out_prefix = os.path.basename(seq_file).rstrip('.seq')
    seq_string = ''
    with open(seq_file, 'rt') as infh:
        for line in infh:
            seq_string += line.rstrip('\n')
    return out_prefix, seq_string

def trim_seq(head_num, tail_num, seq_string):
    trimmed_seq = seq_string[head_num:-tail_num]
    return trimmed_seq

def write_fasta(trimmed_seq, out_prefix):
    out_filename = out_prefix + '.fasta'
    with open(out_filename, 'wt') as outfh:
        outfh.write(f'>{out_prefix}\n{trimmed_seq}\n')

if __name__ == '__main__':
    for seq_file in args.input:
        out_prefix, seq_string = read_seq(seq_file)
        trimmed_seq = trim_seq(args.head, args.tail, seq_string)
        write_fasta(trimmed_seq, out_prefix)
    sys.exit(0)