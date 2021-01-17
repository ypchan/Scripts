#!/usr/bin/env python3
'''
stat_assembly -- stat genome assemblies and get the following statistic values:
                  1:length   2:number_contigs 3:GC_content    4:N50      5:L50   6:N25
                  7:L25      8:N75            9:L75          10:N90     11:L90  12:minimum_len
                 13:median 14:mean           15:maximum_len  16:N_number
AUTHOR:
    chegnyanpeng1992@outlook.com
DATE:
    2021-01-15
'''
import os
import sys
import gzip
import argparse

def parse_args():
    '''Parse command-line arguments

    Return:
        object: args.<argument>
    '''
    parser = argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-i', '--input',
                        metavar='in.fa',
                        type=str,
                        nargs='+',
                        help='input file in FASTA format (.gz allowed)')

    parser.add_argument('-f', '--file',
                        metavar='<txt>',
                        help='the list of input files in one file per line')
    args = parser.parse_args()

    if not any([args.input, args.file]):
        sys.exit(f'Error: at least one option (--input or --file) is supplied')
    return args


def parse_fa_2dict(fafile):
    '''Parse fasta file(.gz allowed) into python3 dictionary, without '>' and newline signs(\n)
    {'id':'seq', ...}

    Args:
        fafile (str): A file name with corresponding path, and the file must be in FASTA format

    Return:
        fa_dict (dict) :A python3 dictionary without '>' and newline signs(\n). {'id':'seq', ...}
    '''
    fa_dict = {}
    fa_fh = gzip.open(fafile, 'rt') if fafile.endswith('.gz') else open(fafile, 'rt')
    for line in fa_fh:
        if not line:
            continue
        line = line.rstrip('\n')
        if line.startswith('>'):
            seq_id = line.lstrip('\n')
            fa_dict[seq_id] = []
        else:
            fa_dict[seq_id].append(line)
    fa_dict = {seq_id:''.join(seq_lst) for seq_id,seq_lst in fa_dict.items()}
    return fa_dict

def sort_fadict_by_length(fa_dict):
    '''Sort fa_dict by sequence length

    Args:
        fa_dict (dict): A unsorted dictionary

    Return:
        dict: A sorted dictionay by length
    '''
    return dict(sorted(fa_dict.items(), key = lambda item:len(item[1]),reverse=True))


def calculate_sequence_statistic_values(sorted_fa_dict):
    '''Calucate sequence statistic values return them in dictionary

    Statistic values : length, number_contigs, GC_content, N50, L50, N25, L25, N75, L75,
                       N90, L90, minimum_len, median, mean, maximum_len, N_number

    Args:
        sorted_fa_dict (dict): A sorted fa dict by sequence length

    Return
        dict: A dictionary contains sequence statistic values
    '''
    statistics_dict = {}
    contigs_len_lst = [len(seq) for _,seq in sorted_fa_dict.items()]

    length = sum(contigs_len_lst)
    statistics_dict['Length'] = length

    minimum_len = min(contigs_len_lst)
    statistics_dict['MinLen'] = minimum_len

    maximum_len = max(contigs_len_lst)
    statistics_dict['MaxLen'] = maximum_len

    num_contigs = len(sorted_fa_dict)
    statistics_dict['Count'] = num_contigs

    mean = int(length / num_contigs)
    statistics_dict['Mean'] = mean

    if num_contigs % 2 == 0:
        median = int((contigs_len_lst[int(num_contigs / 2)] + contigs_len_lst[int(num_contigs / 2 - 1)]) / 2)
    else:
        median = contigs_len_lst[int((num_contigs - 1) / 2)]

    statistics_dict['Media'] = median

    number_atgc = 0
    number_gc = 0
    for seq_id, seq in sorted_fa_dict.items():
        seq = seq.upper()
        number_A = seq.count('A')
        number_T = seq.count('T')
        number_G = seq.count('G')
        number_C = seq.count('C')
        number_atgc += number_A + number_T + number_G + number_C
        number_gc += number_G + number_C
    gc_content = number_gc / number_atgc * 100
    statistics_dict['GC%'] = round(gc_content, 4)

    L_num = 0
    cumulative_len = 0
    for seq_id, seq in sorted_fa_dict.items():
        L_num += 1
        cumulative_len += len(seq)
        if cumulative_len / length >= 0.9:
            N90 = len(seq)
            L90 = L_num
            statistics_dict['N90'] = N90
            statistics_dict['L90'] = L90

        if cumulative_len / length >= 0.75:
            N75 = len(seq)
            L75 = L_num
            statistics_dict['N75'] = N75
            statistics_dict['L75'] = L75

        if cumulative_len / length >= 0.5:
            N50 = len(seq)
            L50 = L_num
            statistics_dict['N50'] = N50
            statistics_dict['L50'] = L50

        if cumulative_len / length >= 0.25:
            N25 = len(seq)
            L25 = L_num
            statistics_dict['N25'] = N25
            statistics_dict['L25'] = L25

    contigs_N_count_lst = [seq.upper().count('N') for seq_id,seq in sorted_fa_dict.items()]
    count_N = sum(contigs_N_count_lst)
    statistics_dict['CountN'] = count_N
    return statistics_dict

if __name__ == '__main__':
    args = parse_args()
    head_lst = ['Length', 'MinLen', 'MaxLen', 'GC%', 'Count', 'Mean', 'Media', 'L90', 'N90', 'L75', 'N75', 'L50', 'N50', 'L25', 'N25']
    print('File' + '\t' + '\t'.join(head_lst), file=sys.stdout, flush=True)

    if args.input:
        for fa in args.input:
            fa_dict = parse_fa_2dict(fa)
            sorted_fa_dict = sort_fadict_by_length(fa_dict)
            statistics_dict = calculate_sequence_statistic_values(sorted_fa_dict)
            stat_lst = [str(tatistics_dict.get(key)) for key in head_lst]
            filename = os.path.basename(fa)
            print(filename + '\t' + '\t'.join(stat_lst), file=sys.stdout, flush=True)

    if args.file:
        file_lst = open(args.file, 'rt').readlines()
        file_lst = [filename.rstrip('\n') for filename in file_lst]
        for fa in file_lst:
            fa_dict = parse_fa_2dict(fa)
            sorted_fa_dict = sort_fadict_by_length(fa_dict)
            statistics_dict = calculate_sequence_statistic_values(sorted_fa_dict)
            stat_lst = [str(statistics_dict.get(key)) for key in head_lst]
            filename = os.path.basename(fa)
            print(filename + '\t' + '\t'.join(stat_lst), file=sys.stdout, flush=True)