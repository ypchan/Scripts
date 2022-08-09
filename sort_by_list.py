#!/usr/bin/env python3
'''
sort_by_list.py -- sort a table by given list

DATE: 2022-02-22
BUGS: Any bugs should be reported to 764022822@outlook.com
'''
import os
import sys
import argparse
import fileinput

parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('order_lst',
    type=str,
    help='order list. Stdin allowed')

parser.add_argument('table',
    type=str,
    help='table need to be sorted')

parser.add_argument('table_column',
    type=int,
    help='specify the column used for sorting')

args = parser.parse_args()

if __name__ == '__main__':
    with fileinput.input(args.order_lst) as fh:
        order_lst_str = fh.read()
        order_lst = order_lst_str.splitlines()

    table_dict = {}
    n_rows = 0
    with open(args.table) as fh:
        for line in fh:
            n_rows += 1
            line = line.rstrip('\n')
            line_lst = line.split('\t')
            sorted_column = line_lst[args.table_column - 1]
            table_dict[sorted_column] = line

    for index in order_lst:
        print(table_dict[index], file=sys.stdout, flush=True)

    if n_rows != len(order_lst):
        print('---------------------------------',file=sys.stderr, flush=True)
        print('Length of order llist is not equal to rows in table', file=sys.stderr, flush=True)
        sys.exit(0)
