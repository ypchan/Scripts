#!/usr/bin/env python3
'''
ftk_gc_content_without_TE.py -- gc content is calculated as the following
                                count(G + C) / count(A + T + G + C) * 100%

Date: 2020-10-10
Bugs: Any bugs should be reported to yanpengch@qq.com

Input:
../00_genome_data/Aciaci1.fna  ../02_repeatmasker/Aciaci1_repeatmasker/Aciaci1.fna.out
../00_genome_data/Corma2.fna   ../02_repeatmasker/Corma2_repeatmasker/Corma2.fna.out
'''
import os
import sys
import argparse


parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument(
    '-i',
    '--input',
    type=str,
    required=True,
    help='genome file and rm result.out(optional)')


args = parser.parse_args()


def grep_sort_rmout(rm_out: str) -> list:
    '''filter unuseful lines
    remove head 3 lines, sort by contig id and start position
    '''
    tmp_out = rm_out + '_tmp'
    command = f"grep -v -e 'position in query' -e 'class/family' -e '^$' -e 'rRNA' -e 'Satellite' -e 'Satellite/centr' -e 'Simple_repeat' -e 'Low_complexity' -e '*$' {rm_out} > {tmp_out}"
    p = os.system(command)
    if p != 0:
        sys.exit(f'Error: run {command}')

    with open(tmp_out) as infh:
        interspersed_repeat_lst = infh.readlines()

    command1 = f'rm {tmp_out}'
    p1 = os.system(command1)
    if p1 != 0:
        sys.exit(f'Eror: run {command1}')

    interspersed_repeat_lst = [line.rstrip(
        '\n').split() for line in interspersed_repeat_lst]
    return interspersed_repeat_lst


def calculate_gc_content(genome, interspersed_repeat_lst):
    '''Check whether the genome caontains unknown or masked character 'N'
    '''
    fa_dict = dict()
    with open(genome) as fh:
        for line in fh:
            line = line.rstrip('\n')
            if line.startswith('>'):
                contig_id = line.lstrip('>').split()[0]
                fa_dict[contig_id] = []
            else:
                line = line.upper()
                fa_dict[contig_id].append(line)

    fa_dict = {k: ''.join(seq_lst) for k, seq_lst in fa_dict.items()}

    A_base_count = []
    T_base_count = []
    G_base_count = []
    C_base_count = []
    for _, seq in fa_dict.items():
        A_base_count.append(seq.count('A'))
        T_base_count.append(seq.count('T'))
        G_base_count.append(seq.count('G'))
        C_base_count.append(seq.count('C'))

    total_A_base = sum(A_base_count)
    total_T_base = sum(T_base_count)
    total_G_base = sum(G_base_count)
    total_C_base = sum(C_base_count)

    # TE gc
    repeat_A_base_count = []
    repeat_T_base_count = []
    repeat_G_base_count = []
    repeat_C_base_count = []
    for record_lst in interspersed_repeat_lst:
        contig_id = record_lst[4]
        start_pos = int(record_lst[5])
        end_pos = int(record_lst[6])
        seq_repeat = fa_dict[contig_id][start_pos-1:end_pos]
        repeat_A_base_count.append(seq_repeat.count('A'))
        repeat_T_base_count.append(seq_repeat.count('T'))
        repeat_G_base_count.append(seq_repeat.count('G'))
        repeat_C_base_count.append(seq_repeat.count('C'))

    total_repeat__A_base = sum(repeat_A_base_count)
    total_repeat_T_base = sum(repeat_T_base_count)
    total_repeat_G_base = sum(repeat_G_base_count)
    total_repeat_C_base = sum(repeat_C_base_count)

    # output
    total_te_size = total_repeat__A_base + total_repeat_T_base + \
        total_repeat_G_base + total_repeat_C_base
    genome_gc_content = (total_G_base + total_C_base) / \
        (total_A_base + total_G_base + total_C_base + total_T_base) * 100
    genome_no_te_gc_content = (total_G_base + total_C_base -
                               total_repeat_G_base - total_repeat_C_base) / (total_A_base + total_G_base +
                                                                             total_C_base + total_T_base - total_repeat__A_base - total_repeat_T_base -
                                                                             total_repeat_G_base - total_repeat_C_base) * 100
    repeat_gc_content = (total_repeat_G_base + total_repeat_C_base) / (total_repeat__A_base +
                                                                       total_repeat_T_base + total_repeat_G_base + total_repeat_C_base) * 100
    print(f'{genome}\t{genome_gc_content:.3f}\t{genome_no_te_gc_content:.3f}\t{repeat_gc_content:.3f}\t{total_te_size}',
          file=sys.stdout, flush=True)


if __name__ == '__main__':
    print(f'Genome\tGC_content\tGC_content_no_TE\tGC_content_Te\tTE_size',
          file=sys.stdout, flush=True)
    with open(args.input) as infh:
        for line in infh:
            genome, rm_out = line.rstrip('\n').split()
            interspersed_repeat_lst = grep_sort_rmout(rm_out)
            calculate_gc_content(genome, interspersed_repeat_lst)
    sys.exit(0)
