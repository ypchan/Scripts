#!/usr/bin/env python3
'''
get_the_longest_transcripts_gff3.py -- only saved the longest transcripts in gff3 format

Date:  2021-04-10
Author: chenyanpeng1992@outlook.com 
Usage：
    get_the_longest_transcripts_gff3.py sorted.gff3 > longest_transcripts.gff3
    cat sorted.gff3 | get_the_longest_transcripts_gff3.py - > longest_transcripts.gff3
'''
import re
import sys
import fileinput
from collections import defaultdict

if len(sys.argv) == 1 or len(sys.argv) > 2):
    print(__doc__, file=sys.stderr)
    sys.exit(1)
if sys.argv[1] in ['-h', '--help', '-help']:
    print(__doc__, file=sys.stderr)
    sys.exit(1)

gene_dict = defaultdict(list)
longest_transcript_dict = defaultdict(str)
CDS_dict = defaultdict(list)

for line in fileinput.input(files=sys.argv[1]):
    if line.startswith("#"):
        continue
    
    line_lst = line.split("\t")
    if len(line_lst) <= 8:
        print('Error message: unknown line\n{line}', file=sys.stderr)
        sys.exit(1)
        continue
    
    if line_lst[2] == "transcript" or line_lst[2] == "mRNA":
        transcript_id = re.search(r'ID=(.*?)[;\n]',line_lst[8]).group(1)
        transcript_parent = re.search(r'Parent=(.*?)[;\n]',line_lst[8]).group(1)
        transcript_parent = transcript_parent.strip() # remove the 'r' and '\n'
        
        # if the parent of transcript is not in the gene_dict, create it rather than append
        if transcript_parent in gene_dict:
            gene_dict[transcript_parent].append(transcript_id)
        else:
            gene_dict[transcript_parent] = [transcript_id]
        transcript_pos_dict[transcript_id] = [line_lst[0],line_lst[3], line_lst[4], line_lst[6] ]
    
    # GFF must have CDS feature
    if line_lst[2] == 'CDS':
        CDS_length = int(line_lst[4]) - int(line_lst[3])
        CDS_parent = re.search(r'Parent=(.*?)[;\n]',line_lst[8]).group(1)
        CDS_parent = CDS_parent.strip() # strip the '\r' and '\n'
        CDS_dict[CDS_parent].append(CDS_length)

for gene, transcripts in gene_dict.items():
    tmp = 0
    for transcript in transcripts:
        transcript_len = sum(CDS_dict[transcript])
        if transcript_len > tmp:
            longest_transcript = transcript
            tmp = transcript_len
    longest_transcript_dict[gene] = longest_transcript

for line in fileinput.input(files=sys.argv[1]):
    line = line.rstrip()
    if line.startswith("#"):
        print(line)
        continue
    line_lst = line.split('\t')
    if line_lst[2] == 'gene':
        gene_id = re.search(r'ID=(.*?)[;\n]', line_lst[8]).group(1)
        if gene_id in longest_transcript_dict:
            print(line)
    
    if line_lst[2] in ['transcript', 'mRNA']:
        transcript_id = re.search(r'ID=(.*?)[;\n]', line_lst[8]).group(1)
        parent_gene_id = re.search(r'Parent=(.*?)[;\n]', line_lst[8]).group(1)
        if transcript_id in longest_transcript_dict.values():
            print(line)
    
    if line_lst[2] in ['exon', 'CDS']:
        parent_transcript_id = re.search(r'Parent=(.*?)[;\n]', line_lst[8]).group(1)
        if parent_transcript_id in longest_transcript_dict.values():
            print(line)