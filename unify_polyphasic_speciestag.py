#!/usr/bin/env python3
'''
'''
import pandas

def unify_species_tag(column_lst):
    hash_dict = {'NA':'species_0'}
    n = 0
    for species_tag in column_lst:
       if species_tag not in hash_dict:
           n += 1
           hash_dict[species_tag] = 'species_' + n
    return hash_dict

def 
