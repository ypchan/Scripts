#!/usr/bin/env python3
'''
single_copy_busco_datasets.py -- select BUSCO genes based on their taxa coverage.

date:  2021-09-21
bugs： Any bugs should be reported to yanpengch@qq.com

label_busco_full_table:
GCA_902806535.1    ./GCA_902806535.1_HR_busco/run_ascomycota_odb10/full_table.tsv
GCA_002246955.1    ./GCA_002246955.1_ASM224695v1_busco/run_ascomycota_odb10/full_table.tsv

--busco_desc:
262829at4890    Proteasome subunit alpha type                           https://www.orthodb.org/v10?query=262829at4890
331536at4890    Mediator of RNA polymerase II transcription subunit 6   https://www.orthodb.org/v10?query=331536at4890
'''
import os
import argparse
import textwrap
import pandas as pd
import numpy as np
import fileinput
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('label_busco_full_table',
                    metavar='<label_full_table_path.txt>',
                    type=str,
                    help='label and path list of BUSCO assessment result files: full_table.tsv')

parser.add_argument('-d', '--details_busco',
                    metavar='<BUSCO_gene_description.txt>',
                    type=str,
                    required=True,
                    help='table of BUSCO gene description including BUSCO ID, Ortho DB url and function')

parser.add_argument('-m', '--matrix',
                    metavar='<out_matrix.tsv>',
                    type=str,
                    default='busco_full_matrix.tsv',
                    help='specify the output filename. Default: busco_full_matrix.tsv')

parser.add_argument('-c', '--coverage_taxa',
                    metavar='<int>',
                    type=int,
                    choices=range(1, 101),
                    default=80,
                    help='taxa coverage = (No. of Taxa having this BUSCO gene / No. all Taxa) * 100. Default: 80')

parser.add_argument('-o', '--out_dir',
                    metavar='<out_directory>',
                    type=str,
                    required=False,
                    default='single_copy_BUSCO_dataset',
                    help='output directory name')

parser.add_argument('-t', '--threads',
                    metavar='<int>',
                    type=int,
                    default=4,
                    help='number of threads to use for concurrent processing. Default: 4')

args = parser.parse_args()

def read_busco_results(file):
    '''read all busco results into python dictionary'''
    label_busco_result_dict = {}
    for line in fileinput.input(file):
        label, full_table_path = line.strip().split()
        label_busco_result_dict[label] = full_table_path
    return label_busco_result_dict

def read_busco_description(file):
    '''read busco gene description into python dictionary'''
    busco_desc_dict = {}
    with open(file, 'r') as f:
        for line in f:
            line_lst = line.rstrip().split('\t')
            busco_id = line_lst[0]
            url = line_lst[2]
            desc = line_lst[1]
            busco_desc_dict[busco_id] = [url, desc]
    return busco_desc_dict

def read_full_table(full_table_path):
    '''read single full table file'''
    buscoid_status = {}
    with open(full_table_path, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            line_lst = line.rstrip().split('\t')
            busco_id = line_lst[0]
            status = line_lst[1]
            buscoid_status[busco_id] = status
    return buscoid_status

def construct_matrix(busco_desc_dict, label_busco_result_dict):
    '''construct busco gene matrix'''
    taxa_label_lst = list(label_busco_result_dict.keys())
    col_name_lst = ['OrthoDB_URL', 'Desc', 'No_taxa', 'Coverage%'] + taxa_label_lst

    row_name_lst = list(busco_desc_dict.keys())
    df = pd.DataFrame(index=row_name_lst, columns=col_name_lst)

    df['OrthoDB_URL'] = [busco_desc_dict[k][0] for k in row_name_lst]
    df['Desc'] = [busco_desc_dict[k][1] for k in row_name_lst]

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(read_full_table, path): label for label, path in label_busco_result_dict.items()}
        for future in tqdm(as_completed(futures), total=len(futures), desc='Reading full tables'):
            label = futures[future]
            buscoid_status = future.result()
            df[label] = df.index.to_series().map(buscoid_status)
    
    return df

def filter_matrix(df, taxa_coverage, out_matrix):
    '''filter matrix by taxa coverage'''
    num_taxa = df.shape[1] - 4
    df['No_taxa'] = np.sum(df.iloc[:, 4:].values == 'Complete', axis=1)
    df['Coverage%'] = np.round(df['No_taxa'] / num_taxa * 100, 2)

    df_filtered = df[df['Coverage%'] >= taxa_coverage]
    num_busco_filtered = df.shape[0] - df_filtered.shape[0]
    print(f'[INFO] Number of BUSCO genes with low taxa coverage: {num_busco_filtered}', flush=True)

    df.to_csv(out_matrix, sep='\t')
    return df_filtered

def read_fasta(fasta_file):
    '''read fasta file into a single sequence string'''
    with open(fasta_file, 'r') as f:
        seq = ''.join(line.strip() for line in f if not line.startswith('>'))
    return seq

def construct_busco_gene_dataset(label_busco_result_dict, df_filtered):
    '''construct busco gene dataset'''
    single_copy_busco_dict = {}
    busco_id_lst = df_filtered.index.tolist()

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {}
        for label, full_table_path in label_busco_result_dict.items():
            single_copy_sequence_path = os.path.join(os.path.dirname(full_table_path), 'busco_sequences', 'single_copy_busco_sequences')
            for busco_id in busco_id_lst:
                if df_filtered.loc[busco_id, label] == 'Complete':
                    fasta_file = os.path.join(single_copy_sequence_path, f'{busco_id}.faa')
                    futures[executor.submit(read_fasta, fasta_file)] = (busco_id, label)
        
        for future in tqdm(as_completed(futures), total=len(futures), desc='Reading sequences'):
            busco_id, label = futures[future]
            busco_sequence = future.result().upper()
            if busco_id not in single_copy_busco_dict:
                single_copy_busco_dict[busco_id] = {}
            single_copy_busco_dict[busco_id][label] = busco_sequence
    
    return single_copy_busco_dict

def out_busco_single_copy_dataset(single_copy_busco_dict, out_dir):
    '''output single-copy BUSCO protein datasets'''
    os.makedirs(out_dir, exist_ok=True)
    
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = []
        for busco_id, taxa_seq_dict in single_copy_busco_dict.items():
            futures.append(executor.submit(write_fasta, busco_id, taxa_seq_dict, out_dir))
        
        for future in tqdm(as_completed(futures), total=len(futures), desc='Writing sequences'):
            future.result()

def write_fasta(busco_id, taxa_seq_dict, out_dir):
    '''write fasta file'''
    with open(os.path.join(out_dir, f'{busco_id}.faa'), 'w') as f:
        for taxa, seq in taxa_seq_dict.items():
            wrapped_seq = textwrap.fill(seq, width=80)
            f.write(f'>{taxa}\n{wrapped_seq}\n')

if __name__ == '__main__':
    label_busco_result_dict = read_busco_results(args.label_busco_full_table)
    busco_desc_dict = read_busco_description(args.details_busco)
    df = construct_matrix(busco_desc_dict, label_busco_result_dict)
    df_filtered = filter_matrix(df, args.coverage_taxa, args.matrix)
    single_copy_busco_dict = construct_busco_gene_dataset(label_busco_result_dict, df_filtered)
    out_busco_single_copy_dataset(single_copy_busco_dict, args.out_dir)
    print('Done.')
