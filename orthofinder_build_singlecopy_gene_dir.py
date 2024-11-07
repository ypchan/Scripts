#!/usr/bin/env python3
'''
orthofinder_single_copy_dataset.py -- create single-copy protein datasets according orthofinder result: Orthogroups.tsv

DATE: 2023-05-23
BUGS: Any bugs should be reported to yanpengch@qq.com
'''
import os
import sys
import time
import tqdm
import argparse

import pandas as pd

parser = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('--tsv',
                    required=True,
                    type=str,
                    metavar='Orthogroups.tsv',
                    help = 'Orthogroups.tsv from orthofinder output')
parser.add_argument('--list',
                    required=True,
                    type=str,
                    metavar='label_path.list',
                    help = 'two-column list: taxa label\tabspath.pep')
parser.add_argument('--coverage',
                    default=80,
                    type=int,
                    metavar='80',
                    help = 'taxa coverage. Default: 80')
parser.add_argument('--directory',
                    required=True,
                    type=str,
                    metavar='single_copy_coverage',
                    help = 'filename of output directory. Orthogroup is will be fasta file name, and the taxa label will be sequence IDs')

args = parser.parse_args()

def read_orthogroup_matrix_2_dataframe(tbl):
    # read orthofinder result file: Orthogroups.tsv into python dataframe
    # first column is index, representing the cluster IDs
    # first row is colnames, representing the species IDs
    try:
        orthogroup_dataframe = pd.read_table(tbl, index_col=0, low_memory=False)
    except FileNotFoundError:
        sys.exit(f'Error: parse {tbl} into dataframe failed ')

    num_rows, num_cols = orthogroup_dataframe.shape[0], orthogroup_dataframe.shape[1]
    print('-' * 20, file=sys.stdout, flush=True)
    print(f'Number of orthogroups: {num_rows}', file=sys.stdout, flush=True)
    print(f'Number of genomes    : {num_cols}', file=sys.stdout, flush=True)
    return orthogroup_dataframe

def orthogroup_dataframe_2_count_matrix(orthogroup_dataframe):
    # get count dataframe by counting gene number in each cell
    count_dataframe = orthogroup_dataframe.applymap(lambda cell: len(cell.split(', ')) if isinstance(cell, str) else 0)
    return count_dataframe

def single_copy_orthogroups(count_dataframe, taxa_coverage):
    # according given taxa coverage to get the single copy orthogroup dataframe
    mask = count_dataframe.apply(lambda row: ((row != 0).sum() / len(row) >= taxa_coverage/100) and not any(cell > 1 for cell in row), axis=1)
    single_copy_dataframe = count_dataframe[mask]
    num_rows, num_cols = single_copy_dataframe.shape[0], single_copy_dataframe.shape[1]
    print(f'single-copy orthogroups: {num_rows}', file=sys.stdout, flush=True)
    return single_copy_dataframe

def read_all_pep_2_dict(args_list):
    # read all pep file into python3 dictionary
    fa_dict = {}
    lable_2_path = {}
    with open(args_list) as lst_fh:
        for line in lst_fh:
            taxa_label, pep_path = line.rstrip('\n').split('\t')
            lable_2_path[taxa_label] = pep_path
    
    taxa_label_lst = list(lable_2_path.keys())
    pbar = tqdm.tqdm(taxa_label_lst)
    for taxa_label in pbar:
        pbar.set_description('Reading ' + taxa_label)
        pep_path = lable_2_path[taxa_label]
        fa_dict[taxa_label] = {}
        with open(pep_path) as fafh:
            for line in fafh:
                line = line.rstrip('\n')
                if line.startswith('>'):
                    seq_id = line.split()[0].lstrip('>')
                    fa_dict[taxa_label][seq_id] = []
                else:
                    fa_dict[taxa_label][seq_id].append(line)
    return fa_dict

def output_single_copy_sequences(fa_dict, single_copy_count_dataframe, orthogroup_dataframe, outdirectory):
    if os.path.exists(outdirectory):
        sys.exit(f'Error: output directory {outdirectory} already exists. Try new output dirname or remove the directory.')
    else:
        os.mkdir(outdirectory)
    print(f'Output single-copy datasets: {outdirectory}', file = sys.stdout, flush = True)
    single_copy_dataframe = orthogroup_dataframe.loc[list(single_copy_count_dataframe.index)]

    for row_index, row in single_copy_dataframe.iterrows():  # iterate over rows
        fa_filename = outdirectory + '/' + row_index + '.faa'
        if os.path.exists(fa_filename):
            sys.exit(f'Error: {fa_filename} already exists.')

        with open(fa_filename, 'wt') as fafh:
            for column_index, geneid in row.items():
                try:
                    sequence = ''.join(fa_dict[column_index][geneid])
                except KeyError:
                    #print(column_index, geneid)
                    continue
                fafh.write('>' + column_index + '\n' + sequence + '\n')

if __name__ == '__main__':
    st = time.time()
    fa_dict = read_all_pep_2_dict(args.list)
    orthogroup_dataframe = read_orthogroup_matrix_2_dataframe(args.tsv)
    count_dataframe = orthogroup_dataframe_2_count_matrix(orthogroup_dataframe)
    single_copy_dataframe = single_copy_orthogroups(count_dataframe, args.coverage)
    output_single_copy_sequences(fa_dict, single_copy_dataframe, orthogroup_dataframe, args.directory)
    print('-' * 20, file=sys.stdout, flush=True)
    elapsed_time = time.time() - st
    print('Elapsed time:', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)), file=sys.stdout, flush=True)
    sys.exit(0)