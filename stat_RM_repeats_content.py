#!/usr/bin/env python3
'''
stat_RM_repeats_content -- collect RepeatMasker result tbl statistic values
                            1: filename 2: sequences 3: total_length 
                            4: GC_level  5: Bases_masked(%)
AUTHOR:
    chegnyanpeng1992@outlook.com
DATE:
    2021-01-16
'''
import os
import sys
import argparse

def parse_args():
    '''Parse command-line arguments

    Return:
        object: args.<argument>
    '''
    parser = argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-i', '--input',
                        metavar='in.tbl',
                        type=str,
                        nargs='+',
                        help='input file generated RepeatMasker')

    parser.add_argument('-f', '--file',
                        metavar='<txt>',
                        help='the list of input files in one file per line')
    args = parser.parse_args()

    if not any([args.input, args.file]):
        sys.exit(f'Error: at least one option (--input or --file) is supplied')
    return args

def extract_statstic_values_from_tbl(tblfile):
    '''Extract statistic values from tbl file

    Args:
        tblfile (str): tbl file genereated from RepeatMasker
    Return:
        dict : a pyton3 dictionary containning statistic values
    '''
    tbl_dict = {}
    with open(tblfile, 'rt') as infh:
        for line in infh:
            if line.startswith('file name'):
                filename = line.split(':')[1].rstrip('\n').strip()
                tbl_dict['filename'] = filename
            
            if line.startswith('sequences'):
                sequences = line.split(':')[1].rstrip('\n').strip()
                tbl_dict['sequences'] = sequences
            
            if line.startswith('total length'):
                total_length = line.split(':')[1].split('bp')[0].rstrip('\n').strip()
                tbl_dict['total_length'] = total_length


            if line.startswith('GC level'):
                GC_content = line.split(':')[1].rstrip('\n').strip()
                tbl_dict['GC_content'] = GC_content

            if line.startswith('bases masked'):
                bases_masked = line.split(':')[1].rstrip('\n').strip()
                tbl_dict['bases_masked'] = bases_masked
    return tbl_dict
    
if __name__ == '__main__':
    args = parse_args()
    
    head_lst = ['filename', 'sequences', 'total length', 'GC level', 'bases masked']
    print('\t'.join(head_lst), file=sys.stdout, flush=True)
    if args.input:
        for tblfile in args.input:
            tbl_dict = extract_statstic_values_from_tbl(tblfile)
            out_lst = [tbl_dict.get(key) for key in head_lst]
            print('\t'.join(out_lst), file=sys.stdout, flush=True)
    if args.file:
        file_lst = open(args.file).readlines()
        file_lst = [tblfile.rstrip('\n') for tblfile in file_lst]
        for tblfile in file_lst:
            tbl_dict = extract_statstic_values_from_tbl(tblfile)
            out_lst = [tbl_dict.get(key) for key in head_lst]
            print('\t'.join(out_lst), file=sys.stdout, flush=True)