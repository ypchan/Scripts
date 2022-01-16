#!/usr/bin/env python3
'''
map_ABGD_Result_2TaxonTable.py -- map ABGD reasult to the Taxon Accession Table.

DATE: 2021-02-19
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

    parser.add_argument('abgd_result',
        metavar='<abgd_part.1.txt>',
        type=str,
        help='ABGD result: *.part.1.txt')

    parser.add_argument('--field',
        metavar='<int>',
        type=int,
        default=2,
        help='specify the column if accession (default to 2)')

    parser.add_argument('--overwrite',
        action='store_true',
        help='add abgd result to original input Taxon table')

    parser.add_argument('--file_head',
        action='store_true',
        help='if the Taxon Table has head line, this option must be selected')

    parser.add_argument('--strip_minor_version',
        action='store_true',
        help='strip accession version info. For example: AB704204.1 -> AB704204')

    args = parser.parse_args()
    return args

def parse_abgd_result_2dict(abgd_resultfile, strip):
    '''Parse ABGD result into python dict, keys represent accession, values represent groupID

    Args:
        abgd_resultfile (str) : ARGD result file name

    Return：
        dict ：keys represent accession, values represent groupID
    '''
    abgd_dict = {}
    with open(abgd_resultfile) as abgdfh:
        for line in abgdfh:
            groupid_number, accession_line = line.rstrip('\n').split(";")
            groupid = groupid_number.split('n:')[0].replace(' ', '').replace('[', '').replace(']', '').lstrip('Group')
            species_id = 'species' + '_' + groupid
            accession_lst = accession_line.lstrip('id: ').split()

            for accession in accession_lst:
                if strip:
                    accession = accession.split('.')[0]

                if accession not in abgd_dict:
                    abgd_dict[accession] = species_id
                else:
                    sys.exit(f'Error message: \n    duplicated accessions {accession}')
    return abgd_dict

def out_result_file(taxontable, filehead, accession_field, abgd_dicti, overwrite):
    '''Output result file with abgd result at the last column

    Args:
        taxontable (str) : mapping file is composed of taxon,otherinfo..., marker1_accession, marker2_accession...
                         If the accession missed, must use NA as placeholder
        accession_field (int) : specify the column of accession
        abgd_dict (dict) : keys represent accession, values represent groupID
    '''
    with open(taxontable) as mapfh:
        mapfile_lst = mapfh.readlines()

    out_line_lst = []

    if filehead:
        head_line_lst = mapfile_lst[0].rstrip('\n').split('\t')
        column_tag = head_line_lst[accession_field - 1]
        head_line_lst.append(column_tag + '_ABGD')
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
            if accession not in abgd_dict:
                sys.exit(f'Error message:\n    {accession} not in {taxontable}')
            else:
                new_line = line + '\t' + abgd_dict[accession]
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
    abgd_dict = parse_abgd_result_2dict(args.abgd_result, args.strip_minor_version)
    out_result_file(args.taxontable, args.file_head, args.field, abgd_dict, args.overwrite)