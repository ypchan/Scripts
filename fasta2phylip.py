#!/usr/bin/env python3
'''
fasta2phylip.py -- convert FASTA format alignment file to phylip format

DATE: 2021-02-05
BUGS: Any bugs should reported to 764022822@qq.com
USAGE:
    fasta2phylip.py alignment.fasta > alignment.phylip
'''

import sys
from Bio import AlignIO

if len(sys.argv) != 2 or '-h' in sys.argv or '--h' in sys.argv or '--help' in sys.argv or '-help' in sys.argv:
    print(__doc__, file=sys.stderr, flush=True)
    sys.exit(1)

records = AlignIO.parse(sys.argv[1], "fasta")
AlignIO.write(records, sys.stdout, "phylip-sequential")
