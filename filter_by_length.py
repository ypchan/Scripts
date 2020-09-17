#!/usr/bin/env python3
'''
filter_by_length.py -- Filter multi-fasta file(s) by length.

DATE:
    2020-09-11
BUGS：
    Any bugs should be sent to chenyanpeng1992@outlook.com
'''

import os
import sys
import gzip
import argparse

def parse_args(argv):
    '''Parse command-line arguments.
    '''
    parser = argparse.ArgumentParser(description=__doc__)

	parser.add_argument('<fasta>',
		metavar='<fasta-file>',
		type=str,
		help='input fasta file')
	
	parser.add_argument('-l', '--length_threshold',
		type=int,
		help='set minimal length of the proteins')
 	
 	args = parser.parse_args()
 	return args

def 


def main():

if __name__ == '__main__':
    args = parse_args()

  sys.exit(main())
