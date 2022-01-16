#!/usr/bin/env python3
'''
blastn_extract_marker_from_genome.py -- extract marker sequences(s) from genome(s) using NCBI blastn program

Date: 2021-05-28
Bugs: Bugs should be reported to chenyanpeng1992@outlook.com

Requirment:
    --markerdb blastdb based on maker sequences that should be filtered by CD-HIT
'''
import os
import sys
import gzip
import time
import argparse


# global variables
blastn = '/data/6190113/miniconda3/envs/maker/bin/blastn'

def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-d', '--markerdb',
        required=True,
        type=str,
        metavar='<markerdb>',
        help='blastdb based on maker sequences that should be filtered by CD-HIT')

    parser.add_argument('-g', '--genome',
        required=True,
        type=str,
        metavar='<genome.fa>',
        help='specify input genome fasta file')

    parser.add_argument('-o', '--out',
        type=str,
        required=True,
        metavar='<maker.fasta>',
        help='specify output filename')

    parser.add_argument('-f', '--flank_percent',
        type=float,
        default='0.1',
        metavar='<float>',
        help='the value can be calculated by (length of single side flanking sequence surrounding the HSP region) / subject_length')

    parser.add_argument('-t', '--threads',
        type=int,
        required=True,
        metavar='<int>',
        help='specify the number of CPUs to use')

    args = parser.parse_args()
    return args

def run_blastn(blastn, markerdb, genome, threads):
    '''Call blastn
    '''
    current_time = time.strftime("%H:%M:%S", time.gmtime())
    blastn_outname = os.path.basename(genome) + '.blastn'
    cmd = f'{blastn} -query {genome} -db {markerdb} -outfmt "6 std qlen slen" -out {blastn_outname} -num_threads {threads}'
    print(f'\n[ {current_time} ] Blastn was called as follows:\n    {cmd}', file=sys.stdout, flush=True)

    p = os.system(cmd)
    if p != 0:
        sys.exit(f'Error: failed to call blastn\n{cmd}')
    return blastn_outname

def best_marker_loc(blastn_outname):
    '''Determine the best marker location according score
    '''
    current_time = time.strftime("%H:%M:%S", time.gmtime())
    print(f'[ {current_time} ] Selecting the best hit according to the Score value', file=sys.stdout, flush=True)
    marker_dict = {}
    with open(blastn_outname) as blastnfh:
        for line in blastnfh:
            line_lst = line.rstrip('\n').split('\t')
            line_lst = [int(float(i)) if index == 11 else i for index,i in enumerate(line_lst)]
            subjectid = line_lst[1]
            marker_tag = subjectid.split('_')[0]
            if marker_tag not in marker_dict:
                marker_dict[marker_tag] = [line_lst]
            else:
                marker_dict[marker_tag].append(line_lst)

    best_hit_dict = {}
    for maker, blast_hits_lst in marker_dict.items():
        blast_hits_lst = sorted(blast_hits_lst, key=lambda blast_hits_lst: blast_hits_lst[11], reverse=True)
        best_hit_dict[maker] = blast_hits_lst[0]
    #print(best_hit_dict)
    return best_hit_dict

def fold_fasta(sequence, width=80):
    '''Convert a single long line fasta to multiple lines fasta
    '''
    start = 0
    line_length = len(sequence)
    line_lst = []
    while line_length - start >= width:
        line_lst.append(sequence[start:start + width])
        start += width

    line_lst.append(sequence[start:])
    return line_lst

def read_fasta2_dict(genome):
    '''Parse genome fasta into python3 dict
    '''
    current_time = time.strftime("%H:%M:%S", time.gmtime())
    print(f'[ {current_time} ] Parsing genome file into python3 dict', file=sys.stdout, flush=True)

    if genome.endswith('.gz'):
        genomefh = gzip.open(genome, 'rt')
    else:
        genomefh = open(genome, 'rt')

    genome_dict = {}
    for line in genomefh:
        line = line.rstrip('\n')
        if line.startswith('>'):
            contigid = line.split()[0].lstrip('>')
            genome_dict[contigid] = []
        else:
            genome_dict[contigid].append(line)
    genomefh.close()

    genome_dict = {k:''.join(v) for k,v in genome_dict.items()}
    return genome_dict

def extract_marker_sequences(genome_dict, best_hit_dict, flank_percent):
    '''extract marker sequences from genome sequence according corresponding blastn best hit
    '''
    current_time = time.strftime("%H:%M:%S", time.gmtime())
    print(f'[ {current_time} ] Extracting best hit region', file=sys.stdout, flush=True)

    target_marker_dict = {}
    for marker,best_hit_lst in best_hit_dict.items():
        contigid = best_hit_lst[0]
        identity = best_hit_lst[2]
        hsp_length = best_hit_lst[3]
        start = int(best_hit_lst[6])
        end = int(best_hit_lst[7])
        contig_length = int(best_hit_lst[12])
        subject_length = int(best_hit_lst[13])
        flanking_length = int(subject_length * flank_percent)
        #print(marker, f'flanking_length={flanking_length}')

        target_with_flank_left = start - flanking_length
        if target_with_flank_left < 0:
            print(f'    target - flank={target_with_flank_left} < 0, left boundary start at 1', file=sys.stdout, flush=True)
            target_with_flank_left = 1

        target_with_flank_right = end + flanking_length
        if target_with_flank_right > contig_length:
            print(f'    target + flank={target_with_flank_right} > contig_length={contig_length}, right boundary end at contig_length={contig_length}')
            target_with_flank_right = contig_length
        #print(f'target_with_flank_left={target_with_flank_left}, target_with_flank_right={target_with_flank_right}', file=sys.stdout, flush=True)

        target_length = target_with_flank_right - target_with_flank_left + 1
        target_seq = genome_dict[contigid][target_with_flank_left - 1:target_with_flank_right].upper()
        defline = f'>{marker} Ref={best_hit_lst[1]} RefLength={subject_length} HSP={hsp_length} Identity={identity} Length={target_length}'
        target_marker_dict[defline] = target_seq
    return target_marker_dict

if __name__ == '__main__':
    start_time = time.time()
    args = parse_args()

    blastn_outname = run_blastn(blastn, args.markerdb, args.genome, args.threads)
    best_hit_dict = best_marker_loc(blastn_outname)
    genome_dict = read_fasta2_dict(args.genome)
    target_marker_dict = extract_marker_sequences(genome_dict, best_hit_dict, args.flank_percent)

    with open(args.out, 'wt') as outfh:
        for target_marker, seq in target_marker_dict.items():
            outfh.write(f'{target_marker}\n')
            seq_lst = fold_fasta(seq)
            for line in seq_lst:
                outfh.write(f'{line}\n')

    current_time = time.strftime("%H:%M:%S", time.gmtime())
    print(f'[ {current_time} ] Output file: {os.path.abspath(args.out)}', file=sys.stdout, flush=True)
    finish_time = time.time()
    minutes, seconds = divmod(finish_time - start_time, 60)
    print(f'[ {current_time} ] Done', file=sys.stdout, flush=True)
    print(f'Elapsed time: {minutes:.0f} min {seconds:.0f} s\n', file=sys.stdout, flush=True)