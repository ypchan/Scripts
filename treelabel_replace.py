#!/usr/bin/env python3
import sys

map_dict = dict()
with open(sys.argv[1], 'rt') as infh:
    for line in infh:
        line_lst = line.rstrip('\n').split()
        map_dict[line_lst[0]] = line_lst[1]

with open(sys.argv[2], 'rt') as infh:
    tree = infh.readline()

for short_label, long_label in map_dict.items():
    tree = tree.replace(short_label,long_label)

print(tree, file=sys.stdout, flush=True)
sys.exit(0)
