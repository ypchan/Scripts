#!/usr/bin/env python
'''
abspath.py -- print absolute path of input file(s) or directories

USAGE:
    abspath.py file1 file2 dir1 dir2 ...
DATE:
    2020-09-12
BUGS:
    Any bugs should be sent to chenyanpeng1992@outlook.com 
'''
import os
import sys

if sys.version_info[0] != 3:
    sys.exit('Error: please specify Python3 as interpreter')

if len(sys.argv) <= 1:
    print(__doc__, file=sys.stdout, flush=True)
    sys.exit(1)

help_lst = ['-h', '--h', '-help', '--help', '-?']
if sys.argv[1] in help_lst:
    print(__doc__, file=sys.stdout, flush=True)
    sys.exit(1)

for entry in sys.argv[1:]:
     print(os.path.abspath(entry), file=sys.stdout, flush=True)
     sys.exit(0)