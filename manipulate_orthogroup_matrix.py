#!/usr/bin/env python3
'''
manipulate_orthogroup_matrix.py -- to manipulate orthofinder output orthogoup matrix

Date: 2020-06-02
Bugs: Any bugs should be reported to chengyanpeng1992@outlook.com
'''

import os
import sys
import argparse
import pandas as pd

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('orthogroup_matrix',
    metavar='<matrixfile>',
    type=str,
    help='singlecopy orthogroups matrix in txt format')

parser.add_argument('--drop_species',
    type=str,
    metavar='<speciesA,speciesB,...>',
    help='species need to be removed from matrix')

parser.add_argument('--drop_orthogroup',
    type=str,
    metavar='<OGOOO1,OG00002,...>',
    help='orthogroups need to be removed from matrix')

parser.add_argument('--single_copy_count_matrix',
    type=str,
    metavar='<single_copy_count_matrix.tsv>',
    help='output file containing single copy orthogroups')

parser.add_argument('--single_copy_seqid_matrix',
    type=str,
    metavar='<single_copy_seqid_matrix.tsv>',
    help='output file containing single copy orthogroup seqid')

parser.add_argument('--orthogroup_count_matrix',
    type=str,
    metavar='<orthogroup_count_matrix.tsv>',
    help='output file containing the gene count of each species in each orthogroup')

args = parser.parse_args()

def read_matrix_into_dataframe(arg_matrix):
    '''Parse orthogroup matrix into pandas data frame
    '''
    df = pd.read_csv("Orthogroups.tsv", sep="\t", index_col=0, dtype='str')
    return df

def drop_species(df, arg_drop_species):
    '''Species list need to be removed from matrix

    drop_species_lst: speciesA,speciesB,...
    '''
    drop_species_lst = arg_drop_species.split(',')

    df = df.drop(columns=drop_species_lst)
    return df

def drop_orthogroup(df, arg_drop_orthogroup):
    '''Orthogroups need to be removed from matrix
    '''
    drop_orthogroup_lst = arg_drop_orthogroup.split(',')

    df = df.drop(index=drop_orthogroup_lst)
    return df

def seqid_matrix_2_count_matrix(df):
    '''Count sequences of each species in each orthogroup
    '''
    row_index = list(df.index)
    count_df = pd.DataFrame()

    for species in df:
        count_df[species] = df[species].apply(lambda x: len(x.split(', ')) if isinstance(x, str) else 0)
    return count_df

def output_orthogroup_count_matrix(count_df, arg_orthogroup_count_matrix):
    '''Output orthogroup count matrix
    '''
    count_df.to_csv(arg_orthogroup_count_matrix, index_label='Orthogroup', sep='\t')
    outfile_abspath = os.path.abspath(arg_orthogroup_count_matrix)
    print(f'##Single-copy orthogroups count matrix:\n     {outfile_abspath}\n', file=sys.stdout, flush=True)

def get_singlecopy_orthogroup_matrix(count_df):
    '''Get and output single-copy orthogroup matrix
    '''
    num_species = count_df.shape[1]
    drop_orthgroup_lst = []
    single_copy_orthogroup_lst = []
    for index, row in count_df.iterrows():
        if list(row).count(1) != num_species:
            drop_orthgroup_lst.append(index)
        else:
            single_copy_orthogroup_lst.append(index)

    singlecopy_count_df = count_df.drop(index=drop_orthgroup_lst)
    return singlecopy_count_df, single_copy_orthogroup_lst

def output_single_copy_seqid_matrix(df, single_copy_orthogroup_lst, arg_single_copy_seqid_matrix):
    '''Output single copy orthogroup seqid matrix
    '''
    single_copy_seqid_df = df.loc[single_copy_orthogroup_lst, :]
    single_copy_seqid_df.to_csv(arg_single_copy_seqid_matrix, index_label='Orthogroup', sep='\t')
    outfile_abspath = os.path.abspath(arg_single_copy_seqid_matrix)
    print(f'##Single-copy orthogroups seqid matrix:\n     {outfile_abspath}\n', file=sys.stdout, flush=True)

def output_single_copy_count_matrix(singlecopy_count_df, arg_single_copy_count_matrix):
    '''Output single copy count matrix
    '''
    singlecopy_count_df.to_csv(arg_single_copy_matrix, index_label='Orthogroup', sep='\t' )
    outfile_abspath = os.path.abspath(arg_single_copy_matrix)
    print(f'##Single-copy orthogroups count matrix:\n     {outfile_abspath}\n', file=sys.stdout, flush=True)

if __name__ == '__main__':
    orthogroup_seqid_df= read_matrix_into_dataframe(args.orthogroup_matrix)

    if args.drop_species:
        orthogroup_seqid_df = drop_species(orthogroup_seqid_df, args.drop_species)
    if args.drop_orthogroup:
        orthogroup_seqid_df = drop_orthogroup(orthogroup_seqid_df, args.drop_orthogroup)

    orthogroup_count_df = seqid_matrix_2_count_matrix(orthogroup_seqid_df)
    singlecopy_count_df, single_copy_orthogroup_lst = get_singlecopy_orthogroup_matrix(orthogroup_count_df)

    if args.orthogroup_count_matrix:
        output_orthogroup_count_matrix(orthogroup_count_df, args.orthogroup_count_matrix)

    if args.single_copy_seqid_matrix:
        output_single_copy_seqid_matrix(orthogroup_seqid_df, single_copy_orthogroup_lst, args.single_copy_seqid_matrix)

    if args.single_copy_count_matrix:
        output_single_copy_count_matrix(singlecopy_count_df, args.single_copy_count_matrix)
