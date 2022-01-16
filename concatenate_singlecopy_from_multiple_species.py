#!/use/bin/env python3
'''
concatenate_singlecopy_from_multiple_species.py -- concatenate single copy gene from multiple species

Date: 2021-05-10
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
    metavar='<map.txt>',
    type=str,
    help='path\torhogroupid')

parser.add_argument('outdir',
    metavar='<outdir>',
    type=str,
    help='output directory.' )

parser.add_argument('format',
    metavar='<aa|nt>',
    type=str,
    help='specify molecular type[aa|nt]')
args = parser.parse_args()



group2species_dict = {}
for line in fileinput.input(files=sys.argv[1]):
    path, groupname = line.rstrip('\n').split()
    path_with_fa = path + '/' + groupname
    if groupname not in group2species_dict:
        group2species_dict[groupname] = [path_with_fa]
    else:
        group2species_dict[groupname].append(path_with_fa)
fileinput.close()

for group,species_lst in group2species_dict.items():
    if args.format == 'aa':
        cmd = f'cat {" ".join(species_lst)} > {args.outir}/{group}.faa'
        os.system(cmd)
    else:
        cmd = f'cat {" ".join(species_lst)} > {args.outir}/{group}.fna'
        os.system(cmd)
