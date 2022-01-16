#!/usr/bin/env python3
'''
map_bPTP_Result_2TaxonTable.py -- map bPTP reasult to the Taxon Accession Table.

DATE: 2021-02-24
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

    parser.add_argument('bPTP_result',
        metavar='<result.*Partition.txt>',
        type=str,
        help='bPTP result that should be [*.PTPhSupportPartition.txt | *.PTPMLPartition.txt]')

    parser.add_argument('--field',
        metavar='<int>',
        type=int,
        default=2,
        help='specify the column if accession (default to 2)')

    parser.add_argument('--method',
        metavar='<HPP|ML>',
        type=str,
        default='HPP',
        help='highest posterial probablity supported species delimitation(HPP);maximum likelihood species delimitation(ML)')

    parser.add_argument('--overwrite',
        action='store_true',
        help='add bPTP result to original input Taxon table')

    parser.add_argument('--file_head',
        action='store_true',
        help='if the Taxon Table has head line, this option must be selected')

    parser.add_argument('--strip_minor_version',
        action='store_true',
        help='strip accession minor version info. For example: AB704204.1 -> AB704204')

    args = parser.parse_args()
    return args

def parse_bPTP_result_2dict(bPTP_resultfile, strip):
    '''Parse bPTP result into python dict, keys represent accession, values represent groupID

    Args:
        bPTP_resultfile (str) : bPTP result file name

    Return：
        dict ：keys represent accession, values represent groupID
    '''
    bPTP_dict = {}
    with open(bPTP_resultfile) as bPTPfh:
        for line in bPTPfh:
            line = line.rstrip('\n')
            if line.startswith('#'):
                continue
            if not line:
                continue
            if line.startswith('Species'):
                species_id = line.split('(support')[0].rstrip().replace(' ', '_').lower()
                continue
            accession_lst = line.lstrip().split(',')
            for accession in accession_lst:
                if strip:
                    accession = accession = accession.split('.')[0]
                if accession in bPTP_dict:
                    sys.exit(f'Error message:\n    duplicated accession {accession}')

                bPTP_dict[accession] = species_id
    return bPTP_dict

def out_result_file(taxontable, filehead, accession_field, bPTP_dict, overwrite, args_method):
    '''Output result file with bPTP result at the last column

    Args:
        taxontable (str) : mapping file is composed of taxon,otherinfo..., marker1_accession, marker2_accession...
                         If the accession missed, must use NA as placeholder
        accession_field (int) : specify the column of accession
        bPTP_dict (dict) : keys represent accession, values represent groupID
    '''
    with open(taxontable) as mapfh:
        mapfile_lst = mapfh.readlines()

    out_line_lst = []

    if filehead:
        head_line_lst = mapfile_lst[0].rstrip('\n').split('\t')
        column_tag = head_line_lst[accession_field - 1]
        head_line_lst.append(column_tag + '_bPTP_' + args_method)
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
            if accession not in bPTP_dict:
                sys.exit(f'Error message:\n    {accession} in {taxontable} does not match that in bPTP_result_file')
            else:
                new_line = line + '\t' + bPTP_dict[accession]
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
    bPTP_dict = parse_bPTP_result_2dict(args.bPTP_result, args.strip_minor_version)
    out_result_file(args.taxontable, args.file_head, args.field, bPTP_dict, args.overwrite, args.method)