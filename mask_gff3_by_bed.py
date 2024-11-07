#!/usr/bin/env python3
'''
filter_gff3_by_bed.py -- filter gff3 according to bed file

DATE:
    2020-04-12
BUGS：
    Any bugs should be sent to chenyanpeng1992@outlook.com
'''

import os
import re
import sys
import gzip
import argparse
import fileinput
from collections import defaultdict

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-g', '--gff3',
                        required=True,
                        metavar='<in.gff3>',
                        type=str,
                        help='input file in gff3 format (.gz allowed)')

    parser.add_argument('-b', '--bed',
                        required=True,
                        type=str,
                        metavar='<in.bed>',
                        help='the 2rd input file in bed format (.gz allowed)')
    
    parser.add_argument('-o', '--out',
                        required=True,
                        type=str,
                        metavar='<out.gff3>',
                        help='output filename')

    parser.add_argument('-c', '--coverage_2_bed',
                       type=float,
                       default=0.5,
                       help='overlapping_region_length / bed_region_length')

    parser.add_argument('-C', '--coverage_2_gff3',
                       type=float,
                       default=0.5,
                       help='overlapping_region_length / gene_region_length')
    args = parser.parse_args()
    if args.coverage_2_bed and args.coverage_2_gff3:
        sys.exit('Error message: --coverage_2_bed is incompatible with --coverage_2_gff3')
    return args

def read_gff3_2_dict(gff3):
    '''
    ##gff-version 3
    ##sequence-region   ANPB02000012.1 10494 820974
    ##sequence-region   CM022975.1 15146 49009
    ...
    ANPB02000006.1  EVM     gene    9322    9480    .       +       .       ID=gene12234;Name=EVM prediction ANPB02000006.1.1
    ANPB02000006.1  EVM     mRNA    9322    9480    .       +       .       ID=mRNA12234;Parent=gene12234;Name=EVM prediction ANPB02000
    ANPB02000006.1  EVM     exon    9322    9480    .       +       .       ID=exon-30840;Parent=mRNA12234
    ANPB02000006.1  EVM     CDS     9322    9480    .       +       0       ID=cds-4787;Parent=mRNA12234
    ANPB02000006.1  EVM     gene    11856   15416   .       -       .       ID=gene12235;Name=EVM prediction ANPB02000006.1.2
    ANPB02000006.1  EVM     mRNA    11856   15416   .       -       .       ID=mRNA12235;Parent=gene12235;Name=EVM prediction ANPB02000
    ANPB02000006.1  EVM     exon    11856   12415   .       -       .       ID=exon-30841;Parent=mRNA12235
    ANPB02000006.1  EVM     exon    12486   15416   .       -       .       ID=exon-30842;Parent=mRNA12235
    ANPB02000006.1  EVM     CDS     11856   12415   .       -       0       ID=CDS7448;Parent=mRNA12235
    ANPB02000006.1  EVM     CDS     12486   15416   .       -       0       ID=CDS7448;Parent=mRNA12235
    '''
    gff3fh = gzip.open(gff3) if gff3.endswith('.gz') else open(gff3)
    
    gff3_gene_pos_strand_dict = defaultdict(list)
    gff3_contig_gene_dict = defaultdict(list)
    gff3_gene_mRNA_dict = defaultdict(list)
    gff3_mRNA_pos_strand_dict = defaultdict(list)
    gff3_mRNA_exon_dict = defaultdict(list)
    gff3_mRNA_CDS_dict = defaultdict(list)
    gff3_exon_pos_strand_dict = defaultdict(list)
    gff3_CDS_pos_strand_dict = defaultdict(list)

    for line in gff3fh:
        if line.startswith('#'):
            continue

        seqid, source, feature, start, end, score, strand, phase, attrs = line.split('\t')
        if feature == 'gene':
            geneid = re.search(r'ID=(.*?)[;\n]', attrs).group(1)
            if geneid in gff3_gene_pos_strand_dict:
                sys.exit(f'Error message: duplicate geneid {geneid}')
            gff3_gene_pos_strand_dict[geneid] = [seqid, start, end, strand]
            gff3_contig_gene_dict[seqid].append(geneid)
        if feature == 'mRNA':
            mRNAid = re.search(r'ID=(.*?)[;\n]', attrs).group(1)
            parent_geneid = re.search(r'Parent=(.*?)[;\n]', attrs).group(1)
            gff3_gene_mRNA_dict[geneid].append(mRNAid)
            gff3_mRNA_pos_strand_dict[mRNAid] = [seqid, start, end, strand]
        if feature == 'exon':
            exonid = re.search(r'ID=(.*?)[;\n]', attrs).group(1)
            parent_mRNAid = re.search(r'Parent=(.*?)[;\n]', attrs).group(1)
            gff3_mRNA_exon_dict[parent_mRNAid].append(exonid)
            gff3_exon_pos_strand_dict[mRNAid] = [seqid, start, end, strand]
        if feature == 'CDS':
            CDSid = re.search(r'ID=(.*?)[;\n]', attrs).group(1)
            parent_mRNAid = re.search(r'Parent=(.*?)[;\n]', attrs).group(1)
            gff3_mRNA_CDS_dict[parent_mRNAid].append(CDSid)
            gff3_CDS_pos_strand_dict[mRNAid] = [seqid, start, end, strand]
    gff3fh.close()
    return gff3_gene_pos_strand_dict, gff3_gene_mRNA_dict, gff3_mRNA_pos_strand_dict, gff3_mRNA_exon_dict, gff3_mRNA_CDS_dict, gff3_exon_pos_strand_dict, gff3_CDS_pos_strand_dict

