#!/usr/bin/env python3

import os

def parse_fa_2rawdict(fafile):
    '''Parse fasta file(.gz allowed) into python3 dictionary, '>' and newline signs(\n) were saved
    {'>id1\n':['seq1_line1\n', 'seq1_line2\n', ...], ...}

    Args:
        fafile (str): a file name with corresponding path, and the file must be in FASTA format

    Return:
        fa_raw_dict (dict): a python3 dictionary. '>' and newline signs(\n) were saved. 
                            {'>id1\n':['seq1_line1\n', 'seq1_line2\n', ...], ...}     
    '''
    fa_raw_dict = {}

    fa_fh = gzip.open(fafile, 'rt') if fafile.endswith('.gz') else open(fafile, 'rt')
    for line in fa_fh:
        if not line:
            continue
        if line.startswith('>'):
            seq_id = line
            fa_raw_dict[seq_id] = []
        else:
            fa_raw_dict[seq_id].append(line)
    return fa_raw_dict

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
    '''
    Sort fa_dict by sequence length

    Parameter
    ---------
    fa_dict : dict
        A unsorted dictionary
    
    Return
    ------
        dict: A sorted dictionay by length
    '''
    return sorted(fa_dict.items(), key = lambda kv:length(kv[1]),reverse=True)
    
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
    contigs_len_lst = [len(seq) for seq in sorted_fa_dict.values()]

    length = sum(contigs_len_lst)
    statistics_dict['length'] = length
    
    minimum_len = min(contigs_len_lst)
    statistics_dict['minimum_len'] = minimum_len

    maximum_len = max(contigs_len_lst)
    statistics_dict['maximum_len'] = maximum_len

    number_contigs = len(sorted_fa_dict)
    statistics_dict['contigs'] = number_contigs
    
    mean = length / number_contigs
    statistics_dict['mean'] = mean

    if number_contigs % 2 == 0:
        median = (contigs_len_lst[number_contigs / 2] + contigs_len_lst[number_contigs / 2 - 1]) / 2
    else:
        median = contigs_len_lst[(number_contigs -1) / 2]
    
    statistics_dict['median'] = median

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
    gc_content = number_gc / number_atgc
    statistics_dict['gc_content'] = gc_content

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
    
    contigs_N_count_lst = [seq.upper().count('N') for seq in sorted_fa_dict.values()]
    count_N = sum(contigs_N_count_lst)
    statistics_dict['count_N'] = count_N
    return statistics_dict

def base_locater(fa_dict, seq_id, position_tuple):
    '''Get the base according position(s)
    
    Input:
        position_tuple : 11-15, 11, 12, 12-13
    Result:
        Flag | Bases
        -----|-------
        11-15: ATGCA
        11   : A 
        12   : T
        12-13: TG

    Args:
        fa_dict (dict) : a genome fasta. Keys represent seq identifiers, and values represent sequences
        seq_id (str) : sequence identifier
        position_tuple (tuple) : a int tuple
    
    Return:
        NULL
    '''
    max_len_flag = max([len(i) for i in position_tuple])
    for pos in position_tuple:
        if '-' in pos:
            pos_start, pos_end = [int(i) for i in pos.split('-')]
            show_bases = fa_dict[seq_id][pos_start - 1: pos_end]
            print(f'{pos:<{max_len_flag}} : {show_bases}', file=sys.stdout, flush=True)
        else:
            pos = int(pos)
            show_base = fa_dict[seq_id][pos]
            print(f'{pos:<{max_len_flag}} : {show_base}', file=sys.stdout, flush=True)

class Phylip():
    def __init__(self, infile='alignment.phy', filetype='sequential'):
        self.basename = os.path.basename(infile)
        self.filetype = filetype
        self.abspath = os.path.abspath(infile)
        
        infile_fh = open(infile, 'rt')
        self.__line_lst =  infile_fh.readlines()
        infile_fh.close()

    def taxons(self):
        