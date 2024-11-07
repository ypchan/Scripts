#!/usr/bin/env python3
'''
ftk_concatenate_msa.py -- concatenate multiple sequence alignments of barcodes by common identifiers.

DATE: 2022-01-19
BUGS: Any bugs should be reported to yanpengch@qq.com

UPDATE: 2023-02-06 optimized output
'''


import os
import sys
import argparse

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('-i', '--input',
                    required=True,
                    nargs='+',
                    type=str,
                    metavar='<msa.fna>',
                    help='multiple alignment files with common IDs')

parser.add_argument('-p', '--prefix',
                    required=True,
                    type=str,
                    metavar='<concat>',
                    help='prefix of the concatenated MSA filename. Do not provide suffix:.fasta/.fna')

parser.add_argument('--abbrev',
                    action='store_true',
                    help='create a new msa file with abbreviated strain ids in strict phylip format')

args = parser.parse_args()


def all_taxa(msafile_tuple):
    '''Getting all taxa table.
    '''
    all_msa_dict = {}
    taxa_lst = []
    for msa in msafile_tuple:
        all_msa_dict[msa] = {}
        with open(msa, 'rt') as fafh:
            for line in fafh:
                line = line.rstrip('\n')
                if line.startswith('>'):
                    taxa_id = line.lstrip('>')
                    taxa_lst.append(taxa_id)
                    all_msa_dict[msa][taxa_id] = []
                else:
                    all_msa_dict[msa][taxa_id].append(line)
    taxa_lst = list(set(taxa_lst))

    for msa, fa_dict in all_msa_dict.items():
        all_msa_dict[msa] = {k: ''.join(v) for k, v in fa_dict.items()}
    return taxa_lst, all_msa_dict


def get_msa_length(all_msa_dict):
    '''Getting msa length.
    '''
    msa_length_dict = {}
    start = 1
    print('', file=sys.stdout, flush=True)
    patition_out_file = os.path.dirname(args.prefix) + '/parts_region.txt'
    with open(patition_out_file, 'wt') as patitionfh:
        print(f'#Msa\tRegion', file=sys.stdout, flush=True)
        patitionfh.write(f'#Msa\tRegion\n')
        for msa, fa_dict in all_msa_dict.items():
            for taxa_id, seq in fa_dict.items():
                fa_length = len(seq)
                msa_length_dict[msa] = fa_length
                end = start + fa_length - 1
                print(f'{os.path.basename(msa)}\t{start}-{end}',
                      file=sys.stdout, flush=True)
                patitionfh.write(f'{msa}\t{start}-{end}\n')
                start = start + fa_length
                break

    return msa_length_dict


def add_missingdata_to_alignment(taxa_lst, all_msa_dict, msa_length_dict):
    '''Adding missing data into some msa file.
    '''
    print('', file=sys.stdout, flush=True)
    print('#Msa\tLength\tMissing', file=sys.stdout, flush=True)
    missing_out_file = os.path.dirname(args.prefix) + '/missing_taxa.txt'
    with open(missing_out_file, 'wt') as missingfh:
        for msa, fadict in all_msa_dict.items():
            msa_length = msa_length_dict[msa]
            taxa_missing_lst = []
            for taxa_id in taxa_lst:
                if taxa_id not in fadict:
                    taxa_missing_lst.append(taxa_id)
                    all_msa_dict[msa][taxa_id] = '?' * msa_length

            print(f'{os.path.basename(msa)}\t{msa_length}\t-{str(len(taxa_missing_lst))}',
                  file=sys.stdout, flush=True)

            missingfh.write(
                '{os.path.basename(msa)}\t{msa_length}-{len(taxa_missing_lst)}')
            missingfh.write("\n".join(taxa_missing_lst) + '\n')
        print()
    return all_msa_dict


def combine(taxa_lst, all_msa_dict):
    '''Combing msa file by common ids
    '''
    combine_dict = {}
    for taxa_id in taxa_lst:
        combine_dict[taxa_id] = []
        for msa, fa_dict in all_msa_dict.items():
            seq = fa_dict[taxa_id]
            combine_dict[taxa_id].append(seq)
    return combine_dict


def out_abbreviated_phylip(combine_dict, args_prefix, args_abbrev):
    '''output abbreviated phylip
    '''
    if not args_abbrev:
        return

    out_phylip_file = args_prefix + '.abbrev.phy'
    num_taxa = len(combine_dict)
    for _, seq_lst in combine_dict.items():
        len_aln = len(''.join(seq_lst))
        break

    with open(out_phylip_file, 'wt') as ofh:
        ofh.write(f'{num_taxa} {len_aln}\n')
        num = 0
        for _, seq_lst in combine_dict.items():
            num += 1
            abbreviated_id = 't' + str(num)
            sequence = ''.join(seq_lst)
            ofh.write(f'{abbreviated_id:10}{sequence}\n')


if __name__ == '__main__':
    taxa_lst, all_msa_dict = all_taxa(args.input)
    msa_length_dict = get_msa_length(all_msa_dict)
    all_msa_dict = add_missingdata_to_alignment(
        taxa_lst, all_msa_dict, msa_length_dict)
    combine_dict = combine(taxa_lst, all_msa_dict)

    with open(args.prefix + '.fna', 'wt') as outfh:
        for taxa_id, seq in combine_dict.items():
            outfh.write(f'>{taxa_id}\n{"".join(seq)}\n')

    out_abbreviated_phylip(combine_dict, args.prefix, args.abbrev)

    sys.exit(0)
