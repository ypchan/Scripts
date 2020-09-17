#!/usr/bin/env python
'''
    abspath.py -- print absolute path of input file(s) or directories
DATE:
    2020-09-12
BUGS:
    Any bugs should be sent to chenyanpeng1992@outlook.com
    
'''
from __future__ import print_function
import os
import sys
for entry in sys.argv[1:]:
     print(os.path.abspath(entry))