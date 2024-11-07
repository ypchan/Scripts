#!/usr/bin/env python3

'''
ftk_extract_barcode_from_genome.py -- extract barcode sequences(s) from the given genome using local blastn

Date: 2021-05-28
Bugs: Bugs should be reported to chenyanpeng1992@outlook.com

Requirment:
    -- bait: multiple FASTA based on barcode sequences that should be filtered by CD-HIT
'''


import os
import sys
import time
import argparse


# global variables, please specify the absolute path of blastn
blastn = '/data/Tools/anaconda3/bin/blastn'


# parse command-line arguments
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('-b', '--bait',
                    required=True,
                    type=str,
                    help='blastn target subject based on maker sequences that should be filtered by CD-HIT')

parser.add_argument('-g', '--genome',
                    required=True,
                    type=str,
                    nargs='+',
                    help='specify input genome fasta file')

parser.add_argument('-o', '--outdir',
                    type=str,
                    required=True,
                    help='prefix all output files')

parser.add_argument('-f', '--flanklength',
                    type=int,
                    default='100',
                    metavar='<int>',
                    help='length of flanking sequences surrounding the HSP region')


args = parser.parse_args()


def run_blastn(args_bait: str, args_genome: str, args_outdir: str):
    '''blastn genome against subject barcode sequences
    '''
    c_time = time.strftime("%Y-%b-%d %H:%M:%S", time.gmtime())
    if os.path.exists(args_outdir):
        print(f'{c_time} -- Error: output folder {args_outdir} already exists.', file=sys.stdout, flush=True)
        sys.exit(f'{c_time} -- Exit.')
    
    blastn_out_lst = []
    for genome in args_genome:
        genome_basename = os.path.basename(genome)
        blastn_out_name = genome_basename + '.blastn'
        cmd = f'{blastn} -query {genome} -subject {args_bait} -outfmt "6 std qlen slen" -out {blastn_out_name}'
        c_time = time.strftime("%Y-%b-%d %H:%M:%S", time.gmtime())
        print(f'{c_time} -- -query {genome} -bait {args_bait}', file=sys.stdout, flush=True)
        p = os.system(cmd)
        if p != 0:
            sys.exit(f'{c_time} -- failed.')
        blastn_out_lst.append(genome_basename)
    return blastn_out_lst


def best_barcode_location(blastn_out_lst, identity_threshold=60):
    '''Determine the best barcode location according score

    Rules:
        identity > 80%, the longer HSP the better
    '''
    c_time = time.strftime("%Y-%b-%d %H:%M:%S", time.gmtime())
    print(f'{c_time} -- Selecting the best hit according to the Score value.', file=sys.stdout, flush=True)

    barcode_dict = {}
    for genome_basename in blastn_out_lst:
        barcode_dict[genome_basename] = []
        with open(genome_basename + '.blastn') as blastnfh:
            for line in blastnfh:
                line_lst = line.rstrip('\n').split('\t')

                subject_id = line_lst[1]
                barcode = subject_id.split('_')[0]
                identity = float(line_lst[2])

                # filter hist with identities less than 80
                if identity < identity_threshold:
                    continue

                if barcode not in barcode_dict:
                    barcode_dict[genome_basename][barcode] = [line_lst]
                else:
                    barcode_dict[genome_basename][barcode].append(line_lst)

    best_hit_dict = {}

    for genome_basename in barcode_dict:
        for barcode, blast_hits_lst in barcode_dict.items():
            blast_hits_lst = sorted(
                blast_hits_lst, key=lambda blast_hits_lst: int(blast_hits_lst[3]), reverse=True)
            best_hit_dict[genome_basename][barcode] = blast_hits_lst[0]

    return best_hit_dict


def read_fasta2_dict(args_genome):
    '''Parse genome fasta into python3 dict
    '''
    genome_dict = dict()
    for genome in args_genome:
        genome_basename = os.path.basename(genome)
        genome_dict[genome_basename] = dict()

        with open(genome, 'rt') as genomefh:
            for line in genomefh:
                line = line.rstrip('\n')
                if line.startswith('>'):
                    contigid = line.split()[0].lstrip('>')
                    genome_dict[genome_basename][contigid] = []
                else:
                    genome_dict[genome_basename][contigid].append(line)
    
    new_genome_dict = {}
    for genome_basename,subgenome_dict in genome_dict.items():
        new_genome_dict[genome_basename] = {}
        for k,v in subgenome_dict.items():
            new_genome_dict[genome_basename][k] = ''.join(v)
    return new_genome_dict

def extract_barcode_sequences(new_genome_dict, best_hit_dict, flank_length):
    '''extract barcode sequences from genome sequence according corresponding blastn best hit
    '''
    c_time = time.strftime("%Y-%b-%d %H:%M:%S", time.gmtime())
    print(f'{c_time} -- extract best hit region.', file=sys.stdout, flush=True)

    target_barcode_dict = {}
    for genome_basename, hit_dict in best_hit_dict.items():
        for barcode, hit_lst in hit_dict.items():
            contig_id = hit_lst[0]
            identity = hit_lst[2]
            hsp_length = hit_lst[3]
            start = int(hit_lst[6])
            end = int(hit_lst[7])
            contig_length = int(hit_lst[12])
            subject_length = int(hit_lst[13])
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
            
            target_seq = new_genome_dict[genome_basename][contig_id][target_with_flank_left -
                                                        1:target_with_flank_right].upper()
            defline = f'>{barcode} Ref={hit_lst[1]} RefLength={subject_length} HSP={hsp_length} Identity={identity} Length={target_length} File={genome_basename}'
            target_barcode_dict[defline] = target_seq
    return target_barcode_dict


if __name__ == '__main__':
    blastn_out_lst = run_blastn(args.bait, args.genome, args.outdir)
    best_barcode_location(blastn_out_lst, identity_threshold=60)
    best_hit_dict = best_barcode_location(blastn_out_lst)

    new_genome_dict = read_fasta2_dict(args.genome)
    target_barcode_dict = extract_barcode_sequences(
        new_genome_dict, best_hit_dict, args.flanklength)

    for defline, sequence in target_barcode_dict.items():
        defline_lst = defline.split()
        barcode_label = defline_lst[0].lstrip('>')
        genome_label = ''.join(defline_lst[-1].lstrip('File=').rstrip('\n').split('.')[:-1])
        outfile = f'{args.outdir}/{barcode_label}_{genome_label}.fasta'
        with open(outfile) as outfh:
            outfh.write(f'>{genome_label}\n'{sequence}\n)
    sys.exit(0)
