#!/usr/bin/env python
import argparse
from Bio import SeqIO

def parse_args():
    parser = argparse.ArgumentParser(description="Filter FASTA sequences by length")
    parser.add_argument('-i', '--input', required=True, help="Input FASTA file")
    parser.add_argument('-o', '--output', required=True, help="Output FASTA file")
    parser.add_argument('-s', '--min_len', type=int, default=400, help="Minimum sequence length")
    parser.add_argument('-m', '--max_len', type=int, default=1500, help="Maximum sequence length")
    return parser.parse_args()

def filter_fasta_by_length(input_file, output_file, min_len, max_len):
    with open(output_file, 'w') as out_f:
        for seq_record in SeqIO.parse(input_file, 'fasta'):
            if min_len <= len(seq_record.seq) <= max_len:
                SeqIO.write(seq_record, out_f, 'fasta')

if __name__ == "__main__":
    args = parse_args()
    filter_fasta_by_length(args.input, args.output, args.min_len, args.max_len)
