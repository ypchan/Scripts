#!/usr/bin/env python3
'''
phylogenomics_concatenate_alignment_by_evolution_models.py -- concatenate hundreds of alignment files by corresponding evolution models

DATE: 2020-02-08
BUGS: Any bugs should be reported to chenyanpeng1992@outlook.com
'''
import os
import sys
import collections
import argparse

parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('-i', '--input',
    required=True,
    type=str,
    help='path of alignment files and the corresponding models')

parser.add_argument('-p', '--prefix',
    required=True,
    type=str,
    help='prefix outfile, PREFIX.concatenate.faa | PREFIX.concatenate.partition_scheme.txt')

args = parser.parse_args()

def read_alignment2models(args_input):
    '''
    Parameters
    ---------------
    args_input: tab-delimited file, the 1st column is the path of the alignment files, and the 2rd column is the coresponding evolution models

    Return
    ---------------
    dictionary1: a python dictionary, the 1st level keys are alignment file, the 2rd level keys are fasta ids, and the sequences are the values.
    dictionary2: a python dictionary, keys represent alignment filenames, values represent alignment length.
    dictionary3: a python dictionary, keys represent evolution models, value are list comprising alignment files.
    txt: Raxml-style partition scheme
    '''
    all_msa_dict = {}
    model2alignment_lst_dict = collections.defaultdict(list)
    taxa_lst = []
    with open(args_input, 'rt') as infh:
        for line in infh:
            alignment_file, model = line.rstrip('\n').split('\t')
            model2alignment_lst_dict[model].append(alignment_file)

            if alignment_file not in all_msa_dict:
                all_msa_dict[alignment_file] = {}
                with open(alignment_file, 'rt') as fafh:
                    for line in fafh:
                        line = line.rstrip('\n')
                        if line.startswith('>'):
                            fa_id = line.split()[0].lstrip('>')
                            taxa_lst.append(fa_id)
                            all_msa_dict[alignment_file][fa_id] = []
                        else:
                            all_msa_dict[alignment_file][fa_id].append(line)

    for msa, fa_dict in all_msa_dict.items():
        all_msa_dict[msa] = {k:''.join(v) for k,v in fa_dict.items()}
    
    model2alignment_lst_dict = {key: val for key, val in sorted(model2alignment_lst_dict.items(), key = lambda ele: ele[0])}
    ordered_msa_lst = []
    for model, alignment_lst in model2alignment_lst_dict.items():
        ordered_msa_lst.extend(alignment_lst)
    
    msa_len_dict = {}
    with open(args.prefix + 'concatenate.partition_scheme.txt', 'wt') as txtfh:
        join_length = 0
        for model, alignment_lst in model2alignment_lst_dict.items():
            for alignment in alignment_lst:
                part_label = os.path.basename(alignment).split('.')[0]
                alignment_length = len(list(all_msa_dict[alignment].items())[0][1])
                msa_len_dict[alignment] = alignment_length
                if join_length == 0:
                    start = 1
                else:
                    start = join_length + 1
                join_length += alignment_length
                end = join_length
                txtfh.write(f'{model}, {part_label} = {start} - {end}\n')
    return all_msa_dict, msa_len_dict, ordered_msa_lst, list(set(taxa_lst))

def add_missingdata_to_alignment(taxa_lst, all_msa_dict, msa_len_dict):
    '''Adding missing data into some msa file.
    '''
    for msa, fadict in all_msa_dict.items():
        msa_length = msa_len_dict[msa]
        taxa_missing_lst = []
        for taxa_id in taxa_lst:
            if taxa_id not in fadict:
                taxa_missing_lst.append(taxa_id)
                all_msa_dict[msa][taxa_id] = '?' * msa_length

        print('#' + msa, msa_length, len(taxa_missing_lst), file=sys.stdout, flush=True)
        print("\n".join(taxa_missing_lst) + '\n', file=sys.stdout, flush=True)
    return all_msa_dict

def concatenate(taxa_lst, all_msa_dict, ordered_msa_lst):
    '''Combing msa file by common ids
    '''
    concatenate_dict = {}
    for taxa_id in taxa_lst:
        concatenate_dict[taxa_id] = []
        for msa in ordered_msa_lst:
            seq = all_msa_dict[msa][taxa_id]
            concatenate_dict[taxa_id].append(seq)
    return concatenate_dict

if __name__ == '__main__':
    all_msa_dict, msa_len_dict, ordered_msa_lst, taxa_lst = read_alignment2models(args.input)
    all_msa_dict = add_missingdata_to_alignment(taxa_lst, all_msa_dict, msa_len_dict)
    concatenate_dict = concatenate(taxa_lst, all_msa_dict, ordered_msa_lst)
    with open(args.prefix + '.partition_concatenate.faa' , 'wt') as outfh:
        for taxa_id, seq in concatenate_dict.items():
            outfh.write(f'>{taxa_id}\n{"".join(seq)}\n')