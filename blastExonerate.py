'''
blastExonerate -- parallel exonerate after blast

AUTHOR:
    chenyanpeng1992@outlook.com
DATE：
    2021-03-30
'''
import os
import sys
import gzip
import argparse
import subprocess


def parse_args():
    '''Parse command-line arguments

    Return:
        args (object) : args.<args>
    '''
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('i','input',
        metavar='<genome.fa>',
        type=str,
        help='input file in FASTA format')

    parser.add_argument('b', 'blastresult',
        type=str,
        metavar='<blastresult.m6.txt>',
        help='blast result in format 6')

    parser.add_argument('p', 'proteinevidence',
        type=str,
        metavar='<protein.fa>',
        help='protein dataset must be in FASTA format')
    
    parser.add_argument('f', 'flanklength',
        type=int,
        default = 5000,
        metavar='<int>',
        help='flankiing sequence length on both sides of target region')

    parser.add_argument('t', 'threads',
        type=int,
        default = 12,
        metavar='<int>',
        help='specify number of threads')
    
    parser.add_argument('o', 'output',
        type=str,
        metavar='<out.gff3>',
        help='output file in gff3 format')

    args = parser.parse_args()
    return args

def get_chr_map(genome):
    '''Abbreviate contig id
    '''
    chr_map_dict = {}
    chr_num = 0
    with open(genome) as fafh:
        for line in fafh:
            if line.startswith('>'):
                chr_num += 1
                ori_id = line.lstrip('>').rstrip('\n').split()[0]
                chr_map_dict[ori_id] = 'chr' + str(chr_num)
    return chr_map_dict

def read_pep_against_genome_2_dict(blastresult):
    '''Parse tblastn result to python3 dictionay
    '''
    blast_dict = {}
    with open(blastresult) as bfh:
        for line in bfh:
            query, contig_id, pident, length, mismatch, gapopen, qstart, qend, sstart, send, evalue, bitscore = line.split('\t')
            if query not in blast_dict:
                blast_dict[query] = {}
                if contig_id not in blast_dict[query]:
                    blast_dict[query][contig_id] = []
                if sstart > send:
                    blast_dict[query][contig_id].append((send, sstart))
                else:
                    blast_dict[query][contig_id].append((sstart, send))
    return blast_dict

def merge_interval_of_same_gene(blast_dict):
    '''Merge continuous interval belongings to same gene
    '''
    for query in blast_dict:
        for subject in blast_dict[query]:
            coord_lst = blast_dict[query][subject]
            if len(coord_lst) == 1:
                blast_dict[query] = [coord_lst[0][0], coord_lst[0][1]]
            else:
                coord_lst = sorted(coord_lst, key=lambda tp: tp[0])
                blast_dict[query] = coord_lst[coord_lst[0][0], coord_lst[-1][1]]
    return blast_dict

def run_exonerate(queryprot, targetnucl, softmask, wkdir):
    '''Run exonerate
    '''
    exonerate_out_filename = f'{queryprot}_{targetnucl}.gff2'
    cmd = f'exonerate --model protein2genome --softmasktarget {softmask} --percent 50 --showalignment no --showvulgar no {queryprot} {targetnucl} > {exonerate_out_filename} 2>{queryprot}_{targetnucl}.err'
    p = subprocess.run(cmd, shell=True, stderr=subprocess.STDOUT, cwd = wkdir)
    if p.returncode != 0:
        sys.exit(f'Error: failed call: [{cmd}]')
    return exonerate_out_filename

def get_sub_seq(genome, blast_dict, flanklength):
    '''Get corresponding sub-sequence of each protein
    '''





