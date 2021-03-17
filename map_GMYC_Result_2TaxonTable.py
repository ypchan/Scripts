#!/usr/bin/env python3
'''
map_GMYC_Result_2TaxonTable.py -- map GMYC reasult to the Taxon Accession Table.

DATE: 2021-03-11
BUGS: Any bugs should be send to chenyanpeng1992@outlook.com
INFO: Taxon table: taxon_id accession
'''

import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('taxontable',
        metavar='<taxontable.tsv>',
        type=str,
        help='taxontable.tsv is composed of taxonIDs and corresponding accession. If the accession missed, must use NA as placeholder')

    parser.add_argument('GMYC_result',
        metavar='<result.*.txt>',
        type=str,
        help='GMYC result that should be [*.PTPhSupportPartition.txt | *.PTPMLPartition.txt]')

    parser.add_argument('--field',
        metavar='<int>',
        type=int,
        default=2,
        help='specify the column if accession (default to 2)')

    parser.add_argument('--method',
        metavar='<single|multiple>',
        type=str,
                choices=['single', 'multiple'],
        default='signle',
        help='method of analysis, either "single" for single-threshold version or "multiple" for multiple-threshold version')

    parser.add_argument('--overwrite',
        action='store_true',
        help='add GMYC result to original input Taxon table')

    parser.add_argument('--file_head',
        action='store_true',
        help='if the Taxon Table has head line, this option must be selected')

    parser.add_argument('--strip_minor_version',
        action='store_true',
        help='strip accession minor version info. For example: AB704204.1 -> AB704204')

    args = parser.parse_args()
    return args

def parse_GMYC_result_2dict(GMYC_resultfile, strip):
    '''Parse GMYC result into python dict, keys represent accession, values represent groupID

    Args:
        GMYC_resultfile (str) : GMYC result file name

    Return：
        dict ：keys represent accession, values represent groupID
    '''
    GMYC_dict = {}
    with open(GMYC_resultfile) as gmycfh:
        for line in gmycfh:
            if line.startswith('sample_name'):
                continue
            accession, species_id = line.rstrip('\n').split()
            if strip:
                accession = accession.split('.')[0]
            if accession in GMYC_dict:
                sys.exit(f'Error message:\n    duplicated accession {accession}')
                GMYC_dict[accession] = species_id
    return GMYC_dict

def out_result_file(taxontable, filehead, accession_field, GMYC_dict, overwrite, args_method):
    '''Output result file with GMYC result at the last column

    Args:
        taxontable (str) : mapping file is composed of taxon,otherinfo..., marker1_accession, marker2_accession...
                         If the accession missed, must use NA as placeholder
        accession_field (int) : specify the column of accession
        GMYC_dict (dict) : keys represent accession, values represent groupID
    '''
    with open(taxontable) as mapfh:
        mapfile_lst = mapfh.readlines()

    out_line_lst = []

    if filehead:
        head_line_lst = mapfile_lst[0].rstrip('\n').split('\t')
        column_tag = head_line_lst[accession_field - 1]
        head_line_lst.append(column_tag + '_GMYC_' + args_method)
        out_head_lst = head_line_lst
        out_line_lst.append('\t'.join(out_head_lst))
        mapfile_lst = mapfile_lst[1:]

    for line in mapfile_lst:
        line = line.rstrip('\n')
        line_lst = line.split('\t')
        accession = line_lst[accession_field - 1]
        if accession == 'NA':
            new_line = line + '\t' + 'NA'
        else:
            if accession not in GMYC_dict:
                sys.exit(f'Error message:\n    {accession} in {taxontable} does not match that in GMYC_result_file')
            else:
                new_line = line + '\t' + GMYC_dict[accession]
        out_line_lst.append(new_line)
    if overwrite:
        with open(taxontable, 'w') as overwritefh:
            for line in out_line_lst:
                overwritefh.write(line + '\n')
    else:
        for line in out_line_lst:
            print(line, file=sys.stdout, flush=True)

if __name__ == '__main__':
    args = parse_args()
    GMYC_dict = parse_GMYC_result_2dict(args.GMYC_result, args.strip_minor_version)
    out_result_file(args.taxontable, args.file_head, args.field, GMYC_dict, args.overwrite, args.method)