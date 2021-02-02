#!/usr/bin/env python3
'''
concatenate_marker_alignment -- concatenate multiple markers for building a phylogenetic tree according a mapping file

DATE:
    2021-01-27
BUGS：
    Any bugs should be sent to chenyanpeng1992@outlook.com
NOTES:
    If the marker is missed in some taxa(species), '-' will occur as placeholders
'''

import sys
import gzip
import argparse

def parse_args():
    '''Parse command-line arguments

    Return
        args (object) : args.<args>
    '''
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-m', '--mapfile',
        required=True,
        metavar='<map_file>',
        type=str,
        help='a tab-separated map file. The first row tags: speceis_id gene1-accession gene2-accession')
    
    parser.add_argument('-a', '--alignment_files',
        required=True,
        metavar='<alignment.fa>',
        type=str,
        nargs='+',
        help='multiple alignment files, the IDs must be consistent with IDs in mapfile')
    
    parser.add_argument('-t', '--alignment_type',
        default='fasta',
        type=str,
        choices=['fasta', 'clustal', 'phylip-sequential', 'phylip-interleaved', 'nexus'],
        help='multiple alignment files, the IDs must be consistent with IDs in mapfile')

    args = parser.parse_args()
    return args

def parse_alignment_2dict(alignment_tup, alignment_type):
    '''Parse multiple alignment files into dictionary

    Args:
        alignment_tup (tuple) : multiple alignment files
        alignment_file (str)  :
    
    Return:
        dictionary : 
    '''
    alignment_dict = {}
    for alignment_file in alignment_tup:
        if alignment_type == 'fasta':
            with open(alignment_file) as filefh:
                for line in filefh:
                    line = line.rstrip('\n')
                    if line.startswith('>'):
                        fa_id = line.lstrip('>')
                        alignment_dict[fa_id] = []
                    else:
                        alignment_dict[fa_id].append(line)

def join_mapfile_alginmentfile(map_file, alignment_dict):
    '''Parse mapfile into nested dictionary

    dict = {gene1:{taxon1:seq, taxon2:seq,...},...}
    Args:
        map_file (str) : a tab-separated file
    
    Return：
        dict ： a nested dictionary
    '''
    mapped_alignment_dict = {}
    mapfile_fh = open(map_file, 'rt')
    line_lst = mapfile_fh.readlines()
    mapfile_fh.close()

    line_lst = [line.rstrip('\n') for line in line_lst]
    marker_lst = line_lst[0].split('\t')[1:]
    taxa_lst = [line.split('\t')[0] for line in line_lst[1:]]
    accession_lst = [line.split('\t')[1:] for line in line_lst[1:]]

    for col, marker in enumerate(marker_lst):
        mapped_alignment_dict[marker] = {}
        for row, taxon in enumerate(taxa_lst):
            accession = accession_lst[row][col]
            aligned_seq = alignment_dict.get(accession, '0')
            mapped_alignment_dict[marker][taxon] = aligned_seq

    formatted_mapped_alignment_dict = {}
    for marker, taxa_dict in mapped_alignment_dict.items():
        formatted_mapped_alignment_dict[marker] = {}
        
        for taxon, aligned_seq in taxa_dict.items():
            if aligned_seq != '0':
                alignment_seq_len = len(aligned_seq)
                break
        for taxon, aligned_seq in taxa_dict.items():
            if aligned_seq == '0':
                taxa_dict[taxon] = '-' * alignment_seq_len
        
        formatted_mapped_alignment_dict[marker] = taxa_dict
    return formatted_mapped_alignment_dict

def out_concatenated_seq(formatted_mapped_alignment_dict):
    '''Output concatenated alignment sequences in FASTA format

    Args:
        formatted_mapped_alignment_dict (dict) : dict = {gene1:{taxon1:seq, taxon2:seq,...},...}

    Return:
        NULL    
    '''
    marker_lst = formatted_mapped_alignment_dict.keys()
    for marker, taxa_dict in formatted_mapped_alignment_dict.items():
        taxa_lst = taxa_dict.keys()
        break
    
    for taxon in taxa_lst:
        concatenated_seq_lst = []
        for marker in marker_lst:
            concatenated_seq_lst.append(formatted_mapped_alignment_dict[marker][taxon])
        concatenated_seq = ''.join(concatenated_seq_lst)
        print(f'>{taxon}\n{concatenated_seq}', file=sys.stdout, flush=True)

if __name__ == '__main__':
    args = parse_args()
    alignment_dict = parse_alignment_2dict(args.alignment_files, args.alignment_type)
    formatted_mapped_alignment_dict = join_mapfile_alginmentfile(args.mapfile, alignment_dict)
    out_concatenated_seq(formatted_mapped_alignment_dict)