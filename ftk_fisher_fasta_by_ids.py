#!/usr/bin/env python

# bugs: yanpengch@qq.com
# date: 2024-01-25

import argparse
from Bio import SeqIO
import sys

def parse_args():
    parser = argparse.ArgumentParser(description="Extract sequences from a FASTA file based on a list of IDs, with an option to reverse the selection.")
    parser.add_argument('-i', '--input', required=True, help="Input FASTA file")
    parser.add_argument('-ids', '--ids', required=True, nargs='+', help="List of sequence IDs to extract")
    parser.add_argument('-r', '--reverse', action='store_true', help="If set, extracts all sequences NOT matching the IDs list")
    return parser.parse_args()

def extract_sequences(input_file, ids_list, reverse):
    sequences_to_extract = set(ids_list)
    extracted_sequences = []

    with open(input_file, 'r') as fasta_file:
        for record in SeqIO.parse(fasta_file, 'fasta'):
            if (record.id in sequences_to_extract) != reverse:  # The '!=' operator works as a XOR here
                extracted_sequences.append(record)

    SeqIO.write(extracted_sequences, sys.stdout, 'fasta')

if __name__ == "__main__":
    args = parse_args()
    extract_sequences(args.input, args.ids, args.reverse)
    sys.exit(0)
