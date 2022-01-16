#!/usr/bin/env python3
'''
check_whether_speceis_has_nucleotide_sequence.py -- check whether the given species has sequencing data in NCBI database(nucleotide)

Date: 2020-10-9
Bugs: Any bugs should be reported to yanpengch@qq.com
'''

import os
import sys
import argparse
import subprocess

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)

input_item = parser.add_mutually_exclusive_group(required=True)
input_item.add_argument('--species_name',
                        type=str,
                        metavar='<Species name>',
                        help='Species name must be in Binomial Nomenclature')
input_item.add_argument('--species_list',
                        type=str,
                        metavar='<species_list.txt>',
                        help='a TXT file, one record per line')

args = parser.parse_args()

def query_ncbi_using_esearch(query_words):
    '''Search NCBI nucleotide database using the tool esearch
    '''
    command = f'esearch -db nucleotide -query "{query_words}"'
    p = subprocess.Popen(command,
                         stdout = subprocess.PIPE,
                         stdin = subprocess.PIPE,
                         shell = True,
                         encoding='utf-8')
    stdout, stderr = p.communicate()
    count_records = stdout.split('\n')[4].lstrip('  <Count>').rstrip('</Count>')
    print(query_words, count_records, sep = '\t', file = sys.stdout, flush = True)

if __name__ == '__main__':
    if args.species_name:
        query_ncbi_using_esearch(args.species_name)
    if args.species_list:
        with open(args.species_list) as listfh:
            for query_words in listfh:
                query_words = query_words.strip().rstrip('\n')
                query_ncbi_using_esearch(query_words)
    sys.exit(0)