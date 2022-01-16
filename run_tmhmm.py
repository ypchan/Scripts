#!/usr/bin/env python3
'''
run_tmhmm -- call tmhmm and parse its result for downstream analysis.

Date: 2021-05-26
Bugs: Any bugs should be reported to chenyanpeng1992@outlook.com
'''
import os
import sys
import argparse
import subprocess

# Specify the dependent files path
decodeanhmm="/home/data/vip21/biosoft/tmhmm/tmhmm-2.0c/bin/decodeanhmm.Linux_x86_64"
model="/home/data/vip21/biosoft/tmhmm/tmhmm-2.0c/lib/TMHMM2.0.model"
options="/home/data/vip21/biosoft/tmhmm/tmhmm-2.0c/lib/TMHMM2.0.options"


parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('fasta',
                    metavar='prot.fasta',
                    help='input file in FASTA format')

args = parser.parse_args()


cmd = f'{decodeanhmm} {model} -f {options} {args.fasta}'

p = subprocess.Open(cmd, shell=True, stdout=PIPE, text=True)
if p.returncode != 0:
    sys.exit(f'Error message: failed to call\n{cmd}')

for line in p.stdout.readlines():





