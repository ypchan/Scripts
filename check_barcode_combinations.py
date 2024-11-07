#!/usr/bin/env python3

# bugs: yanpengch@qq.com
# date: 2024-01-15

import os
import sys
import argparse

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--msa_barcode_model', type=str, required=True, help='The name of the MSA barcode model.')
parser.add_argument('--combination_lst', type=str, required=True, help='A list of combinations to process.')
parser.add_argument('--outdir', type=str, required=True, help='Output directory.')

args = parser.parse_args()

def check_input(args_msa_barcode_models, args_combination_file):
    barcode_lst1 = []
    barcode_lst2 = []
    with open(args_msa_barcode_models) as msa_barcode_model_infh, open(args_combination_file) as combinations_infh:
        for line in msa_barcode_model_infh:
            barcode1 = line.split()[1]
            barcode_lst1.append(barcode1)
        barcode_lst1 = sorted(barcode_lst1)
        for line in combinations_infh:
            combinations = line.rstrip('\n').split()[1].split('-')
            barcode_lst2.extend(combinations)
        barcode_set2 = set(barcode_lst2)
        barcode_set1 = set(barcode_lst1)
        barcode_set2.issubset(barcode_set1)
    if not barcode_set2.issubset(barcode_set1):
        sys.exit('[Error]: some barcode does not have the corresponding barcode fasta file.')

def read_fasta(fa_file):
    fa_dict = {}
    with open(fa_file, 'rt') as infh:
        for line in infh:
            line = line.rstrip('\n')
            if line.startswith('>'):
                seq_id = line.lstrip('>')
                fa_dict[seq_id] = []
            else:
                fa_dict[seq_id].append(line)
    fa_dict = {k:''.join(v) for k,v in fa_dict.items()}
    length = len(list(fa_dict.values())[0])
    taxa_lst = sorted(list(fa_dict.keys()))
    return fa_dict, length, taxa_lst

def read_msa(args_msa_barcode_models):
    barcode_msa_dict = {}

    with open(args_msa_barcode_models) as infh:
        for line in infh:
            msa_file, barcode, model = line.rstrip('\n').split()
            barcode_msa_dict[barcode] = {}
            fa_dict, length, taxa_lst = read_fasta(msa_file)
            barcode_msa_dict[barcode]['length'] = length
            barcode_msa_dict[barcode]['model'] = model
            barcode_msa_dict[barcode]['msa_dict'] = fa_dict
            barcode_msa_dict[barcode]['taxa_lst'] = taxa_lst
    return barcode_msa_dict

def concatenate_msa(barcode_msa_dict, barcode_combination_lst):
    common_taxa_id_lst = []
    for barcode in barcode_combination_lst:
        common_taxa_id_lst.extend(barcode_msa_dict[barcode]['taxa_lst'])
    common_taxa_id_lst = list(set(common_taxa_id_lst))

    concatenated_dict = {}
    best_scheme = {}
    for barcode in barcode_combination_lst:
        length = barcode_msa_dict[barcode]['length']
        msa_dict = barcode_msa_dict[barcode]['msa_dict']
        model = barcode_msa_dict[barcode]['model']
        best_scheme[barcode] = [model,length]
        for taxa in common_taxa_id_lst:
            if taxa not in concatenated_dict:
                concatenated_dict[taxa] = []

            if taxa not in msa_dict:
                taxa_seq = '-' * length
            else:
                taxa_seq= msa_dict[taxa]
            concatenated_dict[taxa].append(taxa_seq)
    return best_scheme, concatenated_dict

def output(best_scheme, concatenated_dict, args_outdir, prefix):
    outfile = f'{args_outdir}/{prefix}.concatenation.fna'
    with open(outfile, 'wt') as outfh:
        for taxa, taxa_seq_lst in concatenated_dict.items():
            concatenated_seq = ''.join(taxa_seq_lst)
            outfh.write(f">{taxa}\n{concatenated_seq}\n")
    best_scheme_file = f"{args_outdir}/{prefix}.best_scheme.txt"
    end = 0
    with open(best_scheme_file, 'wt') as outfh:
        outfh.write(f"#nexus\n")
        outfh.write(f"begin sets;\n")
        charpartion_str = 'charpartition ModelFinder = '
        for barcode, model_length_lst in best_scheme.items():
            model, length = model_length_lst
            start = end + 1
            end = end + length
            outfh.write(f"charset {barcode} = {start}-{end};\n")
            charpartion_str += f"{model}:{barcode},"
        charpartion_str = charpartion_str.rstrip(',') + ";"
        outfh.write(f"{charpartion_str}\n")
        outfh.write(f"end;\n")

if __name__ == "__main__":
    check_input(args.msa_barcode_model, args.combination_lst)
    barcode_msa_dict = read_msa(args.msa_barcode_model)
    with open(args.combination_lst) as infh:
        for line in infh:
            prefix, barcode_combination_str = line.rstrip('\n').split('\t')
            barcode_combination_lst= barcode_combination_str.split("-")
            best_scheme, concatenated_dict = concatenate_msa(barcode_msa_dict,barcode_combination_lst)
            output(best_scheme, concatenated_dict, args.outdir, prefix)
    sys.exit(0)
