#!/usr//bin/env python3
'''
spider_get_assembly_metadata.py -- obtain assembly metadata from NCBI assembly database,
                                   and output to sys.stdout.

Website url prefix: https://www.ncbi.nlm.nih.gov/assembly/${accession}
Accession         : assembly accession ids.         

Author  = "Yanpeng Chen"
Version = "1.0"
Email   = "chenyanpeng1992@outlook.com"
Status  = "Development"
'''
import os
import sys
import argparse
from bs4 import BeautifulSoup

def  parse_args():
    '''
    Parse command-line parameters

    Parameter
    ---------
    NULL
    
    Return
    ------
    args : object
        arguments in args.ARGUMENT format
    '''
    parser = argparse.ArgumentParser(description=__doc__,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('directory',
                        metavar='<directory>',
                        type=str,
                        help='input directory name')
    args = parser.parse_args()
    return args

def soup_html(input_dir):
    '''
    Parse html file using BeautifulSoup4.

    Parameters
    ----------
    input_dir : input directory consisting of metadata html files

    Return
    ------
    assemblies_dict : nested dictionary
        {key_level1: {k_l2:, k2_l2,...}...}, kN_l1 represents accession, Kn_l2 represents the header name.
    '''
    assemblies_dict = {}
    html_lst = os.listdir(input_dir)
    for html in html_lst:
        accession = html.rstrip('.html')
        with open(input_dir + '/' + html, 'rt') as html_fh:
            try:
                page = html_fh.read().decode('utf-8')
                soup = BeautifulSoup(page, 'html.parser')
            except:
                sys.exit(f'Error: failed to soup file: {html}')

            keys = []
            for key in soup.find_all('dt'):
                keys.append(key.text)

            values = []
            for value in soup.find_all('dd'):
                values.append(value.text)

            assmebly_dict = dict(zip(keys,values))
            assemblies_dict[accession] = assmebly_dict
    return assemblies_dict

def output_meta_table(assemblies_dict):
    '''
    Output assembly metadat table

    Parameters
    ---------
    assemblies_dict : nested python3 dictionary
        return value of soup_html function.  
    
    Return
    ------
    NULL
    '''
    header_lst = ['Organism name: ', 'Infraspecific name: ', 'BioSample: ', 'BioProject: ','Submitter: ',
                'Date: ','Assembly level: ','Genome representation: ','RefSeq category: ','GenBank assembly accession: ',
                'RefSeq assembly accession: ','RefSeq assembly and GenBank assembly identical: ','WGS Project: ',
                'Assembly method: ','Genome coverage: ','Sequencing technology: ']
    print('\t'.join(header_lst), file=sys.stdout, flush=True)
    
    for accession, accession_dict in assemblies_dict.items():
        out_lst = [accession]
        for tag in header_lst:
            field = accession_dict.get(tag, 'NA')
            out_lst.append(field)
        print('\t'.join(out_lst), file=sys.stdout, flush=True)

if __name__ == '__main__':
    args = parse_args()
    assemblies_dict = soup_html(args.directory)
    output_meta_table(assemblies_dict)