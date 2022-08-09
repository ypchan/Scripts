#!/usr/bin/env python3
'''
parse_antismash_result.py -- summary antismash results

DATE: 2022-03-01
BUGS: yanpengch@qq.com
'''
import os
import sys
import argparse
import fileinput

parser = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 prog='parse_antismash_result.py')
parser.add_argument('input',
                    type=str,
                    metavar='antimash_result_path_list.txt',
                    help = 'list of antismash result')
args = parser.parse_args()

if __name__ == '__main__':
    gbk_lst = []
    with fileinput.input(args.input) as infh:
        for line in infh:
            gbk_lst.append(line.rstrip('\n'))

    all_antismash_result_dict = {}
    for gbk in gbk_lst:
        gbk_basename = os.path.basename(gbk)
        if gbk_basename in all_antismash_result_dict:
            sys.exit(f'Error: duplicate file {gbk}')
        all_antismash_result_dict[gbk_basename] = {}
        with open(gbk) as gbkfh:
            block = False
            for line in gbkfh:
                if line.startswith('     protocluster'):
                    block = True
                if line.startswith('     proto_core'):
                    block = False
                if block:
                    if line.startswith('                     /product='):
                        product = line.split('=')[1].strip("\n").lstrip('"').rstrip('"')
                        if product not in all_antismash_result_dict[gbk_basename]:
                            all_antismash_result_dict[gbk_basename][product] = 1
                        else:
                            all_antismash_result_dict[gbk_basename][product] += 1
                else:
                    continue
    product_lst = []
    for gbk_name, gbk_dict  in all_antismash_result_dict.items():
        product_lst.extend(gbk_dict.keys())

    product_lst = list(set(product_lst))
    product_lst_str = "\t".join(product_lst)
    print(f'gbk_name\t{product_lst_str}', file=sys.stdout, flush=True)
    for gbk_name, gbk_dict in all_antismash_result_dict.items():
        out_each_gbk_line_lst = [gbk_name]
        for product in product_lst:
            if product not in gbk_dict:
                out_each_gbk_line_lst.append(0)
            else:
                out_each_gbk_line_lst.append(gbk_dict[product])
        out_each_gbk_line_lst = [str(element) for element in out_each_gbk_line_lst]
        print("\t".join(out_each_gbk_line_lst), file=sys.stdout, flush=True)
    sys.exit(0)