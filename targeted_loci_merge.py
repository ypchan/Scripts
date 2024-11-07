#!/usr/bin/env python3
'''
targeted_loci_merge.py -- to create a taxa table including genbank accession of ITS, LSU, SSU for each strain.

AUTHOR:
    chegnyanpeng1992@outlook.com
DATE:
    2023-01-14
'''
import sys
import argparse


parser = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('--its',
                    metavar='ITS.fasta',
                    type=str,
                    required=True,
                    help='ITS.fasta downloaded from the Refseq')

parser.add_argument('--ssu',
                    metavar='SSU.fasta',
                    type=str,
                    required=True,
                    help='SSU.fasta downloaded from the Refseq')

parser.add_argument('--lsu',
                    metavar='LSU.fasta',
                    type=str,
                    required=True,
                    help='LSU.fasta downloaded from the Refseq')

args = parser.parse_args()


def parse_its(args_its):
    its_dict = {}
    with open(args_its, 'rt') as infh:
        for line in infh:
            if line.startswith('>'):
                line = line.split(' ITS region')[0]
                line_lst = line.split(' ')
                accession = line_lst[0].lstrip('>')
                species = line_lst[1] + ' ' + line_lst[2]
                strain_num = ' '.join(line_lst[3:])
                key_id = species + '++' + strain_num
                its_dict[key_id] = accession
    return its_dict


def parse_ssu(args_ssu):
    ssu_dict = {}
    with open(args_ssu, 'rt') as infh:
        for line in infh:
            if line.startswith('>'):
                line = line.split(' 18S ')[0]
                line_lst = line.split(' ')
                accession = line_lst[0].lstrip('>')
                species = line_lst[1] + ' ' + line_lst[2]
                strain_num = ' '.join(line_lst[3:])
                key_id = species + '++' + strain_num
                ssu_dict[key_id] = accession
    return ssu_dict


def parse_lsu(args_lsu):
    lsu_dict = {}
    with open(args_lsu, 'rt') as infh:
        for line in infh:
            if line.startswith('>'):
                line = line.split(' 28S ')[0]
                line_lst = line.split(' ')
                accession = line_lst[0].lstrip('>')
                species = line_lst[1] + ' ' + line_lst[2]
                strain_num = ' '.join(line_lst[3:])
                key_id = species + '++' + strain_num
                lsu_dict[key_id] = accession
    return lsu_dict


def merge(its_dict, ssu_dict, lsu_dict):
    '''[ITS, SSU, LSU]
    '''
    merge_dict = {}
    for species, accession in its_dict.items():
        merge_dict[species] = [accession, '-', '-']

    for species, accession in ssu_dict.items():
        if species in merge_dict:
            merge_dict[species][1] = accession
        else:
            merge_dict[species] = ['-', accession, '-']

    for species, accession in lsu_dict.items():
        if species in merge_dict:
            merge_dict[species][2] = accession
        else:
            merge_dict[species] = ['-', '-', accession]

    return merge_dict


if __name__ == '__main__':
    its_dict = parse_its(args.its)
    ssu_dict = parse_ssu(args.ssu)
    lsu_dict = parse_lsu(args.lsu)
    merge_dict = merge(its_dict, ssu_dict, lsu_dict)

    print(f'Species\tStrain\tITS\tSSU\tLSU', file=sys.stdout, flush=True)
    for species_strain, accession_lst in merge_dict.items():
        try:
            species, strain = species_strain.split('++')
        except:
            sys.exit(f'\nError: {species_strain}')
        accession_str = '\t'.join(accession_lst)
        print(f'{species}\t{strain}\t{accession_str}',
              file=sys.stdout, flush=True)
    sys.exit(0)
