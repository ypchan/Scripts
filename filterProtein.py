#!/usr/bin/env python3
'''
filterProtein.py -- filter protein(.fa|.fa.gz) file by length, and whether the start amino acid "M" exists.

Author:
    chengyanpeng1992@outlook.com
Bugs: 
    Any bugs should be reported to the above E-mail.
'''
import os
import sys
import gzip
import argparse

def parse_args():
    '''Parse command-line arguments.
    '''
    parser = argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('fasta',
                        metavar='<in.fa[.gz]>',
                        type=str,
                        help='proteinset file in FASTA format')

    parser.add_argument('-l', '--len_threshold',
                        default=50,
                        metavar='<int>',
                        type=int,
                        help='length threshold of protein')
    
    parser.add_argument('-s', '--start_aminoacid',
                        action='store_true',
                        help='filter by the start amino acid "M"')

    parser.add_argument('-out', '--field',
                        metavar='<in_pass.faa.gz>',
                        type=str,
                        help='filtered protein file name. default: in_pass.faa.gz')
    
    parser.add_argument('-f', '--failed_out',
                        metavar='<in_notpass.faa.gz>',
                        help='protein file that did not pass the filtration. default: in_notpass.faa.gz')
    
    parser.add_argument('-S', '--statistics',
                        metavar='<statistics.txt>',
                        help='output base statistics')
    
    parser.add_argument('-g', '--gzip',
                        action='store_true',
                        help='output file in .gz format')
    
    args = parser.parse_args()

    return args

class Proteinfaa:
    single_letter_amino_acid_code = 'GAVLIPFYWSTCMNQDEKRH'
    
    def __init__(self, infile, length=50, start=False):
        self.abspath = os.path.abspath(infile)
        self.suffix = os.path.splitext(infile)[1]
        self.filename = os.path.split(infile)[1].rstrip(self.suffix)
        self.checkstart = start
        self.checklength = length
    
    def fa_length(self):
        self.fadict = {}
        fh = gzip.open(self.abspath, 'rt') if self.suffix == '.gz' else open(self.abspath)
        for line in fh:
            line = line.rstrip('\n')

            if line.startswith('>'):
                # protein_des : protein description line
                protein_des = line.lstrip('>')
                self.fadict[protein_des] = []
            else:
                # valid the protein, whether the sequence only consists of 20 AA 
                for amino_acid in line.uppeer():
                    if amino_acid not in single_letter_amino_acid_code:
                        sys.exit(f'Error: unnatural amino acid: {amino_acid} in {protein_des}')
                
                self.fadict[protein_des].append(line)
        fh.close()
        self.fadict = {k:''.join(v) for k,v in self.fadict.items()}
        return self.fadict
    
    def filter_by_start(self):
        self.pass_start_lst = []
        self.notpass_start_lst = []
        
        if not self.checkstart:
            return self.pass_start_lst, self.notpass_start_lst

        for k,v in self.fadict.items():
            if v.upper().startswith('M'):
                self.pass_start_lst.append(k)
            else:
                self.notpass_start_lst.append(k)
        return self.pass_start_lst, self.notpass_start_lst
    
    def filter_by_length(self):
        self.pass_length_lst = []
        self.notpass_length_lst = []

        for k,v in self.fadict.items():
            if len(v) >= self.checklength:
                self.pass_length_lst.append(k)
            else:
                self.notpass_length_lst.append(k)
        return self.pass_length_lst, self.notpass_length_lst
    
    def filter_by_start_length(self):
        self.pass_start_length_lst = []
        self.pass_start_length_lst = list(set(self.pass_start_lst) & set(self.pass_length_lst))
        self.notpass_start_length_lst = list(set(self.fadict.keys()) - set(self.pass_start_length_lst))
        return self.pass_start_length_lst, self.notpass_start_length_lst

if __name__ == '__main__':
    args = parse_args()
    proteinfa = Proteinfaa(args.fasta, length=args.len_threshold, start=args.start_aminoacid)
    if args.out:
        proteinfa.filename = args.out
    
    ofh = gzip.open(args.out, 'w') if args.gzip else open(args.out, 'w')
    line_width = 70
    for passed_id in proteinfa.pass_start_length_lst:
        ofh.write(f'>{passed_id}\n')
        
        # formatting fasta output 
        sequence = proteinfa.fadict[passed_id]
        line_num = len(sequence) // line_width + 1 if len(sequence) % line_width != 0 else len(sequence) // line_width 
        line_lst = []
        n = 1
        while n < line_number:
            line_lst.append(sequence[line_width*(n-1):line_width*n]) 
            n += 1
        line_lst.append(sequence[line_width*n:])
        line_out = "\t".join(line_lst)
        ofh.write(f'{line_out}\n')
    ofh.close()

    if args.failed_out:
        if args.gzip:
            args.failed_out = args.failed_out.rstrip('.gz') + '.gz'
    
        failed_ofh = gzip.open(args.failed_out, 'w') if args.gzip else open(args.failed_out, 'w')
        
        for notpassed_id in proteinfa.notpass_start_length_lst:
            failed_ofh.write(f'>{notpassed_id}\n')
        
        # formatting fasta output 
            sequence = proteinfa.fadict[notpassed_id]
            line_num = len(sequence) // line_width + 1 if len(sequence) % line_width != 0 else len(sequence) // line_width 
            line_lst = []
            n = 1
            while n < line_number:
                line_lst.append(sequence[line_width*(n-1):line_width*n]) 
                n += 1
            line_lst.append(sequence[line_width*n:])
            line_out = "\t".join(line_lst)
            failed_ofh.write(f'{line_out}\n')
        failed_ofh.close()         