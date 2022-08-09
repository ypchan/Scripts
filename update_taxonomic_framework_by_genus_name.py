#!/usr/bin/env python3
'''
update_taxonomic_framework_by_genus_name.py -- update taxonomic framework accordign given genus name(s)

Taxonomic Framework:
#Refined families of Sordariomycetes. Mycosphere, 2020
Class           Subclass                Order           Family          Genus
Sordariomycetes Diaporthomycetidae      Annulatascales  Annulatascaceae Annulatascus
Sordariomycetes Diaporthomycetidae      Annulatascales  Annulatascaceae Annulusmagnus
Sordariomycetes Diaporthomycetidae      Annulatascales  Annulatascaceae Aqualignicola
Sordariomycetes Diaporthomycetidae      Annulatascales  Annulatascaceae Ascitendus

Table
#Need to add lineage information, the species name must be in the second column
Assembly           Organism                 Strain           Length 
GCA_000222935.2    Aciculosporium take      MAFF-241224      58,836,405
GCA_000769265.1    Acremonium chrysogenum   ATCC 11550       28,563,214
GCA_022814615.1    Acremonium citrinum      FKII-L8-BK-P5    34,525,570
GCA_021347865.1    Acremonium sp.           CBMAI 1973       35,841,001
GCA_020087035.1    Acremonium sp.           FKII-L8-BK-P5    34,452,312
GCA_001653215.1    Akanthomyces lecanii     UM487            32,603,708

Date: 2021-06-28
Bugs: chenyanpeng1992@outlook.com
'''

import os
import sys
import argparse
import fileinput

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('framework',
    metavar='<framework.txt>',
    type=str,
    help='taxonomic framework')

parser.add_argument('straintable',
    type=str,
    metavar='<table>',
    help='strain information table')

args = parser.parse_args()

def read_framework_2_dict(framework):
    framework_dict = {}
    infh = fileinput.input(files = framework)
    for line in infh:
        line_lst = line.rstrip('\n').split('\t')
        if line.startswith('Class'):
            lineage_head = line_lst[:4]
        genus = line_lst[4]
        lineage = '\t'.join(line_lst[:4])
        framework_dict[genus] = lineage
    fileinput.close()
    return framework_dict, lineage_head

if __name__ == '__main__':
    framework_dict, lineage_head = read_framework_2_dict(args.framework)
    with open(args.straintable) as infh:
        counter = 0
        for line in infh:
            counter += 1
            if counter == 1:
                print(line.strip('\n') + '\t' + '\t'.join(lineage_head), file=sys.stdout, flush=True)
                continue
            line_lst = line.rstrip('\n').split('\t')
            genus = line_lst[1].split(' ')[0]
            if genus in framework_dict:
                lineage = framework_dict[genus]
            else:
                lineage = 'na'
            line_lst.append(lineage)
            print("\t".join(line_lst), file=sys.stdout, flush=True)
    sys.exit(0)
