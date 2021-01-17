#!/usr/bin/env python

'''
rmout_dictToGFF3.py -- parse RepeatMasker .out file to gff3.

Author:
    Y.P. Chen
Date:
    2020-10-24
Example:
    1. rmout_dictToGFF3.py rm.out > rm.gff3
    2. cat rm.out | rmout_dictToGFF3.py - > rm.gff3
'''

import sys
import argparse
import fileinput

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Any bugs should be reported to 764022822@qq.com")

    parser.add_argument('input',
        metavar='<rm.out>',
        help='input RepeatMaker output file.out')

    args = parser.parse_args()
    return args

def rmout_2_dict(in_file):
    '''Parse rmout to python3 dictionary.

    #rm.out format

       SW   perc perc perc  query           position in query        matching          repeat           position in repeat
    score   div. del. ins.  sequence        begin  end      (left)   repeat            class/family   begin  end    (left)   ID

    231   18.5  1.8  1.8  ML735207.1        4685   4739   (2798) + rnd-1_family-9    LINE/Tad1           8     62 (1211)    1
    518   18.4 12.8  0.0  ML735207.1        4836   4944   (2593) C rnd-1_family-4    DNA/TcMar-Fot1 (1726)    421    299    2
    10302 17.3  0.6  0.4  ML735208.1       18816  20665  (28957) + rnd-1_family-7    DNA/TcMar-Fot1      1   1853   (22)    3
    577   23.8  0.0  7.6  ML735208.1       34170  34310  (15312) C rnd-4_family-1122 DNA/TcMar-Ant1 (6069)   1523   1393    4
    '''
    rmout_dict = {}
    num_line = 0
    for line in fileinput.input(in_file):
        num_line += 1
        if num_line <= 3:
            continue

        line_lst = line.rstrip('\n').split()
        ID = line_lst[14]

        #1
        contig_id = line_lst[4]
        #2
        source = 'RepeatMasker'
        #3
        type_str = 'repeat_region'
        #4
        start = line_lst[5]
        #5
        end = line_lst[6]
        #6
        score = '.'
        #7
        strand = line_lst[8]
        if line_lst[8] == 'C':
            strand = '-'
        #8
        phase = '.'

        #9 attributes
        repeat_match = line_lst[9]
        repeat_class = line_lst[10]

        subject_left = int(line_lst[7].lstrip('(').rstrip(')'))
        contig_length = int(end) + subject_left

        if ID not in rmout_dict:
            rmout_dict[ID] = {}
            rmout_dict[ID]['contig_id'] = contig_id
            rmout_dict[ID]['source'] = source
            rmout_dict[ID]['type'] = type_str
            rmout_dict[ID]['start'] = start
            rmout_dict[ID]['end'] = end
            rmout_dict[ID]['score'] = score
            rmout_dict[ID]['strand'] = strand
            rmout_dict[ID]['phase'] = phase
            rmout_dict[ID]['contig_length'] = contig_length
            rmout_dict[ID]['repeat_match'] = repeat_match
            rmout_dict[ID]['repeat_class'] = repeat_class
        else:
            if len(line_lst) == 16:
                rmout_dict[ID]['contig_id'] = contig_id
                rmout_dict[ID]['source'] = source
                rmout_dict[ID]['type'] = type_str
                rmout_dict[ID]['start'] = start
                rmout_dict[ID]['end'] = end
                rmout_dict[ID]['score'] = score
                rmout_dict[ID]['strand'] = strand
                rmout_dict[ID]['phase'] = phase
                rmout_dict[ID]['repeat_match'] = repeat_match
                rmout_dict[ID]['repeat_class'] = repeat_class

    return rmout_dict

def rmout_dict_2_gff3(rmout_dict):
    '''Output gff3.
    '''
    gff3_version = '##gff-version 3'
    print(gff3_version, file=sys.stdout, flush=True)

    contig_list = []
    for ID in rmout_dict:
        contig_id = rmout_dict[ID]['contig_id']
        source = rmout_dict[ID]['source']
        type_str = rmout_dict[ID]['type']
        start = rmout_dict[ID]['start']
        end = rmout_dict[ID]['end']
        score = rmout_dict[ID]['score']
        strand = rmout_dict[ID]['strand']
        phase = rmout_dict[ID]['phase']
        contig_length = rmout_dict[ID]['contig_length']
        repeat_match = rmout_dict[ID]['repeat_match']
        repeat_class = rmout_dict[ID]['repeat_class']

        if contig_id not in contig_list:
            contig_list.append(contig_id)
            contig_info = f'##sequence-region {contig_id} 1 {contig_length}'
            print(contig_info, file=sys.stdout, flush=True)

        #9 attributes
        attributes_info = f'ID=repeat{ID};Name={repeat_match};Note=repeat_class:{repeat_class}'

        out_line_lst = [contig_id, source, type_str, start, end, score, strand, phase, attributes_info]
        out_line = '\t'.join(out_line_lst)
        print(out_line, file=sys.stdout, flush=True)

def main():
    args = parse_args()
    rmout_dict = rmout_2_dict(args.input)
    rmout_dict_2_gff3(rmout_dict)

if __name__ == "__main__":
    sys.exit(main())