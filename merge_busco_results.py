#!/usr/bin/env python3
'''
merge_busco_results.py -- merge multiple busco result files into a table

Date:
    2020-04-14
Bugs：
    Any bugs should be reported to chenyanpeng1992@outlook.com
'''
import re
import os
import sys
import gzip
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-f', '--file_list', type=str, metavar='<txt>', help='busco result file paths are listed in <txt>')
    parser.add_argument('-d', '--directory', type=str, metavar='<dir>', help='busco result files in <dir>')
    args = parser.parse_args()

    if not any([args.file_list, args.directory]):
        sys.exit('Error mesage: --file_list or --directory is needed')
    if all([args.file_list, args.directory]):
        sys.exit('Error message: --file_list is incompatible with --directory')
    return args

def parse_busco_result_2_lst(busco_result_file):
    '''BUSCO output:
    # BUSCO version is: 4.1.4
    # The lineage dataset is: ascomycota_odb10 (Creation date: 2020-09-10, number of species: 365, number of BUSCOs: 1706)
    # Summarized benchmarking in BUSCO notation for file SRR10394974_contigs_200.faa
    # BUSCO was run in mode: proteins

            ***** Results: *****

            C:97.9%[S:97.6%,D:0.3%],F:0.7%,M:1.4%,n:1706
            1670    Complete BUSCOs (C)
            1665    Complete and single-copy BUSCOs (S)
            5       Complete and duplicated BUSCOs (D)
            12      Fragmented BUSCOs (F)
            24      Missing BUSCOs (M)
            1706    Total BUSCO groups searched
    '''
    speciesid = os.path.basename(busco_result_file)
    with open(busco_result_file) as buscofh:
        statistic_value_lst = [speciesid]
        for line in buscofh:
            line = line.strip()
            if line.startswith('#') or line.startswith('**'):
                continue
            if not line:
                continue
            if line.startswith('C:'):
                index_lst = [1,3,5,8,10, 12]
                statistic_value_lst += [re.split(r'[:\[\],]', line)[pos] for pos in index_lst]
                continue
            statistic_value_lst.append(line.split()[0])
    return statistic_value_lst

if __name__ == '__main__':
    args = parse_args()
    head_lst = ['SpeciesID', 'C', 'S', 'D', 'F', 'M', 'n', 'Complete BUSCOS (C)', 'Complete and single-copy BUSCOs (S)', 'Complete and duplicated BUSCOs (D)', 'Fragemented BUSCOs (F)', 'Missing BUSCOs (M)', 'Total BUSCO groups searched']
    print('\t'.join(head_lst))
    if args.file_list:
        with open(args.file_list) as filefh:
            file_lst = filefh.readlines()
        file_lst = [file.rstrip('\n') for file in file_lst]

        for file in file_lst:
            statistic_value_lst = parse_busco_result_2_lst(file)
            print('\t'.join(statistic_value_lst))