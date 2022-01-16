#!/usr/bin/env python
'''
check_dupseq_for_beast.py -- report and remove duplicated sequences in alignment file for BEAST analysis

DATA: 2021-02-25
AUTHOR：chenyanpeng1992@outlook.com
USAGE:
    check_dupseq_for_beast.py alignment.fasta > alignment.rmdup.fasta 2> duplicated.accession.txt
'''
import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('inalignedfile',
        metavar='<alignment.fasta>',
        type=str,
        help='input alignment file must be in FASTA format')
    
    parser.add_argument('outalginedfile',
        metavar='<alignment_beast.fasta>',
        type=str,
        help='out file name')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    fa_dict = {}
    strip_newline_fa_dict = {}
    with open (args.inalignedfile) as fafh:
        for line in fafh:
            line = line.rstrip('\n')
            if line.startswith('>'):
                seq_id = line.lstrip('>')
                fa_dict[seq_id] = []
                strip_newline_fa_dict[seq_id] = []
            else:
                fa_dict[seq_id].append(line)
                strip_newline_fa_dict[seq_id].append(line)

    strip_newline_fa_dict = {k:''.join(v) for k,v in strip_newline_fa_dict.items()}

    dup_dict = {}
    for k1,v1 in strip_newline_fa_dict.items():
        for k2,v2 in strip_newline_fa_dict.items():
            if v1 == v2 and k1 != k2:
                if k1 not in dup_dict:
                    dup_dict[k1] = [k2]
                else:
                    dup_dict[k1].append(k2)

    all_dup_seq_lst = []
    for seq_id,dup_lst in dup_dict.items():
        print(f'>{seq_id}*', file=sys.stdout, flush=True)
        for dup_seq_id in dup_lst:
            all_dup_seq_lst.append(dup_seq_id)
            print(f' {dup_seq_id}', file=sys.stdout, flush=True)
    with open(args.outalignedfile, 'w') as outfh:
        for seq_id, seq_lst in fa_dict.items():
            if seq_id not in all_dup_seq_lst:
                outfh.write(f'>{seq_id}\n')
                for seq in seq_lst:
                    outfh.write(seq + '\n')