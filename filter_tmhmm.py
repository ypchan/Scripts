#!/usr/bin/env python3
'''
filter_tmhmm.py -- filter tmhmm result file.

Bugs : Any bugs should be reported to yanpengch@qq.com
Date : 2020-11-03
'''
import sys
import argparse

parser = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('-i',
                    '--input',
                    required=True,
                    type=str,
                    help='six-cloumn tmhmm resulting file')

parser.add_argument('-o',
                    '--output',
                    required=True,
                    type=str,
                    help='output filename')

args = parser.parse_args()


def filter_tmhmm(tmhmm_result: str, outfile: str):
    '''The first few lines gives some statistics:

    Length: the length of the protein sequence.
    Number of predicted TMHs: The number of predicted transmembrane helices.
    Exp number of AAs in TMHs: The expected number of amino acids intransmembrane helices. 
                               If this number is larger than 18 it is very likely to be a transmembrane protein (OR have a signal peptide).
    Exp number, first 60 AAs: The expected number of amino acids in transmembrane helices in the first 60 amino acids of the protein. 
                            If this number more than a few, you should be warned that a predicted transmembrane helix in the N-term could be a signal peptide.
    Total prob of N-in: The total probability that the N-term is on the cytoplasmic side of the membrane.
    POSSIBLE N-term signal sequence: a warning that is produced when "Exp number, first 60 AAs" is larger than 10.

    if PredHel <= 1 and (ExpAA <= 18 or (ExpAA > 18 and First60 >= 10) )
    '''
    with open(tmhmm_result, 'rt') as infh, open(outfile, 'wt') as otfh:
        for line in infh:
            line_lst = line.rstrip('\n').split()
            num_exp_aa = float(line_lst[2].split('=')[1])
            num_first_60 = float(line_lst[3].split('=')[1])
            num_pred_mhs = float(line_lst[4].split('=')[1])
            if num_pred_mhs <= 1:
                if num_exp_aa <= 18:
                    otfh.write(line)
                else:
                    if num_first_60 >= 10:
                        otfh.write(line)


if __name__ == '__main__':
    filter_tmhmm(args.input, args.output)
    sys.exit(0)