def read_bed_2_dict(bedfile):
    '''Bed file can be generated using bedtools

    WEZL01001080.1  .       BED_feature     6582    7080    .       .       .       .
    WEZL01001080.1  .       BED_feature     7278    7336    .       .       .       .
    WEZL01001084.1  .       BED_feature     3398    3504    .       .       .       .
    WEZL01001085.1  .       BED_feature     5489    5530    .       .       .       .
    WEZL01001085.1  .       BED_feature     7881    7921    .       .       .       .
    WEZL01001085.1  .       BED_feature     14493   14572   .       .       .       .
    WEZL01001086.1  .       BED_feature     13050   13293   .       .       .       .
    WEZL01001087.1  .       BED_feature     5039    5209    .       .       .       .
    WEZL01001089.1  .       BED_feature     5892    6061    .       .       .       .
    WEZL01001091.1  .       BED_feature     330     381     .       .       .       .
    '''
    bedfh = gzip.open(bedfile) if bedfile.endswith('.gz') else open(bedfile)
    bed_dict = defaultdict(list)
    for line in bedfh:
        if line.startswith('#'):
            continue
        seqid, _, feature, start, end = line.split('\t')[:5]
        bed_dict[seqid].append((start, end))
    bedfh.close()
    return bed_dict

def remove_overlapping_region(gff3_contig_gene_dict, gene_pos_strand_dict, bed_dict, cover2bed, cover2gff3):
    for seqid, regions in bed_dict.items():
        for region in regions:
            region_start = region[0]
            region_end = region[1]
            region_length = int(region_end) - int(region_start) + 1
            for gene in gff3_contig_gene_dict[seqid]:
                _, gene_region_start, gene_region_end = gene_pos_strand_dict[gene][:3]
                gene_length = int(gene_region_end) - int(gene_region_start) + 1
                if int(gene_region_start) >= int(region_end) or int(gene_region_end) <= int(region_start):
                    continue
                if int(gene_region_start) < int(region_end) and int(gene_region_start) > int(region_start):
                    overlapping_region_length = int(region_end) - int(gene_region_start) += 1
                    if cover2bed and overlapping_region_length / region_length >= 0.5:
                        del gene_pos_strand_dict[gene]
                        continue
                    if cover2gff3 and overlapping_region_length / gene_length >= 0.5:
                        del gene_pos_strand_dict[gene]
                        continue
    seqids_with_genes = set([seqid_pos_strand[0] for gene,seqid_pos_strand in gene_pos_strand_dict.items()])
    return gene_pos_strand_dict, seqids_with_genes

if __name__ == '__main__':
    args = parse_args()
    gff3_gene_pos_strand_dict, gff3_gene_mRNA_dict, gff3_mRNA_pos_strand_dict, gff3_mRNA_exon_dict, gff3_mRNA_CDS_dict, gff3_exon_pos_strand_dict, gff3_CDS_pos_strand_dict = read_gff3_2_dict(args.gff3)
    bed_dict = read_bed_2_dict(args.bed)
    gene_pos_strand_dict, seqids_with_genes = remove_overlapping_region(gff3_contig_gene_dict, gene_pos_strand_dict, bed_dict, args.coverage_2_bed, args.coverage_2_gff3)
    gff3fh = gzip.open(gff3) if gff3.endswith('.gz') else open(gff3)
    
    outfh = open(args.out, 'wt')
    for line in gff3fh:
        if line.startswith('##sequence-region'):
            seq_id = line.split()[1]
            if seq_id in seqids_with_genes:
                outfh.write(line)
            continue
        if line.startswith('#'):
            outfh.write(line)
            continue
        seqid, source, feature, start, end, score, strand, phase, attrs = line.split('\t')
        if feature == 'gene':
            geneid = re.search(r'ID=(.*?)[;\n]', attrs).group(1)
            if geneid in gene_pos_strand_dict:
                outfh.write(line)
            continue
        if feature == 'mRNA':
            mRNAid = re.search(r'ID=(.*?)[;\n]', attrs).group(1)
            parent_geneid = re.search(r'Parent=(.*?)[;\n]', attrs).group(1)
            if parent_geneid in gene_pos_strand_dict:
                outfh.write(line)
            continue
         if feature
















