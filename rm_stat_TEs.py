#!/usr/bin/env python3
'''
rm_stat_TEs.py -- stat repeatmasker results of multiple result files.

Date: 2022-11-08
Bugs: any bugs should reported to yanpengch@qq.com
'''


import sys
import argparse
import pandas as pd

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('--rm_tbl_list',
                    required=True,
                    type=str,
                    help='repeatmasker result file list, one file per line')

parser.add_argument('--output',
                    type=str,
                    help='output filename')
args = parser.parse_args()


label_lst = ['Genome', 'SINES', 'Penelope', 'CRE/SLACS', 'L2/CR1/Rex', 'R1/LOA/Jockey',
             'R2/R4/NeSL', 'RTE/Bov-B', 'L1/CIN4', 'BEL/Pao', 'Ty1/Copia',
             'Gypsy/DIRS1', 'Retroviral', 'hobo-Activator', 'Tc1-IS630-Pogo',
             'En-Spm', 'MuDR-IS905', 'PiggyBac', 'Tourist/Harbinger',
             'Other', 'Rolling-circles', 'Unclassified:']


def parse_rm_tbl(tbl: str, class_dict: dict):
    '''
    Repeat Classes
    ==============
    Total Sequences: 74
    Total Length: 22071485 bp
    Class                  Count        bpMasked    %masked
    =====                  =====        ========     =======
    LTR                    --           --           --   
        Copia              8            5604         0.03% 
    Unknown                200          15477        0.07% 
                        ---------------------------------
        total interspersed 208          21081        0.10%

    Low_complexity         479          22704        0.10% 
    Satellite              15           2151         0.01% 
    Simple_repeat          3652         137864       0.62% 
    ---------------------------------------------------------
    Total                  4354         183800       0.83%
    '''
    item_base_dict = dict()
    out_line = False

    with open(tbl, 'rt') as infh:
        for line in infh:
            line = line.rstrip('\n')
            if line.startswith('Class '):
                out_line = True
                continue

            if '--------------' in line:
                continue

            if "=====" in line:
                continue

            if line.startswith('    total interspersed'):
                break

            if out_line:
                if not line.startswith(' '):
                    top_class = line.split()[0]
                    if top_class not in class_dict:
                        class_dict[top_class] = []

                if line.startswith('    ') or line.startswith('Unknown '):
                    line_lst = line.strip().split()
                    item = line_lst[0]
                    class_dict[top_class].append(item)
                    if len(line_lst) <= 1:
                        continue
                    num_base = line_lst[2]
                    item_base_dict[item] = num_base

    return item_base_dict, class_dict


def unify_all_rm_result(summary_dict: dict):
    '''
    No element record in rm result file, if the genome does not contain the element.
    In order to compare, we should confirm that each subdict includes same number of keys, key represent element name
    we do not know how many kinds of elements will be present in the comparative studies, 
    so we should summary the elements, and confirmt if the element is present or absent in some genomes. 
    '''
    element_lst = list()
    for _, subdict in summary_dict.items():
        element_lst.extend(list(subdict.keys()))

    element_lst = list(set(element_lst))

    update_summary_dict = dict()
    for file, subdict in summary_dict.items():
        for element in element_lst:
            if element not in subdict:
                subdict[element] = 0

        update_summary_dict[file] = subdict

    return update_summary_dict


if __name__ == "__main__":
    summary_dict = dict()
    class_dict = dict()

    with open(args.rm_tbl_list) as infh:
        for file in infh:
            file_name_with_path = file.rstrip('\n')
            item_base_dict, class_dict = parse_rm_tbl(
                file_name_with_path, class_dict)
            summary_dict[file_name_with_path] = item_base_dict

    update_summary_dict = unify_all_rm_result(summary_dict)
    df = pd.DataFrame.from_dict(update_summary_dict, orient='index')

    order_df_head_lst = []
    for top, lst in class_dict.items():
        print(top)
        print(set(lst))
        order_df_head_lst.extend(set(lst))
    df = df[order_df_head_lst]
    df.to_csv(args.output, sep='\t')
    sys.exit(0)
