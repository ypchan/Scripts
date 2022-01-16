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
    
    parser.add_argument('-M', '--Mapfile',
        required=True,
        metavar='<Map_file>',
        type=str,
        help='a tab-separated map file. The 1st column lists marker names, the 2nd cloumn lists corresponding alignment files')
    args = parser.parse_args()
    return args

def build_map_dict(map_file):
    '''Parse mapfile into nested dictionary

    Args:
        map_file (str) : a tab-separated file
    
    Return：
        dict ： a nested dictionary
    '''
    map_alignment_dict = {}
    with open(map_file) as mapfh:
        for line in mapfh:
            taxa, marker, accession = line.rstrip('\n').split('\t')
            map_alignment_dict[taxa] = {}
            map_alignment_dict[taxa][marker] = ''
            if accession == 'NA':
                map_alignment_dict[taxa][marker] = 0
            else:
                map_alignment_dict[taxa][marker] = accession
    return map_alignment_dict

def get_marker_alignment_dict(marker2alignment):
    '''Parse alignment files to dictionary

    Args:
        marker2alignment (str) : mapfilename, a tab-separated map file. The 1st column lists marker names, the 2nd cloumn lists corresponding alignment files
    
    Return:
        dict : a nested dictionary
    '''
    marker_alignment_dict = {}
    with open(marker2alignment) as map2fh:
        for line in map2fh:
            marker, alignmentfile = line.rstrip('\n').split('\t')
            marker_alignment_dict[marker] = {}
            with open(alignmentfile) as alignment_fh:
                for line in alignment_fh:
                    line = line.rstrip('\n')
                    if line.startswith('>'):
                        accession = line.lstrip('>')
                        marker_alignment_dict[marker][accession] = []
                    else:
                        marker_alignment_dict[marker][accession].append(line)
            
            marker_alignment_dict[marker] = {k:''.join(v) for k,v in marker_alignment_dict[marker].items()}
    return marker_alignment_dict

def load_map_alignment_dict(map_alignment_dict, marker_alignment_dict):
    '''Load aligned seq into map_alignment_dict
    '''
    updated_map_alignment_dict = {}
    for taxa, taxa_dict in map_alignment_dict.items():
        updated_map_alignment_dict[taxa] = {}
        for marker,accession in taxa_dict.items():
            if not accession:
                updated_map_alignment_dict[taxa][marker] = 0
            else:
                seq = marker_alignment_dict[marker][accession]
                updated_map_alignment_dict[taxa][marker] = seq
    return updated_map_alignment_dict

def add_blank_seq_2alignment_dict(updated_map_alignment_dict):
    marker_aligned_length_dict = {}

    for taxa, marker_dict in updated_map_alignment_dict.items():
        for marker, seq in marker_dict.items():
            if seq != 0 and marker not in marker_aligned_length_dict:
                marker_aligned_length_dict[maker] = len(seq)

    add_blank_map_alignment_dict = {}
    for taxa, marker_dict in updated_map_alignment_dict.items():
        add_blank_map_alignment_dict[taxa] = {}
        for marker, seq in marker_dict.items():
            if seq == 0:
                blank_seq = '-' * marker_aligned_length_dict[marker]
                add_blank_map_alignment_dict[taxa][marker] = blank_seq
            else:
                add_blank_map_alignment_dict[taxa][marker] = seq
    return add_blank_map_alignment_dict

def out_concatenated_seq(add_blank_map_alignment_dict):
    '''Output concatenated alignment sequences in FASTA format
    '''
    taxa_lst = add_blank_map_alignment_dict.keys()
    for taxa, taxa_dict in add_blank_map_alignment_dict.items():
        marker_lst = taxa_dict.keys()
        break
    
    for taxa in taxa_lst:
        seq_lst = []
        print(f'>{taxa}', file=sys.stdout, flush=True)
        for marker in marker_lst:
            seq = add_blank_map_alignment_dict[taxa].get(marker)
            seq_lst.append(seq)
        contatenated_seq = ''.join(seq_lst)
        print(contatenated_seq, file=sys.stdout, flush=True)

if __name__ == '__main__':
    args = parse_args()
    map_alignment_dict = build_map_dict(args.mapfile)
    marker_alignment_dict = get_marker_alignment_dict(args.Mapfile)
    updated_map_alignment_dict = load_map_alignment_dict(map_alignment_dict, marker_alignment_dict)
    add_blank_map_alignment_dict = add_blank_seq_2alignment_dict(updated_map_alignment_dict)
    out_concatenated_seq(add_blank_map_alignment_dict)