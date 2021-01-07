#!/usr/bin/env python3
'''
fasta_id_mapper.py -- change fasta ids according to given mapping file

DATE:
    2021-01-07
BUGS：
    Any bugs should be sent to chenyanpeng1992@outlook.com
'''

import sys
import gzip
import argparse

def parse_args():
    '''Parse command-line arguments.
    '''
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('input',
        metavar='<in-fasta>',
        type=str,
        help='input fasta filename')

    parser.add_argument('output',
        type=str,
        metavar='<out-fasta>',
        help='output fasta filename (suffix .gz for gzipped out)')
    
    parser.add_argument('mapfile',
        type=str,
        metavar='<mapfile>',
        help='two-column mapfile, 1st column lists old ids, 2ed column lists new ids')

    args = parser.parse_args()
    return args

def fasta_2dict(infile):
    '''
    Parse fasta into python dictionary

    Parameter
    ---------
    infile : str
        input file in FASTA format

    Return
    ------
    fa_dict : dict
        python dictionary, keys represent protein names and values represent sequence lst
    '''
    fa_fh = gzip.open(infile, 'rt') if infile.endswith('.gz') else open(infile, 'rt')

    fa_dict = {}
    for line in fa_fh:
        if line.startswith('>'):
            protein_id = line
            fa_dict[protein_id] = []
        else:
            fa_dict[protein_id].append(line)
    fa_fh.close()
    return fa_dict

def mapping_dict(mapfile):
    '''
    Parse mapfile into python3 dictionary

    Parameter
    ---------
    mapfile : str
        input file, a tab-delimited file. 1st column lists old ids, 2ed column lists new ids
    
    Return
    ------
    map_dict : dict
        a python dictionary, keys represent old ids, and values represent new ids
    '''
    map_dict = {}
    with open(mapfile, 'rt') as map_fh:
        for line in map_fh:
            [old_id, new_id] = line.rstrip('\n').split('\t')
            map_dict[old_id] = new_id
    
    return map_dict

def change_id(fa_dict, map_dict):
    '''
    Removed protein if the it's length short than given length

    Parameter
    ---------
    fa_dict : dict
        python dictionary, keys represent protein names and values represent sequence list
    map_dict : dict
        a python dictionary, keys represent old ids, and values represent new ids

    Return
    ------
    id_changed_fa_dict : dict
        fasta ids are changed in id_changed_fa_dict
    '''
    id_changed_fa_dict = {}
    for old_id, seq_lst in fa_dict.items():
        old_id = old_id.lstrip('>').rstrip('\n')
        new_id = '>' + map_dict[old_id] + '\n'
        id_changed_fa_dict[new_id] = seq_lst
    return id_changed_fa_dict

def out_fasta(id_changed_fa_dict, outfile):
    '''
    Out ids cahgned protein sequences in FASTA format

    Parameters
    ----------
    id_changed_fa_dict : dict
        fasta ids are changed in id_changed_fa_dict
    outfile : str
        outfilename (suffix .gz for gzipped out)
    '''
    ofh = gzip.open(outfile, 'w') if outfile.endswith('.gz') else open(outfile, 'w')
    for protein_id, seq_lst in id_changed_fa_dict.items():
        ofh.write(protein_id)
        for line in seq_lst:
            ofh.write(line)
    ofh.close()

if __name__ == '__main__':
    args = parse_args()
    fa_dict = fasta_2dict(args.input)
    map_dict = mapping_dict(args.mapfile)
    id_changed_fa_dict = change_id(fa_dict, map_dict)
    out_fasta(id_changed_fa_dict, args.output)