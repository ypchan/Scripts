#!/usr/bin/env python3

import os
import sys
import argparse
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('matrixfile',
        metavar='<matrixfile>',
        type=str,
        help='singlecopy orthogroups matrix in txt format')

    parser.add_argument('proteinfilepathmap',
        type=str,
        metavar='<filepathmaplist>',
        help='protein file list corresponding to species')
    parser.add_argument('-o', '--outdir',
        type=str,
        required=True,
        metavar='<outdir>',
        help='output directory')
    args = parser.parse_args()
    return args

def get_proteinfile_map(proteinfilemap):
    '''Get protein files list
    '''
    mapdict = {}
    with open(proteinfilemap) as filelistfh:
        for line in filelistfh:
            genomeid, proteinsetpath = line.rstrip('\n').split('\t')
            mapdict[genomeid] = proteinsetpath
    return mapdict

def fasta2dict(fastafile):
    '''parse fasta file into python3 dictionary
    '''
    fadict = {}
    with open(fastafile) as fafh:
        for line in fafh:
            if line.startswith('#'):
                continue
            if not line:
                continue

            if line.startswith('>'):
                identifier = line.lstrip('>').rstrip('\n').split()[0]
                fadict[identifier] = []
            else:
                fadict[identifier].append(line)
    fadict = {identifier:''.join(seq_lst) for identifier,seq_lst in fadict.items()}
    return fadict

def output(matrixfile, mapdict, outdir):
    '''
    '''
    matrix = pd.read_table(matrixfile, header=0, index_col=0)
    speciesid_lst = list(matrix.columns)
    groupid_lst = list(matrix.index)

    if set(speciesid_lst) - set(mapdict.keys()):
        sys.exit(f'Error: matrix species ids not match proteinfileids\n{sorted(speciesid_lst)}\n{sorted(protein_speciesid_lst)}')

    for genome in speciesid_lst:
        os.mkdir(outdir + '/' + genome)
        # out groupid and proteinid mapping file
        with open(outdir + '/' + genome + '/orthogroup2protein.txt', 'wt') as outfh:
            outfh.write('GroupID' + '\t' + 'ProteinID\n')
            for groupid in groupid_lst:
                proteinid = matrix.loc[groupid, genome]
                outfh.write(groupid + '\t' + proteinid + '\n')

        for groupid in groupid_lst:
            proteinid = matrix.loc[groupid, genome]
            proteinsetfa = fasta2dict(mapdict[genome])
            seq = proteinsetfa[proteinid]
            with open(outdir + '/' + genome + '/' + groupid + '.faa', 'wt') as faafh:
                faafh.write('>' + proteinid + '\n' + seq)

if __name__ == '__main__':
    args = parse_args()
    mapdict = get_proteinfile_map(args.proteinfilepathmap)
    output(args.matrixfile, mapdict, args.outdir)
