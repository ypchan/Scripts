#!/usr/bin/env python3


def check_input_is_file(inputstring):
    '''Check whether the inputstring is file name.
    '''
    if hasattr(inputstring, 'read'):
        return True
    else:
        return False

def count_nucleotide_occurrence(dnastring):
    '''Count the number of occurrences of each nucleotide in a given strand of DNA.
    '''
    dnastring = dnastring.upper()
    nucleotides = ['A','C', 'G', 'T']
    count_lst = []
    for nucleotide in nucleotides:
        # Output order: A C G T
        count_lst.append(dnastring.count(nucleotide))
    return(count_lst)

from codondict import mRNAcodonDict, DNAcodonDict

def nuclseq2protein (sequence, phase=1, stopsymbol='*'):
    '''Translate DNA or RNA to protein from given start base
    '''
    aminoacid_lst = []
    num_codon = int(len(sequence[phase-1:]) / 3)
    sequence = sequence[phase-1:]
    for i in range(num_codon):
        codon = sequence[i*3:(i+1)*3]
        aminoacid = mRNAcodonDict.get(codon) if 'U' in sequence.upper() else DNAcodonDict.get(codon)
        if aminoacid == 'stop':
            aminoacid = stopsymbol
        aminoacid_lst.append(aminoacid)
    return ''.join(aminoacid_lst)

def reverse_complement(dnastring):
    '''Get the reverse complement of the given DNA string 
    '''
    basepair_dict = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    return ''.join([basepair_dict[base] for base in dnastring.upper()[::-1]])

def fibonacci(generation_num, initial_num=1, offspring_size=3):
    '''get the total number of rabbit pairs that will be present after n months, if we begin with 1 pair and in each generation, every pair of reproduction-age rabbits produces a litter of k rabbit pairs (instead of only 1 pair).
    '''
    if generation_num > 2:
        return fibonacci(generation_num - 2) * offspring_size + fibonacci(generation_num - 1)
    else:
        return initial_num