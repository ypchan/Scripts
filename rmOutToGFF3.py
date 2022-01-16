#!/usr/bin/env python

'''
rmOutToGFF3.py -- parse RepeatMasker *.out file to gff3.

Author & date:
    chenyanpeng1992@outlook.com, 2020-10-24
Example:
    rmOutToGFF3.py rm.out > rm.gff3
'''

import sys
import argparse
import fileinput

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('input',
        metavar='<rm.out>',
        help='input RepeatMaker output file.out')

    args = parser.parse_args()
    return args

def rmout_2_gff3(in_file):
    '''Parse rmout to python3 dictionary.

    RepeatMasker output：
    ---------------------------------------------------------------------------------------------------------------------------
       SW   perc perc perc  query           position in query        matching          repeat           position in repeat
    score   div. del. ins.  sequence        begin  end      (left)   repeat            class/family   begin  end    (left)   ID

    231   18.5  1.8  1.8  ML735207.1        4685   4739   (2798) + rnd-1_family-9    LINE/Tad1           8     62 (1211)    1
    518   18.4 12.8  0.0  ML735207.1        4836   4944   (2593) C rnd-1_family-4    DNA/TcMar-Fot1 (1726)    421    299    2
    10302 17.3  0.6  0.4  ML735208.1       18816  20665  (28957) + rnd-1_family-7    DNA/TcMar-Fot1      1   1853   (22)    3
    577   23.8  0.0  7.6  ML735208.1       34170  34310  (15312) C rnd-4_family-1122 DNA/TcMar-Ant1 (6069)   1523   1393    4
    '''
    rmout_dict = {}
    infh = open(in_file)
    line_lst = infh.readlines()
    infh.close()

    # Skipping head 2 lines
    line_lst = line_lst[3:]
    line_lst = [line.split() for line in line_lst]
    # Delete duplicated record, only records star marked will be saved
    duplicate_record_index_lst = []
    for index,lst in enumerate(line_lst):
        if lst[-1] == '*':
            duplicate_record_index_lst.append(index - 1)

    for index in sorted(duplicate_record_index_lst, reverse=True):
            del line_lst[index]

    num_repeats = len(line_lst)
    num_digits = len(str(num_repeats))

    # Gff3 header
    print('##gff-version 3', file=sys.stdout, flush=True)

    last_contig_id = 0
    source = 'RepeatMasker'
    feature_type = 'dispersed_repeat'
    phase = '.'

    n = 0
    for lst in line_lst:
        n += 1
        contig_id = lst[4]
        feature_start = lst[5]
        feature_end = lst[6]
        contig_len = int(feature_end) + int(lst[7].lstrip('(').rstrip(')'))
        score = lst[0].strip()
        strand = lst[8]
        target_match = lst[9]
        target_start = lst[11]
        target_end = lst[12]
        name = lst[10]
        target_len = int(lst[13].lstrip('(').rstrip(')')) + int(target_end)
        note = f'Note=target_len_{target_len}'
        attributes = f'ID=repeat{n:0{num_digits}};Target={target_match} {target_start} {target_end};Note=target_len {target_len}'
        if strand == 'C':
            strand = '-'

        if contig_id != last_contig_id:
            sequence_region = f'##sequence-region {contig_id} 1 {contig_len}'
            print(sequence_region, file=sys.stdout, flush=True)
            last_contig_id = contig_id
        out_line_lst = [contig_id, source, feature_type, feature_start, feature_end, score, strand, phase, attributes]
        out_line = '\t'.join(out_line_lst)
        print(out_line, file=sys.stdout, flush=True)

if __name__ == "__main__":
    args = parse_args()
    rmout_2_gff3(args.input)