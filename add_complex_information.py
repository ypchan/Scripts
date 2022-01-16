#!/use/bin/env python3
'''
add_complex_information.py -- add complex information column into table.

Date: 2021-06-10
Bugs: Any bugs should be reported to chenyanpeng1992@outlook.com

'''
import os
import sys
import argparse
import fileinput


parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('map',
    type=str,
    help='species and its complex information: speceies    complex')

parser.add_argument('table',
    type=str,
    help='table need to be added the complex column')

parser.add_argument('--column',
    type=int,
    default=1,
    help='speces name column')

args = parser.parse_args()

def read_map_2dict(mapfile):
    '''
    species complex
    '''
    species2complex_dict = {}
    for line in fileinput.input(mapfile):
        species, complexinfo = line.rstrip('\n').split('\t') 
        species2complex_dict[species] = complexinfo
    return species2complex_dict

if _name__ == '__main__':
    species2complex_dict = read_map_2dict(args.mapfile)
    with open(args.table) as infh:
        counter = 0
        for line in infh:
            counter += 1
            line_lst = line.rstrip('\n').split()
            if counter == 1:
                line_lst.append('Complex')
                print('\t'.join(line_lst))
                continue
            speceis = line_lst[args.column - 1]
            if speceis not in species2complex_dict:
                sys.exit(f'Error message: {species} not in species_complex mapping table')
            line_lst.append(species2complex_dict[speceis])
            print('\t'.join(line_lst))