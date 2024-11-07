#!/usr/bin/env python3
'''
mycopshere_outline_2_table.py -- parse taxonomic scheme into table for other use.
Author: yanpengch@qq.com
DATE: 2023-01-16
'''

import sys

with open(sys.argv[1], 'rt') as infh:
    for line in infh:
        line = line.rstrip('\n')
