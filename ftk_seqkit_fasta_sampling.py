#!/usr/bin/env python3

# update: 2024-02-01
# bugs  : yanpengch@qq.com

import os
import sys
import argparse

# check the requirements first.
if os.system('seqkit --help &> /dev/null'):
    print('Error: cd-hit is required. Please install it.', file=sys.stderr, flush=True)
    sys.exit(1)

# add command-line argument parser
parser = argparse.ArgumentParser(description="sampling FASTA by given proporatins")
parser.add_argument('--fasta', '-f',
        required=True,
        metavar='Periconia_ITS.fasta',
        help='barcode sequences in multi-fasta format.')

parser.add_argument('--proportion', '-p',
        nargs="+",
        required=True,
        type=float,
        metavar="0.25 0.50 0.75 1",
        help='Proporations.')

parser.add_argument('--out_prefix', '-o',
        type=str,
        required=True,
        help='prefix the output.')

args = parser.parse_args()

def run(fasta, proportion, prefix):
    command = f"seqkit sample -p {proportion} {fasta} >{prefix}_{proportion}.fasta"
    try:
        os.system(command)
    except:
        sys.exit(f'Error: run seqkit error. \n    {command}')
    print(f"[INFO] {fasta}    {proportion}\n")

if __name__ == '__main__':
    for proportion in args.proportion:
        run(args.fasta, proportion, args.out_prefix)
    sys.exit(0)

