#!/usr/bin/env python3

'''
ftk_extract_marker_from_genome.py -- extract barcode sequences(s) from the given genome using local blastn

Date: 2021-05-28
Bugs: Bugs should be reported to chenyanpeng1992@outlook.com

Requirment:
    -- subject FASTA based on barcode sequences that should be filtered by CD-HIT
'''


import os
import sys
import gzip
import time
import argparse


# global variables, please specify the absolute path of blastn
blastn = '/data/Tools/anaconda3/bin/blastn'


# parse command-line arguments
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('-s', '--subject',
                    required=True,
                    type=str,
                    help='blastn target subject based on maker sequences that should be filtered by CD-HIT')

parser.add_argument('-g', '--genome',
                    required=True,
                    type=str,
                    help='specify input genome fasta file')

parser.add_argument('-p', '--prefix',
                    type=str,
                    required=True,
                    help='prefix all output files')

parser.add_argument('-f', '--flanklength',
                    type=int,
                    default='100',
                    metavar='<int>',
                    help='length of flanking sequences surrounding the HSP region')


args = parser.parse_args()


def log(message: str):
    '''format log information
    '''
    ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f'{ctime} -- {message}', file=sys.stdout, flush=True)
    return


def run_blastn(blastn: str, subject: str, genome: str, prefix: str):
    '''blastn genome against subject barcode sequences
    '''
    blastn_out_name = prefix + '.blastn'
    cmd = f'{blastn} -query {genome} -subject {subject} -outfmt "6 std qlen slen" -out {blastn_out_name}'

    print('', file=sys.stdout, flush=True)
    log(f'-query {genome} -subject {subject} -out {blastn_out_name}')

    p = os.system(cmd)
    if p != 0:
        ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sys.exit(f'{ctime} -- Error: {cmd}')
    return blastn_out_name


def best_barcode_location(blastn_out_name, identity_threshold=60):
    '''Determine the best barcode location according score

    Rules:
        identity > 80%, the longer HSP the better
    '''
    log('Selecting the best hit according to the Score value')

    barcode_dict = {}
    with open(blastn_outname) as blastnfh:
        for line in blastnfh:
            line_lst = line.rstrip('\n').split('\t')

            subject_id = line_lst[1]
            barcode = subject_id.split('_')[0]
            identity = float(line_lst[2])

            # filter hist with identities less than 80
            if identity < identity_threshold:
                continue

            if barcode not in barcode_dict:
                barcode_dict[barcode] = [line_lst]
            else:
                barcode_dict[barcode].append(line_lst)

    best_hit_dict = {}

    for barcode, blast_hits_lst in barcode_dict.items():
        blast_hits_lst = sorted(
            blast_hits_lst, key=lambda blast_hits_lst: int(blast_hits_lst[3]), reverse=True)
        best_hit_dict[barcode] = blast_hits_lst[0]

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
    log('Parsing genome file into python3 dict')

    genome_basename = os.path.basename(genome)
    genome_dict = dict()
    genome_dict[genome_basename] = dict()

    if genome.endswith('.gz'):
        genomefh = gzip.open(genome, 'rt')
    else:
        genomefh = open(genome, 'rt')

    for line in genomefh:
        line = line.rstrip('\n')
        if line.startswith('>'):
            contigid = line.split()[0].lstrip('>')
            genome_dict[genome_basename][contigid] = []
        else:
            genome_dict[genome_basename][contigid].append(line)
    genomefh.close()

    new_genome_dict = dict()
    for filename, sub_genome_dict in genome_dict.items():
        new_genome_dict[filename] = dict()
        for seq_id, seq_lst in sub_genome_dict.items():
            new_genome_dict[filename][seq_id] = ''.join(seq_lst)

    return new_genome_dict


def extract_marker_sequences(new_genome_dict, best_hit_dict, flank_length):
    '''extract marker sequences from genome sequence according corresponding blastn best hit
    '''
    log('Extracting best hit region')

    target_barcode_dict = {}
    for barcode, best_hit_lst in best_hit_dict.items():
        contig_id = best_hit_lst[0]
        identity = best_hit_lst[2]
        hsp_length = best_hit_lst[3]
        start = int(best_hit_lst[6])
        end = int(best_hit_lst[7])
        contig_length = int(best_hit_lst[12])
        subject_length = int(best_hit_lst[13])
        flanking_length = int(flank_length)
        if flanking_length > 1000:
            flanking_length = 1000
        #print(marker, f'flanking_length={flanking_length}')

        target_with_flank_left = start - flanking_length
        if target_with_flank_left < 0:
            print(
                f'                       target - flank={target_with_flank_left} < 0, left boundary start at 1')
            target_with_flank_left = 1

        target_with_flank_right = end + flanking_length
        if target_with_flank_right > contig_length:
            print(
                f'                       target + flank={target_with_flank_right} > contig_length={contig_length}, right boundary end at contig_length={contig_length}')
            target_with_flank_right = contig_length
        #print(f'target_with_flank_left={target_with_flank_left}, target_with_flank_right={target_with_flank_right}', file=sys.stdout, flush=True)

        target_length = target_with_flank_right - target_with_flank_left + 1
        filename = list(new_genome_dict.keys())[0]
        target_seq = genome_dict[filename][contig_id][target_with_flank_left -
                                                      1:target_with_flank_right].upper()
        defline = f'>{barcode} Ref={best_hit_lst[1]} RefLength={subject_length} HSP={hsp_length} Identity={identity} Length={target_length} file={filename}'
        target_barcode_dict[defline] = target_seq
    return target_barcode_dict


if __name__ == '__main__':
    start_time = time.time()

    blastn_outname = run_blastn(
        blastn, args.subject, args.genome, args.prefix)
    best_hit_dict = best_barcode_location(blastn_outname)
    genome_dict = read_fasta2_dict(args.genome)
    target_barcode_dict = extract_marker_sequences(
        genome_dict, best_hit_dict, args.flanklength)

    with open(args.prefix + '_barcode.fna', 'wt') as outfh:
        for target_marker, seq in target_barcode_dict.items():
            outfh.write(f'{target_marker}\n')
            seq_lst = fold_fasta(seq)
            for line in seq_lst:
                outfh.write(f'{line}\n')

    current_time = time.strftime("%H:%M:%S", time.gmtime())

    finish_time = time.time()
    minutes, seconds = divmod(finish_time - start_time, 60)

    log(f'Done. Elapsed time: {minutes:.0f} min {seconds:.0f} s\n')
    sys.exit(0)
