#!/use/bin/env python3
'''
combine_sequence_alignment.py -- combine multiple alignment file with identifical sequence id (phylogenomic analysis).

Date: 2021-05-15
Bugs: Any bugs should be reported to yanpengch@qq.com
'''
import os
import sys
import argparse

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('modelmap',
    type=str,
    help='multiple sequence alignmnt file(s) and corresponding DNA or protein evolution model mapping table: msafile    model')

parser.add_argument('out',
    type=str,
    metavar='out_combined.fa',
    help='output filename')
args = parser.parse_args()

def parse_modelmap_2dict(modelmap):
    '''Parse msa files and corresponding evolution models into python3 dictionary return dict

    modelmap: tab-delimited text file
        msafile1    GTR+I+G
        msafile2    K3Pu+F+I+G4
        ...
    '''
    model_map_dict = {}
    with open(modelmap) as modelfh:
        for line in modelfh:
            if line.startswith('#'):
                continue
            msafilename, model = line.rstrip('\n').split('\t')
            if model not in model_map_dict:
                model_map_dict[model] = [msafilename]
            else:
                model_map_dict[model].append(msafilename)
    for model in model_map_dict:
        model_map_dict[model].sort()
    return model_map_dict

def read_alignment_file2dict(alignmnet_file):
    '''Parse alignment file into python3 dictonary return fasta dictionary

    alignment_file: multiple fasta format file with simple identifier
    '''
    aln_dict = {}
    with open(aln_file) as aln_fh:
        for line in aln_fh:
            line = line.rstrip('\n')
            if line.startswith('>'):
                seq_id = line.lstrip('>')
                aln_dict[seq_id] = []
            else:
                aln_dict[seq_id].append(line)
    aln_dict = {k:''.join(v) for k,v in aln_dict.items()}
    return aln_dict

def get_msa_length(aln_dict):
    '''Get multiple sequence alignemnt length 

    aln_dict: msa in fasta format stored in dictionary
    '''
    msa_length = 0
    for k,v in aln_dict.items():
        while msa_length == 0:
            msa_length = len(v) 
    return msa_length

def check_missing_and_add_placeholders(id_lst, aln_dict):
    '''Check whether some taxa are absent in certain alignment file
    '''
    aln_dict_seqid_set = set(aln_dict.keys())
    complete_id_set = set(id_lst)

    if aln_dict_seqid_set != complete_id_set:
        print(f'{aln_file} ： some taxa sequence data are missing', file=sys.stdout, flush=True)
        need_add_taxa_lst = list(complete_id_set - aln_dict_seqid_set)
        aln_length = len(aln_dict[list(complete_id_set & aln_dict_seqid_set)[0]])
        for taxa in need_add_taxa_lst:
            aln_dict[taxa] = '-' * aln_length
    return aln_dict

def get_partition_scheme(model_map_dict, all_msa_length_dict):
    '''Output patition file for iqtree
    
    Input:
        mdel_map_dict:       dictionary with models and corresponding msa file paths list
        all_msa_length_dict: dictionary with the path of msa files and corresponding alignemnt lengths
    
    Out:
        DNA, part1 = 1-100
        DNA, part2 = 101-384
        ...
    '''
    schemefh = open("partition.txt", 'wt')
    counter_part = 0
    start = 1
    end = 0
    for model, msafile_lst in model_map_dict.items():
        counter_part += 1
        msa_length_lst = [all_msa_length_dict[msafile] for msafile in msafile_lst]
        end += sum(msa_length_lst)
        part_str = f'DNA, part{counter_part} = {start}-{end}'
        schemefh.write(part_str + '\n')
        start = end + 1
    schemefh.close()
    schemefile_abspath = os.path.abspath("partition.txt")
    print(f'## Partition file: {schemefile_abspath}', file=sys.stdout, flush=True)

if __name__ == '__main__':
    # input msa files set
    model_map_dict = parse_modelmap_2dict(args.modelmap)
    msa_files_lst = []
    for model, msa_lst in model_map_dict.items():
        msa_files_lst.extend(msa_lst)

    taxa_list = []
    all_msa_dict = {}
    for aln_file in msa_files_lst:
        aln_dict = read_alignment_file2dict(aln_file)
        if aln_file not in all_msa_dict:
            all_msa_dict[aln_file] = aln_dict
        else:
            sys.exit(f'Error message: duplicate msa file {aln_file}')
        taxa_list.extend(list(aln_dict.keys()))
    
    taxa_lst = list(set(taxa_list))
    
    # all msa length dictionary
    all_msa_length_dict = {}
    for msa_name, msa_dict in all_msa_dict.items():
        all_msa_length_dict[msa_name] = get_msa_length(msa_dict)
    
    model_map_dict = parse_modelmap_2dict(args.modelmap)
    # output partition scheme for iqtree analysis
    get_partition_scheme(model_map_dict, all_msa_length_dict)

    combine_dict = {}
    for _, msa_file_path_lst in model_map_dict.items():
        for msa_file_path in msa_file_path_lst:
            aln_dict = all_msa_dict[msa_file_path]
            aln_dict = check_missing_and_add_placeholders(taxa_lst, aln_dict)
            for k,v in aln_dict.items():
                if k not in combine_dict:
                    combine_dict[k] = [v]
                else:
                    combine_dict[k].append(v)

    combine_dict = {k:''.join(v) for k,v in combine_dict.items()}

    with open(args.out, 'wt') as outfh:
        for k,v in combine_dict.items():
            outfh.write(f'>{k}\n{v}\n')