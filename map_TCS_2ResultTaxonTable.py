#!/usr/bin/env python3
'''
map_TCS_Result_2TaxonTable.py -- map TCS statistical parsinomy reasult to the Taxon Accession Table.

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

    parser.add_argument('TCS_result',
        metavar='<result.*.log>',
        type=str,
        help='TCS result that should be result.log')

    parser.add_argument('--field',
        metavar='<int>',
        type=int,
        default=2,
        help='specify the column if accession (default to 2)')

    parser.add_argument('--overwrite',
        action='store_true',
        help='add TCS result to original input Taxon table')

    parser.add_argument('--file_head',
        action='store_true',
        help='if the Taxon Table has head line, this option must be selected')

    parser.add_argument('--strip_minor_version',
        action='store_true',
        help='strip accession minor version info. For example: AB704204.1 -> AB704204')

    args = parser.parse_args()
    return args

def deal_with_haplotype(TCS_resultfile):
    '''Dealing with haplotype list

    Args:
        TCS_resultfile (str) : TCS result file

    Return:
        dict : keys represent haplotype represent accession, and values represent other accessions
    '''
    haplotype_dict = {}
    with open(TCS_resultfile) as TCSfh:
        for line in TCSfh:
            line = line.rstrip('\n')
            if line.startswith(' - '):
                represent_accession, rest_accession_line = line.lstrip(' - ').split(' : ')
                represent_accession = represent_accession.strip()
                if not rest_accession_line:
                    continue
                rest_accession_lst = rest_accession_line.split()
                haplotype_dict[represent_accession] = rest_accession_lst
    return haplotype_dict

def parse_TCS_result_2dict(TCS_resultfile, strip, haplotype_dict):
    '''Parse TCS result into python dict, keys represent accession, values represent groupID

    Args:
        TCS_resultfile (str) : TCS result file name

    Return：
        dict ：keys represent accession, values represent groupID
    '''
    TCS_dict = {}
    with open(TCS_resultfile) as TCSfh:
        skip = True
        for line in TCSfh:
            if line.startswith('*** Network'):
                skip = False
                species_id = 'species_' + line.rstrip('\n').lstrip('*** Network').strip()
                continue

            if line.startswith('Total weight'):
                skip = True

            if skip:
                continue
            accession = line.split()[0]
            if strip:
                accession = accession.split('.')[0]
            TCS_dict[accession] = species_id

    for accession, rest_accession_lst in haplotype_dict.items():
        if strip:
            accession = accession.split('.')[0]
        species_id = TCS_dict[accession]
        for rest_accession in rest_accession_lst:
            if strip:
                rest_accession = rest_accession.split('.')[0]
            if rest_accession in TCS_dict:
                sys.exit(f'Error message:\n    rest accession in haplotype list is included in TCS_dict')
            TCS_dict[rest_accession] = species_id
    return TCS_dict

def out_result_file(taxontable, filehead, accession_field, TCS_dict, overwrite):
    '''Output result file with TCS result at the last column

    Args:
        taxontable (str) : mapping file is composed of taxon,otherinfo..., marker1_accession, marker2_accession...
                         If the accession missed, must use NA as placeholder
        accession_field (int) : specify the column of accession
        TCS_dict (dict) : keys represent accession, values represent groupID
    '''
    with open(taxontable) as mapfh:
        mapfile_lst = mapfh.readlines()

    out_line_lst = []

    if filehead:
        head_line_lst = mapfile_lst[0].rstrip('\n').split('\t')
        column_tag = head_line_lst[accession_field - 1]
        head_line_lst.append(column_tag + '_TCS')
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
            if accession not in TCS_dict:
                sys.exit(f'Error message:\n    {accession} in {taxontable} does not match that in TCS_result_file')
            else:
                new_line = line + '\t' + TCS_dict[accession]
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
    haplotype_dict = deal_with_haplotype(args.TCS_result)
    TCS_dict = parse_TCS_result_2dict(args.TCS_result, args.strip_minor_version, haplotype_dict)
    out_result_file(args.taxontable, args.file_head, args.field, TCS_dict, args.overwrite)