#!/usr/bin/env python3
'''
join_BUSCO_gene_alignment.py -- combine multiple alignment files with identifical sequence id (phylogenomic analysis).

Date: 2021-05-15
Bugs: Any bugs should be reported to 764022822@qq.com
Note:
    if evolution model was supplied, msa files sharing identical models will be joined firstly.
'''

import os
import sys
import argparse

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('--alignment2model',
                    required=True,
                    type=str,
                    help='Tab-delimited list including multiple sequence alignmnt file(s) and corresponding DNA or protein evolution models mapping table: msafile    model')

parser.add_argument('--output',
                    required=True,
                    type=str,
                    metavar='Concatenated.fna',
                    help='concatenated FASTAfilename')

parser.add_argument('--partition_scheme',
                    type=str,
                    metavar='partition_scheme.txt',
                    default='partition_scheme.txt',
                    help='partition scheme')

args = parser.parse_args()

def parse_modelmap_2dict(arg_alignment2model_file):
    '''Parse msa files and corresponding evolution models into python3 dictionary

    arg_alignment2model_file: tab-delimited text file
        msafile1    GTR+I+G
        msafile2    K3Pu+F+I+G4
        ...
    '''
    model2alignment_dict = {}
    alignmentfile_lst = []
    with open(arg_alignment2model_file) as fh:
        for line in fh:
            if line.startswith('#'):
                continue

            msafile, model = line.rstrip('\n').split('\t')
            alignmentfile_lst.append(msafile)

            if model not in model2alignment_dict:
                model2alignment_dict[model] = [msafile]
            else:
                model2alignment_dict[model].append(msafile)
    for model in model2alignment_dict:
        model2alignment_dict[model].sort()
    return model2alignment_dict, alignmentfile_lst

def parse_all_alignment_2_dict(alignmentfile_lst):
    '''Parse alignment file into python3 dictonary

    alignment_file: multiple FASTA format file
    '''
    # get the length of the longest file name to format log
    max_length_of_str = max([len(alignmentfile) for alignmentfile in alignmentfile_lst])
    all_alignment_dict = {}
    number_total_msa_file = len(alignmentfile_lst)
    count = 0
    for alignmentfile in alignmentfile_lst:
        count += 1

        alignment_dict = {}
        with open(alignmentfile) as fh:
            for line in fh:
                line = line.rstrip('\n')

                if line.startswith('>'):
                    seq_id = line.lstrip('>').split('__')[1]
                    alignment_dict[seq_id] = []
                else:
                    alignment_dict[seq_id].append(line)
        alignment_dict = {k:''.join(v) for k,v in alignment_dict.items()}

        msa_length = 0
        for k,v in alignment_dict.items():
            msa_length = len(v)
            break
        print(f'Parsing {alignmentfile:{max_length_of_str}} length:{msa_length:0>5} into dictionary........[{count:04}/{number_total_msa_file}]', file = sys.stdout, flush = True)

        if alignmentfile not in all_alignment_dict:
            all_alignment_dict[alignmentfile] = {}
            all_alignment_dict[alignmentfile]['alignment'] = alignment_dict
            all_alignment_dict[alignmentfile]['length'] = msa_length

    return all_alignment_dict

def check_missing_and_add_placeholders(all_alignment_dict):
    '''Check whether some taxa are absent in certain alignment file
    '''
    # check how many taxa the aligment files includes
    all_taxa_id_lst = []
    for msafile in all_alignment_dict:
        all_taxa_id_lst.extend(list(all_alignment_dict[msafile]['alignment'].keys()))

    all_taxa_id_set = set(all_taxa_id_lst)
    number_total_taxa = len(all_taxa_id_set)
    print('Number of taxa: {number_total_taxa}', file = sys.stdout, flush=True)

    # checking missing taxa in msa file
    for msafile in all_alignment_dict:
        taxa_id_set = set(all_alignment_dict[msafile]['alignment'].keys())

        if taxa_id_set != all_taxa_id_set:

            print(f'{msafile} ： some taxa are missing', file=sys.stdout, flush=True)

            missing_taxa_lst = list(all_taxa_id_set - taxa_id_set)
            aln_length = all_alignment_dict[msafile]['length']

            for taxa in missing_taxa_lst:
                all_alignment_dict[msafile]['alignment'][taxa] = '?' * aln_length
                print(f"    {taxa}\t{aln_length}", file = sys.stdout, flush = True)

    return all_alignment_dict, all_taxa_id_set

def get_partition_scheme(model2alignment_dict, all_alignment_dict, arg_partition_scheme_filename):
    '''Output patition file for iqtree

    Input:
        model2alignment_dict: dictionary with models and corresponding msa file paths list
        all_msa_length_dict : dictionary with the path of msa files and corresponding alignemnt lengths

    Out:
        modle, part1 = 1-100
        modle, part2 = 101-384
        ...
    '''
    start = 1
    end = 0

    model_part_dict = {}
    model2alignment_dict = dict(sorted(model2alignment_dict.items(), key = lambda items: (len(items[1]), items[0]), reverse = True))
    print(model2alignment_dict)
    for model, msafile_lst in model2alignment_dict.items():
        model_part_dict[model] = []

        for msafile in msafile_lst:
            msa_length = all_alignment_dict[msafile]['length']
            start = end + 1
            end = end + msa_length
            model_part_dict[model].append(f'{start}-{end}')
    with open(arg_partition_scheme_filename, 'wt') as ofh:
        count_part = 0
        number_partitions = len(model_part_dict)
        for model, start_end_lst in model_part_dict.items():
            count_part += 1
            print(f'{model}, part_{count_part} = {", ".join(start_end_lst)}', file = ofh, flush=True)

    schemefile_abspath = os.path.abspath(arg_partition_scheme_filename)
    print(f'## Partition file: {schemefile_abspath}', file=sys.stdout, flush=True)
    return model2alignment_dict

def join_marker(model2alignment_dict, all_alignment_dict, all_taxa_id_set, arg_output_filename):
    '''
    '''
    msa_list_ordered = []
    for model, msa_lst in model2alignment_dict.items():
        msa_list_ordered.extend(msa_lst)

    joined_dict = {}
    print(f'Start joining all alignment file', file = sys.stdout, flush=True)

    number_taxa = len(all_taxa_id_set)
    count_taxa = 0
    max_len_taxa_str = max([len(taxa) for taxa in all_taxa_id_set])

    for taxa in list(all_taxa_id_set):
        count_taxa += 1
        joined_dict[taxa] = []
        print(f'    joining {taxa:.<{max_len_taxa_str}}........[{count_taxa}/{number_taxa}]', file = sys.stdout, flush=True)
        for msafile in msa_list_ordered:
            joined_dict[taxa].append(all_alignment_dict[msafile]['alignment'][taxa])

    joined_dict = {k:''.join(v) for k,v in joined_dict.items()}
    # output joined sequences
    with open(arg_output_filename, 'wt') as ofh:
        for k,seq in joined_dict.items():
            ofh.write(f">{k}\n{seq}\n")

if __name__ == '__main__':
    model2alignment_dict, alignmentfile_lst = parse_modelmap_2dict(args.alignment2model)
    all_alignment_dict = parse_all_alignment_2_dict(alignmentfile_lst)
    all_alignment_dict, all_taxa_id_set = check_missing_and_add_placeholders(all_alignment_dict)
    model2alignment_dict = get_partition_scheme(model2alignment_dict, all_alignment_dict, args.partition_scheme)
    join_marker(model2alignment_dict, all_alignment_dict, all_taxa_id_set, args.output)
    print('Done!', file = sys.stdout, flush=True)
    sys.exit(0)