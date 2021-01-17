#!/usr/bin/env python3
'''
calculateGenomeSize.py -- calculate the number of bases in genome(.fa|.fa.gz) file.

Author:
    chengyanpeng1992@outlook.com
Bugs: 
    Any bugs should be reported to the above E-mail.
Info:
    Scale units:
    1 kbp (kilo base pairs) = 1,000 bp (base pairs)
    1 Mbp (mega base pairs) = 1,000,000 bp
    1 Gbp (giga base pairs) = 1,000,000,000 bp
'''
import os
import sys
import gzip
import argparse
import pandas as pd

def parse_args():
    '''Parse command-line arguments.
    '''
    parser = argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('-i', '--input',
                        metavar='<in.fa[.gz]>',
                        required=True,
                        type=str,
                        nargs='+',
                        help='genome file(s) in FASTA format, or multi-fasta folder(s)')

    parser.add_argument('-s', '--scale_unit',
                        metavar='[K|M|G]',
                        choices=['K', 'M', 'G'],
                        type=str,
                        help='print sizes in human readable format,k,M,G')
    
    parser.add_argument('-n', '--ndecimal',
                        metavar='<int>',
                        type=int,
                        help='specify the number of decimal places (default: 2)')

    parser.add_argument('-f', '--field',
                        metavar='<int>',
                        type=int,
                        help='specify fasta id field to output (default: the first field). O means entire line except ">"')
    
    parser.add_argument('-c', '--contig',
                        action='store_true',
                        help='calucate the number of bases in contigs respectively')
    
    args = parser.parse_args()

    if args.field and not args.contig:
        _, scirpt_name = os.path.split(sys.argv[0])
        sys.exit(f'{scirpt_name}: error: option --field must with the option --contig')

    return args

def fa2dict(arg_input):
    '''Parse fasta files into dictionary.

    parameters:
        arg_input: input file(s) or folder(s)
    '''
    fa_len_dict = {}
    for arg in arg_input:
        if os.path.isfile(arg):
            _, filename = os.path.split(arg)
            fa_len_dict[filename] = {}
            
            fh = gzip.open(arg, 'rt') if arg.endswith('.gz') else open(arg, 'rt')
            for line in fh:
                line = line.rstrip('\n')
                if line.startswith('>'):
                    identifier = line.lstrip('>')
                    fa_len_dict[filename][identifier] = 0
                else:
                    fa_len_dict[filename][identifier] += len(line)
            fh.close()

        if os.path.isdir(arg):
            file_lst = os.listdir(arg)
            file_lst = [f'{arg}/{file}' for file in file_lst]
            for file in file_lst:
                _, filename = os.path.split(arg)
                fa_len_dict[filename] = {}
            
                fh = gzip.open(file, 'rt') if arg.endswith('.gz') else open(file, 'rt')
                for line in fh:
                    line = line.rstrip('\n')
                    if line.startswith('>'):
                        identifier = line.lstrip('>')
                        fa_len_dict[filename][identifier] = 0
                    else:
                        fa_len_dict[filename][identifier] += len(line)
                fh.close()
    return fa_len_dict

def genomelen_dataframe(fa_len_dict):
    '''Parse fa_len_dict into dataframe, and out genome and it's number of bases
    
    parameter:
        fa_len_dict: dictionary {genome_name:{identifier:length}...}
    '''
    genomic_len_dict = {}
    for genome_name in fa_len_dict:
        genomic_len_dict[genome_name] = 0
        for identifier in fa_len_dict[genome_name]:
            genomic_len_dict[genome_name] += fa_len_dict[genome_name][identifier]
    
    genomic_len_df = pd.DataFrame.from_dict(genomic_len_dict, orient='index', colums=['GenomeID', '#Base'])
    return genomic_len_df

def contiglen_dataframe(fa_len_dict):
    '''Parse fa_len_dict into dataframe, and out genome, contig, identifier and it's number of bases
    
    parameter:
        fa_len_dict: dictionary {genome_name:{identifier:length}...}
    '''
    contig_len_dict = {}
    for genome_name in fa_len_dict:
        for identifier in fa_len_dict[genome_name]:
            contig_len = fa_len_dict[genome_name][identifier]
            contig_len_dict[genome_name] = [identifier, contig_len]
    
    contig_len_df = pd.DataFrame.from_dict(contig_len_dict, orient='index', colums=['GenomeID', 'Identifier', '#Base'])
    return contig_len_df

def out_genomic_len(genomic_len_df, arg_scale, arg_ndecimal):
    '''Output genome length in two-column, tab-delimited table.
    
    parameter:
        genomic_len_df: two-column dataframe, genomename and genome_length
        arg_scale     : scale unit,[K|M|G]
        arg_ndecimal  : number of decimal places (default: 2)
    '''
    if arg_scale == 'K':
        divisor = 1000
    elif arg_scale == 'M':
        divisor = 1000000
    elif arg_scale == 'G':
        divisor = 1000000000
    else:
        divisor = 1
        arg_ndecimal = 0

    genomic_len_df['#Base'].map(lambda x: round(x / divisor, arg_ndecimal))
    genomic_len_df.to_csv(sys.stdout, sep='\t')

def out_contig_len(contig_len_df, arg_scale, arg_ndecimal):
    '''Output genome length in three-column, tab-delimited table.

    parameter:
        contig_len_df: three-column dataframe, genomename, identifier and genome_length
        arg_scale     : scale unit,[K|M|G]
        arg_ndecimal  : number of decimal places (default: 2)
    '''
    if arg_scale == 'K':
        divisor = 1000
    elif arg_scale == 'M':
        divisor = 1000000
    elif arg_scale == 'G':
        divisor = 1000000000
    else:
        divisor = 1
        arg_ndecimal = 0

    contig_len_df['#Base'].map(lambda x: round(x / divisor, arg_ndecimal))
    contig_len_df.to_csv(sys.stdout, sep='\t')

if __name__ == '__main__':
    args = parse_args()
    fa_len_dict = fa2dict(args.input)
    contig_len_df = contiglen_dataframe(fa_len_dict)
    if args.contig:
        out_contig_len(contig_len_df, args.scale, args.ndecimal)
        sys.exit(0)

    genome_len_df = genomelen_dataframe(fa_len_dict)
    out_genomic_len(genomic_len_df, args.scale, args.ndecimal)
    sys.exit(0)