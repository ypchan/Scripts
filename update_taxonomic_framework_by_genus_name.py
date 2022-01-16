#!/usr/bin/env python3
'''
update_taxonomic_framework_by_genus_name.py -- update taxonomic framework accordign given genus name(s)

Taxonomic Framework:
    Refined families of Sordariomycetes. Mycosphere, 2020

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
    '''
    Class   Subclass        Order   Family  Genus
    Sordariomycetes Diaporthomycetidae      Annulatascales  Annulatascaceae Annulatascus
    Sordariomycetes Diaporthomycetidae      Annulatascales  Annulatascaceae Annulusmagnus
    Sordariomycetes Diaporthomycetidae      Annulatascales  Annulatascaceae Aqualignicola
    Sordariomycetes Diaporthomycetidae      Annulatascales  Annulatascaceae Ascitendus
    Sordariomycetes Diaporthomycetidae      Annulatascales  Annulatascaceae Ayria
    Sordariomycetes Diaporthomycetidae      Annulatascales  Annulatascaceae Cataractispora
    Sordariomycetes Diaporthomycetidae      Annulatascales  Annulatascaceae Chaetorostrum
    Sordariomycetes Diaporthomycetidae      Annulatascales  Annulatascaceae Longicollum
    Sordariomycetes Diaporthomycetidae      Annulatascales  Annulatascaceae Submersisphaeria
    Sordariomycetes Diaporthomycetidae      Annulatascales  Annulatascaceae Vertexicola
    Sordariomycetes Diaporthomycetidae      Annulatascales  incertae sedis  Clohiesia
    Sordariomycetes Diaporthomycetidae      Atractosporales Atractosporaceae        Atractospora
    Sordariomycetes Diaporthomycetidae      Atractosporales Atractosporaceae        Rubellisphaeria
    ...
    '''
    framework_dict = {}
    infh = fileinput.input(files = framework)
    for line in infh:
        line_lst = line.rstrip('\n').split('\t')
        genus = line_lst[4]
        lineage = '\t'.join(line_lst[:4])
        framework_dict[genus] = lineage
    fileinput.close()
    return framework_dict

if __name__ == '__main__':
    framework_dict = read_framework_2_dict(args.framework)
    with open(straintable) as infh:
        counter = 0
        for line in infh:
            counter += 1
            if counter == 1:
                print(line, file=sys.stdout, flush=True)
                continue
            line_lst = line.rstrip('\n').split('\t')
            genus = line_lst[-1]
            if genus in framework_dict:
                lineage = framework_dict[genus]
            else:
                lineage = 'na'
            line_lst.append(lineage)
            print("\t".join(line_lst), file=sys.stdout, flush=True)