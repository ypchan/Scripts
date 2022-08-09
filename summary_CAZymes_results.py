#!/usr/bin/env python3
'''
summary_CAZymes_results.py -- summary run_dbcan results

DATE: 2022-03-03
BUGS: yanpengch@qq.com
'''
import os
import re
import sys
import argparse
import fileinput

parser = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 prog='parse_CAZymes_result.py')
parser.add_argument('input',
                    type=str,
                    metavar='run_dbcan results',
                    help = 'list of CAZymes result')
args = parser.parse_args()

if __name__ == '__main__':
    tsv_lst = []
    with fileinput.input(args.input) as infh:
        for line in infh:
            tsv_lst.append(line.rstrip('\n'))

    all_CAZymes_result_dict = {}
    for tsv_path in tsv_lst:
        # run_dbcan2 output： outdir/hmmer.out, so the last two dield is identifier
        tsv_basename = tsv_path.split('/')[-2]
        if tsv_basename in all_CAZymes_result_dict:
            sys.exit(f'Error: duplicate file {tsv_path}')
        
        all_CAZymes_result_dict[tsv_basename] = {}
        with open(tsv_path) as tsvfh:
            for line in tsvfh:
                if line.startswith('HMM Profile'):
                    continue
                cazy_class = re.sub(r'[0-9_]', '', line.split()[1])
                if cazy_class not in all_CAZymes_result_dict[tsv_basename]:
                    all_CAZymes_result_dict[tsv_basename] = 1
                else:
                    all_CAZymes_result_dict[tsv_basename] += 1
    product_lst = []
    for tsv_name, tsv_dict  in all_CAZymes_result_dict.items():
        product_lst.extend(tsv_dict.keys())
    product_lst = list(set(product_lst))
    
    product_lst_str = "\t".join(product_lst)
    print(f'tsv_name\t{product_lst_str}', file=sys.stdout, flush=True)
    for tsv_name, tsv_dict in all_CAZymes_result_dict.items():
        out_each_tsv_line_lst = [tsv_name]
        for product in product_lst:
            if product not in tsv_dict:
                out_each_tsv_line_lst.append(0)
            else:
                out_each_tsv_line_lst.append(tsv_dict[product])
        out_each_tsv_line_lst = [str(element) for element in out_each_tsv_line_lst]
        print("\t".join(out_each_tsv_line_lst), file=sys.stdout, flush=True)
    sys.exit(0)