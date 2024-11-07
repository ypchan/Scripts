#!/usr/bin/env python3

# update: 2024-02-07
# bugs  : yanpengch@qq.com

import os
import re
import argparse

# Creating the parser for command line arguments
parser = argparse.ArgumentParser(description="Summarize BGC counts from files.")
# Adding an argument to accept multiple file paths
parser.add_argument('files',
    nargs='+',
    type=str,
    help='File paths to process')
parser.add_argument('--output',
    default='sordariales.BGCs.summary.tsv',
    type=str,
    help='output filename')

args = parser.parse_args()  # Parsing the arguments provided

if __name__ == '__main__':
    summary_dict = {}
    category_lst = ['total']
    # Using args.files to process multiple input files specified on the command line
    for filename in args.files:
        genome_label = os.path.basename(filename)
        summary_dict[genome_label] = {}
        with open(filename, 'rt') as infh:
            for line in infh:
                if re.search(r"\* (\d+) BGCs", line):
                    total_num = line.split()[1]
                    summary_dict[genome_label]['#total'] = total_num
                if re.search(r"(\d+)\t", line):
                    count, category = line.rstrip('\n').split('\t')
                    if category not in category_lst:
                        category_lst.append(category)
                    summary_dict[genome_label][category] = count
    header_lst = ['Label'] + category_lst
    # Using with statement to ensure the output file is properly closed
    with open('sordariales.bgcs.summary.tsv', 'wt') as outfh:
        outfh.write('\t'.join(header_lst) + '\n')
        for genome_label in summary_dict:
            out_line_lst = [genome_label]  # Initializing the list with the genome label
            for category in category_lst:
                if category in summary_dict[genome_label]:
                    out_line_lst.append(summary_dict[genome_label][category])
                else:
                    out_line_lst.append('0')  # Ensuring data type consistency by using string '0'
            outfh.write('\t'.join(out_line_lst) + '\n')  # Converting the list to a string for writing to the file

    # The script ends normally, so there's no need to call sys.exit(0) unless you need to return a non-zero status code to indicate an error
