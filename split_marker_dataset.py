#!/usr/bin/env python
'''
DATE: 2022-01-26
BUGS: Any bugs should reported to yanpengch@qq.com
'''
import os
import sys
import fileinput

with fileinput.input(files=sys.argv[1]) as fh:
    for line in fh:
        filename= line.rstrip('\n')
        with open(filename) in fafh:
            for line in fafh:
                line = line.rstrip('\n')
                if line.startswith('>'):
                    faid_file, marker_file = line.split('__')
                    marker_file_name = marker_file + 'splits.fna'
                    if os.path.exists(marker_file_name):
                        with open(marker_file_name, 'w+') as ofh:
                            ofh.write(faid_file + '\n')
                    else:
                        with open(marker_file_name, 'w') as ofh:
                            ofh.write(faid_file + '\n')
                else:
                    try:
                        with open(marker_file_name, 'w+') as ofh:
                            ofh.write(line + '\n')
                    except NameError:
                        print(line, file=sys.stdout, flush=True)
                        sys.exit(1)