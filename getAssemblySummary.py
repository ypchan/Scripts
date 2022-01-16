#!/usr/bin/env python3

'''
getAssemblySummary.py -- get summary information of assemblies by accession_id, tax_name, tax_id

AUTHOR: Yanpeng Chen
DATE  : 2020-11-05
BUGS  : Any bugs should be reported to 764022822@qq.com
'''

import sys
import argparse

try:
    import ncbi.datasets
except ImportError:
    print('ERROR: ncbi.datasets module not found. To install, run `pip install ncbi-datasets-pylib`.', file=sys.stderr, flush=True)
    sys.exit(1)

def parse_args():
    '''Parse command-line arguments.
    '''
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('--taxon_name',
        metavar='<taxon-name>',
        type=str,
        help='get assembly descriptors by organism or tax group name')

    parser.add_argument('--accession',
        metavar='<accession-id>',
        type=str,
        help='get assembly descriptors by accession')

    parser.add_argument('--accession_file',
        metavar='<accession-file>',
        type=str,
        help='get multiple assemblies descriptors by accession id')

    args = parser.parse_args()
    if any([args.taxon_name, args.accession, args.accession_file]):
        return args
    else:
        print('ERROR: one argument must be selected from --taxon_name, --accession, --accession_file', file=sys.stderr, flush=True)
        sys.exit(1)

def get_obj_by_accession(accession:str):
    '''get assembly descriptors object by accession(s)

    Example:
    GCA_001563115.1
    GCA_001563115.1，GCA_002814275.1
    '''
    if ',' in accession:
        assembly_accession_lst = accession.split(',')
    else:
        assembly_accession_lst = [accession]

    api_instance = ncbi.datasets.GenomeApi(ncbi.datasets.ApiClient())
    try:
        assembly_descriptors = api_instance.assembly_descriptors_by_accessions(assembly_accession_lst, limit='all')
    except:
        print(f'ERROR: {accession} is an invalid NCBI Taxonomy id', file=sys.stderr, flush=True)

    if len(assembly_descriptors.assemblies) != len(assembly_accession_lst):
        num_accession_err = len(assembly_accession_lst) - len(assembly_descriptors.assemblies)
        print('ERROR: {num_accession_err:<4} accession are invalid', file=sys.stderr, flush=True)
        sys.exit(1)

    return assembly_descriptors

def get_obj_by_accession_file(accession_file:str):
    '''get assembly descriptors object by accession file

    File content:
    GCA_001563115.1
    GCA_002814275.1
    ...
    '''
    assembly_accession_lst = []
    accession_fh = open(accession_file, 'rt')
    for line in accession_fh:
        if line.startswith('#'):
            continue
        line = line.rstrip('\n')
        if line:
            assembly_accession_lst.append(line)

    api_instance = ncbi.datasets.GenomeApi(ncbi.datasets.ApiClient())
    try:
        assembly_descriptors = api_instance.assembly_descriptors_by_accessions(assembly_accession_lst, limit='all')
    except:
        print(f'ERROR: {accession} is an invalid NCBI Taxonomy id', file=sys.stderr, flush=True)

    if len(assembly_descriptors.assemblies) != len(assembly_accession_lst):
        num_accession_err = len(assembly_accession_lst) - len(assembly_descriptors.assemblies)
        print('ERROR: {num_accession_err:<4} accession are invalid', file=sys.stderr, flush=True)
        sys.exit(1)

    return assembly_descriptors

def get_obj_by_tax_name(tax_name):
    '''get assembly descriptors object by tax_name

    Examples:
    tax_name = 'mammals'
    tax_name = 'birds'
    tax_name = 'butterflies'
    '''
    api_instance = ncbi.datasets.GenomeApi(ncbi.datasets.ApiClient())
    try:
        assembly_descriptors = api_instance.assembly_descriptors_by_taxon(taxon=tax_name, limit='all')
    except:
        print(f'ERROR: {tax_name} is an invalid NCBI Taxonomy name', file=sys.stderr, flush=True)
        sys.exit(1)

    return assembly_descriptors

def get_summary(assembly_descriptors:object):
    metadata_dict = {}
    for assembly in assembly_descriptors.assemblies:
        assembly_dict = assembly.to_dict()['assembly']
        assembly_accession = assembly_dict['assembly_accession']
        del assembly_dict['assembly_accession']
        if len(assembly_dict['chromosomes']) > 1:
            assembly_dict['chromosomes'] = '-'.join(assembly_dict['chromosomes'])
        else:
            assembly_dict['chromosomes'] = ''
        if assembly_dict['annotation_metadata']:
            assembly_dict['annotation_metadata'] = '1'
        if assembly_accession not in metadata_dict:
            metadata_dict[assembly_accession] = {}
        else:
            print('ERROR: duplicate assembly accession', file=sys.stderr, flush=True)
        origin_dict = assembly_dict['org']
        del assembly_dict['org']
        rm_keys = ['assembly_counts', 'merged_tax_ids']
        for key in rm_keys:
            del origin_dict[key]
        metadata_dict[assembly_accession].update(assembly_dict)
        metadata_dict[assembly_accession].update(origin_dict)
    return metadata_dict

def out_summary_table(metadata_dict):
    '''output tab-delimited txt file.
    '''
    n = 0
    for accession in metadata_dict:
        head_lst = ['assembly_accession']
        line_lst = [accession]
        n += 1
        for term, info in metadata_dict[accession].items():
            if n == 1:
                head_lst.append(term)
            if not info:
                info = ''
            line_lst.append(info)
        if n == 1:
            head_line = '\t'.join(head_lst)
            print(head_line, file=sys.stdout, flush=True)
        try:
            line_lst = [str(i) for i in line_lst]
            line = '\t'.join(line_lst)
        except TypeError:
            print(line_lst, file=sys.stderr, flush=True)
            sys.exit(1)
        print(line, file=sys.stdout, flush=True)

if __name__ == '__main__':
    args = parse_args()
    if args.taxon_name:
        assembly_descriptors = get_obj_by_tax_name(args.taxon_name)

    if args.accession:
        assembly_descriptors = get_obj_by_accession(args.accession)

    if args.accession_file:
        assembly_descriptors = get_obj_by_accession_file(args.accession_file)

    metadata_dict = get_summary(assembly_descriptors)
    out_summary_table(metadata_dict)