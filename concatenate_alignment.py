#!/usr/bin/env python3
'''
concatenate_alignment.py -- concatenate different marker sequences of each taxon in multiple alignment files

DATE: 2022-01-19
BUGS: Any bugs should be reported to yanpengch@qq.com
'''

import os
import sys
import argparse

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('-i', '--input',
    required=True,
    nargs='+',
    type=str,
    metavar='<msa.fna>',
    help='multiple alignment files with common IDs')

parser.add_argument('-o', '--output',
    required=True,
    type=str,
    metavar='<concatenated.fa>',
    help='concatenated MSA filename')

parser.add_argument('-p', '--partition',
    type=str,
    metavar='<partition_region.txt>',
    default='parts_region.txt',
    help='parts and the corresponding region')

parser.add_argument('-m', '--missing_part',
    type=str,
    metavar='<missing_taxa.txt>',
    default='missing_taxa.txt',
    help='missing taxa of each part')

args = parser.parse_args()

def all_taxa(msafile_tuple):
    '''Getting all taxa table.
    '''
    all_msa_dict = {}
    taxa_lst = []
    for msa in msafile_tuple:
        all_msa_dict[msa] = {}
        with open(msa, 'rt') as fafh:
            for line in fafh:
                line = line.rstrip('\n')
                if line.startswith('>'):
                    taxa_id = line.lstrip('>')
                    taxa_lst.append(taxa_id)
                    all_msa_dict[msa][taxa_id] = []
                else:
                    all_msa_dict[msa][taxa_id].append(line)
    taxa_set = list(set(taxa_lst))

    for msa, fa_dict in all_msa_dict.items():
        all_msa_dict[msa] = {k:''.join(v) for k,v in fa_dict.items()}
    return taxa_lst, all_msa_dict

def get_msa_length(all_msa_dict):
    '''Getting msa length.
    '''
    msa_length_dict = {}
    start = 1
    print('', file=sys.stdout, flush=True)
    with open(args.partition, 'wt') as patitionfh:
        for msa,fa_dict in all_msa_dict.items():
            for taxa_id, seq in fa_dict.items():
                fa_length = len(seq)
                msa_length_dict[msa] = fa_length
                end = start + fa_length - 1
                print(f'{msa}\t{start}-{end}', file=sys.stdout, flush=True)
                patitionfh.write(f'{msa}\t{start}-{end}\n')
                start = start + fa_length
                break

    return msa_length_dict

def add_missingdata_to_alignment(taxa_lst, all_msa_dict, msa_length_dict):
    '''Adding missing data into some msa file.
    '''
    print('', file=sys.stdout, flush=True)
    print('#Msa\tLength\tCount', file=sys.stdout, flush=True)
    with open(args.missing_part, 'wt') as missingfh:
        for msa, fadict in all_msa_dict.items():
            msa_length = msa_length_dict[msa]
            taxa_missing_lst = []
            for taxa_id in taxa_lst:
                if taxa_id not in fadict:
                    taxa_missing_lst.append(taxa_id)
                    all_msa_dict[msa][taxa_id] = '?' * msa_length

            print('#' + msa, msa_length, len(taxa_missing_lst), file=sys.stdout, flush=True)
            print('#' + msa, msa_length, len(taxa_missing_lst), file=missingfh, flush=True)
            print("\n".join(taxa_missing_lst) + '\n', file=sys.stdout, flush=True)
            print("\n".join(taxa_missing_lst) + '\n', file=missingfh, flush=True)
    return all_msa_dict

def combine(taxa_lst, all_msa_dict):
    '''Combing msa file by common ids
    '''
    combine_dict = {}
    for taxa_id in taxa_lst:
        combine_dict[taxa_id] = []
        for msa, fa_dict in all_msa_dict.items():
            seq = fa_dict[taxa_id]
            combine_dict[taxa_id].append(seq)
    return combine_dict

if __name__ == '__main__':
    taxa_lst, all_msa_dict = all_taxa(args.input)
    msa_length_dict = get_msa_length(all_msa_dict)
    all_msa_dict = add_missingdata_to_alignment(taxa_lst, all_msa_dict, msa_length_dict)
    combine_dict = combine(taxa_lst, all_msa_dict)

    with open(args.output, 'wt') as outfh:
        for taxa_id, seq in combine_dict.items():
            outfh.write(f'>{taxa_id}\n{"".join(seq)}\n')
