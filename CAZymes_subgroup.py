#!/usr/bin/env python3
'''
CAZymes_subgroup -- subgroup CAZymes into multiple subgroups: PCWDEs, FCWDEs, Cellulose, 
                    Hemicellulose, Lignin, Pectin, Peptidoglycan, Mannan, Glucan, Chitin, Sucrose

Author:
    chengyanpeng1992@outlook.com
Bugs: 
    Any bugs should be reported to the above E-mail.

REF:
 Large-scale genome sequencing of mycorrhizal fungi provides insights into the early evolution of symbiotic traits. supplemtary information 7 sheet H
'''
import re
import sys
import argparse


'''cazymes subgroups
PCWDE    AA1_1 AA2 AA9 AA10 AA14 AA16 CBM1 CBM63 CBM67 CE5 CE8 CE12 CE15 GH3 GH5_4 GH5_1 GH5_5 GH5_7 GH5_22 GH6 GH7 GH8 GH10 GH11 GH12 GH26 GH28 GH30_7 GH43 GH44 GH45 GH48 GH51 GH52 GH53 GH54 GH62 GH67 GH74 GH78 GH88 GH93 GH105 GH106 GH113 GH115 GH131 GH134 PL1 PL3 PL4 PL8_4 PL9 PL11 PL14_4 PL26
FCWDE    AA15 CBM5 CBM12 CBM14 CBM18 CBM43 GH5_9 GH5_15 GH5_31 GH16 GH17 GH18 GH19 GH20 GH23 GH24 GH25 GH30_3 GH30_5 GH46 GH55 GH64 GH71 GH72 GH75 GH76 GH81 GH92 GH125 GH128 GH132 GH135
Cellulose    AA9 AA10 AA16 CBM1 CBM63 GH5_4 GH5_1 GH5_5 GH5_22 GH6 GH7 GH12 GH44 GH45 GH48 GH131
Hemicellulose    AA14 CE5 CE15 GH5_7 GH8 GH10 GH11 GH30_7 GH43 GH51 GH52 GH54 GH62 GH67 GH74 GH93 GH113 GH115 GH134
Lignin    AA2
Pectin    CBM67 CE8 CE12 GH28 GH51 GH53 GH78 GH88 GH105 GH106 PL1 PL3 PL4 PL8_4 PL9 PL11 PL14_4 PL26
Peptidoglycan    GH23 GH24 GH25
Mannan    GH5_31 GH26 GH76 GH92 GH125
Glucan    GH5_9 GH5_15 GH16 GH17 GH55 GH64 GH71 GH72 GH81 GH128 GH132
Chitin    AA15 CBM5 CBM18 GH18 GH19 GH20 GH46 GH75
Sucrose    GH32
end'''


parser = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('-i', '--input',
                    metavar='<cazy_overview.txt>',
                    required=True,
                    type=str,
                    help='run_dbcan2 result file: overview.txt')

args = parser.parse_args()

cazy_subgroup_dict = dict()
cazy_subgroup_definations = False
with open(sys.argv[0], 'rt') as infh:
    for line in infh:
        line = line.rstrip('\n')
        if line.startswith("'''cazymes subgroups"):
            cazy_subgroup_definations = True
            continue
        if line.startswith("end'''"):
            break
        if cazy_subgroup_definations:
            subgroup_lab, subgroup_str = line.split('    ')
            subgroup_lst = subgroup_str.split(' ')
            cazy_subgroup_dict[subgroup_lab] = subgroup_lst


def remove_duplicate_and_2(overview):
    '''
    remove record with only one tool support
    remove duplicate records in case of one protein with 2+ match cazy labels
    '''
    records_lst = []
    gene_id_lst = []
    with open(overview, 'rt') as infh:
        for line in infh:
            if line.startswith('Gene ID'):
                continue
            line_lst = line.rstrip('\n').split('\t')
            gene_id = line_lst[0]
            tool_support_n = int(line_lst[5])
            if tool_support_n >= 2 and gene_id not in gene_id_lst:
                gene_id_lst.append(gene_id)
                records_lst.append(line_lst)
    return records_lst


def cazy_6_group_stat(records_lst):
    '''stat AA, GH, CE, CBM, PL, GT
    '''
    cazymes_label_lst = []
    for record in records_lst:
        _, _, hmmer_p, ecami_p, diamond_p, _ = record
        if re.match(r'^[a-zA-Z]{2}.*',  hmmer_p):
            cazymes_label = hmmer_p.split('(')[0]

        elif re.match(r'^[a-zA-Z]{2}.*',  ecami_p):
            cazymes_label = ecami_p.split('(')[0]

        elif re.match(r'^[a-zA-Z]{2}.*',  diamond_p):
            cazymes_label = diamond_p.split('+')[0]
        else:
            sys.exit(f"Error: unknown label. {{'\t'.join(record)}}")
        cazymes_label_lst.append(cazymes_label)

    GH_lst = []
    GT_lst = []
    PL_lst = []
    CE_lst = []
    AA_lst = []
    CBM_lst = []

    for label in cazymes_label_lst:
        if label.startswith('GH'):
            GH_lst.append(label)
        if label.startswith('GT'):
            GT_lst.append(label)
        if label.startswith('PL'):
            PL_lst.append(label)
        if label.startswith('CE'):
            CE_lst.append(label)
        if label.startswith('AA'):
            AA_lst.append(label)
        if label.startswith('CBM'):
            CBM_lst.append(label)

    cazymes_6group_stat_lst = [len(GH_lst), len(GT_lst), len(
        PL_lst), len(CE_lst), len(AA_lst), len(CBM_lst)]
    if sum(cazymes_6group_stat_lst) != len(records_lst):
        sys.exit('Error: unknown error. please check code line 119')
    return cazymes_6group_stat_lst, cazymes_label_lst


def cazy_function_group_stat(cazymes_label_lst):
    '''subgroup cazymes into functional groups
    '''
    function_subgroup_count_dict = {}
    for subgroup_lab in cazy_subgroup_dict.keys():
        function_subgroup_count_dict[subgroup_lab] = 0

    for label in cazymes_label_lst:
        for subgroup_lab, subgroup_lst in cazy_subgroup_dict.items():
            if label in subgroup_lst:
                function_subgroup_count_dict[subgroup_lab] += 1

    function_subgroup_count_lst = list(function_subgroup_count_dict.values())
    return function_subgroup_count_lst


if __name__ == '__main__':
    records_lst = remove_duplicate_and_2(args.input)
    cazymes_count = len(records_lst)
    cazymes_6group_stat_lst, cazymes_label_lst = cazy_6_group_stat(records_lst)
    function_subgroup_count_lst = cazy_function_group_stat(cazymes_label_lst)
    header_line_lst = ['#Filename', 'CAZymes', 'GH', 'GT', 'PL', 'CE', 'AA', 'CBM',
                       'PCWDE', 'FCWDE', 'Cellulose', 'Hemicellulose', 'Lignin',
                       'Pectin', 'Peptidoglycan', 'Mannan', 'Glucan', 'Chitin', 'sucrose']
    print('\t'.join(header_line_lst), file=sys.stdout, flush=True)
    print(args.input, cazymes_count, '\t'.join(map(str, cazymes_6group_stat_lst)), '\t'.join(
        map(str, function_subgroup_count_lst)), sep='\t', file=sys.stdout, flush=True)
    sys.exit(0)
