#!/usr/bin/env python3
'''
filter_gb_by_LOCUS_id.py -- filter GBK file by given LOCUS is list

DATE: 2022-1-16
BUGS: Any bugs should be reported to yanpengch@qq.com
'''
import sys

id_lst = []
with open(sys.argv[2]) as idfh:
    for line in idfh:
        id_lst.append(line.rstrip('\n'))

with open(sys.argv[1]) as gbkfh:
    for line in gbkfh:
        if line.startswith('LOCUS'):
            locus_id = line.split()[1]
            if locus_id in id_lst:
                skip = 1
                continue
            else:
                skip = 0

        if line.startswith('//'):
            if not skip:
                print(line, end='')
            skip = 0

            continue
        if skip:
            continue
        else:
            print(line, end='')
sys.exit(0)
