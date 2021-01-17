#!/usr/bin/env python3
'''
longest_transcripts.py -- extract the longest trascripts from de novo trinity assembly

Author:
    chengyanpeng1992@outlook.com
Date: 
    December 12 2020, created
    January 09 2021,  1st updates
'''
import sys
import gzip
import argparse

def parse_args():
    '''
    Parse command-line arguments

    Parameter
    ---------
    NULL

    Return
    ------
    NULL
    '''
    parser = argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('input',
                        metavar='<input.fna>',
                        type=str,
                        help='input file must be in FASTA format and generated Trinity de novo assembly')
    
    parser.add_argument('output',
                        metavar='<out_longest.fna>',
                        type=str,
                        help='output file in FASTA format, if suffix is .gz, output file in gzipped format')   
               
    args = parser.parse_args()
    return args

def get_longest_transcripts(input_file):
    '''
    Get the longest transcript from the Trinity de novo assembly result

    Parameter
    ---------
    input_file : str
        Trinity de novo assembly result in FASTA format

    Return
    ------
    transcripts_dict : dict
        python 3 dictionary, keys represent transcript ids, values represent sequences.

    longest_transcripts_lst : list
        a list consists of the longest transcript ids
    '''
    trinity_dict = {}
    transcripts_dict = {}
    longest_transcripts_lst = []
    
    fh = gzip.open(arg_input, 'rt') if arg_input.endswith('.gz') else open(arg_input, 'rt')
    for line in fh:
        if line.startswith('>'):
            line_lst = line.strip('>').split()[:2]
            transcript_id = line_lst[0]
            transcripts_dict[transcript_id] = []

            gene_transcript, transcript_len = line_lst
            gene_id = "_".join(gene_transcript.split('_')[0:4])
            isoform_id = gene_transcript.split('_')[4]
            transcript_len = int(transcript_len.lstrip('len='))
            
            if gene_id not in trinity_dict:
                trinity_dict[gene_id] = {}
            
            trinity_dict[gene_id][isoform_id] = transcript_len
        else:
            transcripts_dict[transcript_id].append(line)
    
    for gene_id in trinity_dict:
        trinity_dict[gene_id] = sorted(trinity_dict[gene_id].items(), key=lambda x:x[1])
        longest_transcript_id = gene_id + '_' + trinity_dict[gene_id][0][0]
        longest_transcripts_lst.append(longest_transcript_id)
    fh.close()
    return transcripts_dict, longest_transcripts_lst

def output_longest_transcrpts(transcripts_dict, longest_transcripts_lst, outputfile):
    '''
    Output the longest transcripts in FASTA format

    Parameter
    ---------
    transcripts_dict : dict
        python 3 dictionary, keys represent transcript ids, values represent sequences.

    longest_transcripts_lst : list
        a list consists of the longest transcript ids
    
    outputfile : str
        output file name. if it is suffixed with '.gz', outputfile will be in gzipped fasta file
    
    Return
    ------
    NULL
    '''
    ofh = gzip.open(args.output, 'wt') if args.output.endswith('.gz') else open(args.output, 'wt')
    for longest_transcript_id in longest_transcripts_lst:
        seq_lst = transcripts_dict[longest_transcript_id]
        seq = ''.join(seq_lst)
        ofh.write(f'>{longest_transcript_id}\n')
        ofh.write(seq)
    ofh.close()

if __name__ == '__main__':
    args = parse_args()
    transcripts_dict, longest_transcripts_lst = get_longest_transcripts(args.input)
    output_longest_transcrpts(transcripts_dict, longest_transcripts_lst, args.output)