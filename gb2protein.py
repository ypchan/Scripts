#!/usr/bin/env python3
'''
gb2protein.py -- get protein from gbk file

DATE: 2020-10-10
BUGS: Any bugs should be reported to yanpengch@qq.com
'''

import os
import re
import sys
import argparse
import fileinput

# DNA codons
DNA_Codons = {
    # 'M' = START, '*' = STOP
    "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "TGT": "C", "TGC": "C",
    "GAT": "D", "GAC": "D",
    "GAA": "E", "GAG": "E",
    "TTT": "F", "TTC": "F",
    "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
    "CAT": "H", "CAC": "H",
    "ATA": "I", "ATT": "I", "ATC": "I",
    "AAA": "K", "AAG": "K",
    "TTA": "L", "TTG": "L", "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
    "ATG": "M",
    "AAT": "N", "AAC": "N",
    "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "CAA": "Q", "CAG": "Q",
    "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R", "AGA": "R", "AGG": "R",
    "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S", "AGT": "S", "AGC": "S",
    "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
    "TGG": "W",
    "TAT": "Y", "TAC": "Y",
    "TAA": "*", "TAG": "*", "TGA": "*"
}

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('inputgbk',
                    type=str,
                    metavar='<inputgbk>',
                    help='input file in GBK format')
args = parser.parse_args()

def translate(DNAseq, init_pos=0):
    '''Translate a DNA sequence to an amino acid sequence
    '''
    # To avoid unwanted characters suach as whitespaces or newline signs
    DNAseq = DNAseq.strip('\n').strip().upper()
    AAseq = []
    for pos in range(init_pos, len(DNAseq), 3):
        codon = DNAseq[pos:pos+3]
        AAseq.append(DNA_Codons[codon])
    return ''.join(AAseq)

def complement(DNAseq):
    '''Get complementary sequence of DNAseq
    '''
    complement_dict = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    complementary_DNAseq = []
    for base in DNAseq.upper():
        if base not in complement_dict:
            sys.exit(f'[ERROR] Existing unknown character {base} in input DNA sequence')

        complementary_DNAseq.append(complement_dict[base])
    return ''.join(complementary_DNAseq)

def reverse(DNAseq):
    '''reverse given dna sequences
    '''
    return DNAseq[::-1]

if __name__ == '__main__':
    with fileinput.input(files=args.inputgbk) as fh:

        # Parse LOCUS block one by one
        for line in fh:
            if line.startswith('LOCUS'):
                locus_id = line.split()[1]
                DNAseq_lst = []
                #print()
                #print(locus_id, file=sys.stdout, flush=True)
                continue
            if line.startswith('     CDS'):
                interval_string = line.split()[1].strip()
                #print(interval_string, file=sys.stdout, flush=True)
                # skip the mRNA interval line
                interval_string_continue = 'yes'
                continue
            if re.findall(r' {21}[,.0-9]', line) and interval_string_continue == 'yes':
                #print(line)
                interval_string += line.strip()
                #print(interval_string, file=sys.stdout, flush=True)
                continue

            if line.startswith('ORIGIN'):
                #print(interval_string)
                interval_string_continue = 'no'
                if 'complement(join(' in interval_string:
                    strand = '-'
                    cds_interval_lst = interval_string.strip('complement(join(').strip('))').split(',')
                    cds_interval_lst = [interval.split('..') for interval in cds_interval_lst]
                    continue
                elif 'join' in interval_string:
                    strand = '+'
                    cds_interval_lst = interval_string.strip('join(').strip(')').split(',')
                    cds_interval_lst = [interval.split('..') for interval in cds_interval_lst]
                    continue
                elif 'complement(' in interval_string:
                    strand = '-'
                    cds_interval_lst = [interval_string.strip('complement(').strip(')').split('..')]
                    continue
                else:
                    strand = '+'
                    cds_interval_lst = [interval_string.split('..')]
                    continue

            if re.match(r'\s+[0-9]+ ', line):

                if not DNAseq_lst:
                    DNAseq_lst = [''.join(line.split()[1:]).replace(' ', '')]
                else:
                    DNAseq_lst.append(''.join(line.split()[1:]).replace(' ', ''))

            if line.startswith('//'):
                DNA_seq = ''.join(DNAseq_lst)
                cds_seq_lst = []
                #print(DNA_seq)
                #print(cds_interval_lst)
                # extract cds one interval by one interval
                for interval in cds_interval_lst:
                    start, end = interval
                    cds_seq_lst.append(DNA_seq[int(start)-1:int(end)])
                cds_seq = ''.join(cds_seq_lst)
                #print(cds_seq)

                if strand == '-':
                    cds_seq = reverse(complement(cds_seq))
                new_locus_id = locus_id.replace('_','__')
                print(f'>{new_locus_id} {locus_id}', file=sys.stdout, flush=True)
                AA_seq = translate(cds_seq)
                print(AA_seq, file=sys.stdout, flush=True)
                interval_string = ''
    sys.exit(0)