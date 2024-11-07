#!/usr/bin/env python3

"""
genome_stat.py --stat basic information of genome assemblies.

date: 2024-07-28
bugs: yanpengch@qq.com
usage:
    ls 00_genomes/*.fna | genome_stat.py -t 4 - > genome.statistics.tsv
    find 00_genomes -name "*.fna" -type f | genome_stat.py -t 4 - > genome.statistics.tsv
"""

import csv
import sys
import argparse
import fileinput
from concurrent.futures import ThreadPoolExecutor, as_completed

def stat(genome_file):
    with open(genome_file, 'r') as file:
        sequences = []
        current_seq = []
        for line in file:
            if line.startswith('>'):
                if current_seq:
                    sequences.append(''.join(current_seq))
                    current_seq = []
            else:
                current_seq.append(line.strip())
        if current_seq:
            sequences.append(''.join(current_seq))

    num_fragments = len(sequences)
    gc_content = []
    n_count = 0
    lengths = []

    for sequence in sequences:
        gc_content.append((sequence.count('G') + sequence.count('C')) / len(sequence))
        n_count += sequence.count('N')
        lengths.append(len(sequence))

    if not lengths:
        return (genome_file, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    lengths.sort(reverse=True)
    total_length = sum(lengths)

    def calc_N_L(x):
        cum_len = 0
        for i, length in enumerate(lengths):
            cum_len += length
            if cum_len >= total_length * (x / 100.0):
                return length, i + 1

    N50, L50 = calc_N_L(50)
    N75, L75 = calc_N_L(75)
    N90, L90 = calc_N_L(90)

    return (
        genome_file,
        num_fragments,
        sum(gc_content) / num_fragments,
        n_count,
        max(lengths),
        min(lengths),
        N90, L90,
        N50, L50,
        N75, L75
    )

def process_genomes(genome_files, num_threads):
    results = []
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_genome = {executor.submit(stat, genome): genome for genome in genome_files}
        for future in as_completed(future_to_genome):
            result = future.result()
            results.append(result)
            yield result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", type=str, metavar="<genome_lst.tsv>", help="Path to the file containing genome paths or use '-' for standard input")
    parser.add_argument("-t", "--threads", type=int, default=1, metavar="<1>", help="Number of threads to use. Default 1")

    args = parser.parse_args()

    if args.input == '-':
        genome_files = [line.strip() for line in fileinput.input(files='-')]
    else:
        with open(args.input, 'rt') as file:
            genome_files = [line.strip() for line in file]

    tsvwriter = csv.writer(sys.stdout, delimiter='\t')
    tsvwriter.writerow([
        "Genome", "#Contigs", "GC", "#N_character",
        "Contig_longest", "Contig_minimum", "N90", "L90",
        "N50", "L50", "N75", "L75"
    ])

    for result in process_genomes(genome_files, args.threads):
        tsvwriter.writerow(result)
        sys.stdout.flush()
