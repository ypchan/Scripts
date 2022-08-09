#!/usr/bin/env python3
'''
orthofinder_single_copy_gene_dir.py -- list single-copy genes and the corresponding protein filenames

DATE: 2022-02-02
BUGS: Any bugs should be reported to yanpengch@qq.com
'''
import os
import sys
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 prog='orthofinder_single_copy_gene_lst.py')
parser.add_argument('-i',
                    '--input',
                    required=True,
                    type=str,
                    help = 'single-copy orthogroup matrix: first row represents genome lebels, the first column represents orthogroup IDs')
parser.add_argument('-l',
                    '--fasta_lst',
                    required=True,
                    type=str,
                    help = 'a list comprises the absolute path of all input protein file, the second column can be abbreviation or taxa label')
parser.add_argument('-o',
                    '--output',
                    required=True,
                    type=str,
                    help = 'output dirname to store all single-copy gene familys, orthogroup is will be fasta  faile name, and the taxa label will be defline')

args = parser.parse_args()

def read_singlecopy_matrix_2_table(args_input):
    '''

    Parameters
    ----------
    args_input: orthofinder result file: .../OrthoFinder/Results_Jan29/Orthogroups/Orthogroups.tsv

    Returns
    -------
    dataframe: first row comprises protein file names, the first column comprises the orthogroup ids
         and the other cells contain the gene names

    '''
    try:
        df = pd.read_table(args_input, index_col=0)
    except FileNotFoundError:
        sys.exit(f'Error: parse {args_input} into dataframe failed ')
    print(f'Parse single-copy matrix: {args_input} into python dataframe', file =sys.stdout, flush=True)
    num_rows, num_cols = df.shape[0], df.shape[1]
    print(f'Number of single-copy orthogroups: {num_rows}', file=sys.stdout, flush=True)
    print(f'number of genomes    ：{num_cols}'，file=sys.stdout, flush=True)
    print(df.head(5), sys.stdout, flush=True)
    return df

def read_all_pep_2_dict(args_fasta_lst):
    '''

    Parameters
    ----------
    args_fasta_lst: tab-delimited file, the first comprises abspath of all input fasta file,
                    the second column can be taxa label or the corresponding abbreviation

    Returns
    fa_dict: taxa label as 1st level keys, and the gene ids as 2rd level keys, sequences as the value list.
    '''
    fa_dict = {}
    with open(args_fasta_lst) as lst_fh:
        for line in lst_fh:
            fa_path = line.rstrip('\n')
            taxa_label = os.path.basename(fa_path)
            fa_dict[taxa_label] = {}
            with open(fa_path) as fafh:
                for line in fafh:
                    line = line.rstrip('\n')
                    if line.startswith('>'):
                        fa_id = line.split()[0].lstrip('>')
                        fa_dict[taxa_label][fa_id] = []
                    else:
                        fa_dict[taxa_label][fa_id].append(line)
    return fa_dict

def output_single_copy_sequences(fa_dict, df, output):
    '''

    Parameters
    ----------
    fa_dict: taxa label as 1st level keys, and the gene ids as 2rd level keys, sequences as the value list.
    single_copy_name_df: similar with df, while only single-copy orthogroups are saved

    Returns
    -------
    output dirname, comprising all single-copy orthogroups, groupid as fasta filename, and the taxalabel as deflines

    '''
    if os.path.exists(output):
        sys.exit(f'Error: output directory {output} already exists.')
    else:
        os.mkdir(output)
    print(f'Output single-copy datasets in directory {output}', file = sys.stdout, flush = True)
    for row_index, row in single_copy_name_df.iterrows():  # iterate over rows
        fa_filename = output + '/' + row_index + '.faa'
        if os.path.exists(fa_filename):
            sys.exit(f'Error: {fa_filename} already exists.')
        with open(fa_filename, 'wt') as fafh:
            for column_index, geneid in row.items():
                try:
                    sequence = ''.join(fa_dict[column_index][geneid])
                    fafh.write('>' + column_index + '\n' + sequence + '\n')
                except KeyError:
                    print(column_index, geneid)
                    sys.exit(1)

if __name__ == '__main__':
    df = read_singlecopy_matrix_2_table(args.input)
    fa_dict = read_all_pep_2_dict(args.fasta_lst)
    output_single_copy_sequences(fa_dict, df, args.output)
    sys.exit(0)