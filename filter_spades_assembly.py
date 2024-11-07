#!/usr/bin/env python3
import argparse

def parse_header(header):
    parts = header.split('_')
    length = int(parts[3])
    coverage = float(parts[5])
    return length, coverage

def filter_sequences(input_file, min_length, min_coverage):
    keep_sequence = False
    with open(input_file, 'r') as file:
        for line in file:
            if line.startswith('>'):
                header_line = line.strip()
                length, coverage = parse_header(header_line)
                keep_sequence = length >= min_length and coverage >= min_coverage
                if keep_sequence:
                    print(header_line)
            else:
                if keep_sequence:
                    print(line.strip())

def main():
    parser = argparse.ArgumentParser(description='Filter sequences by length and coverage.')
    parser.add_argument('input_file', type=str, help='Input file containing sequences')
    parser.add_argument('--min_length', type=int, default=0, help='Minimum sequence length')
    parser.add_argument('--min_coverage', type=float, default=0.0, help='Minimum sequence coverage')

    args = parser.parse_args()

    filter_sequences(args.input_file, args.min_length, args.min_coverage)

if __name__ == '__main__':
    main()

