#!/usr/bin/env python3
'''
extract_pdf_pages -- extract target page(s) from PDF file.

Date: 2021-05-31
Bugs: Any bugs should reported to chenyanpeng1992@outlook.com
'''
import os
import sys
import argparse
from PyPDF2 import PdfFileReader, PdfFileWriter

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('--pdf',
                    metavar='input.pdf',
                    required=True,
                    type=str,
                    help='input PDF file')

parser.add_argument('--page_nums',
                    metavar='...',
                    required=True,
                    nargs='+',
                    type=int,
                    help='specify the pages. Ex: 1_10; 2 5 7')

parser.add_argument('--out',
                    metavar='out.pdf',
                    type=str,
                    help='output file name')

args = parser.parse_args()

page_lst = []
for page_num in args.page_nums:
    if '_' in page_num:
        start, end = page_num.split('_')
        start = int(start) - 1
        end = int(end)
        page_lst.extend(list(range(start, end)))
    else:
        page_lst.append(int(page_num)-1)

page_lst = list(set(page_lst))
page_lst.sort()


input_file = PdfFileReader(open(args.pdf, 'rb'))

output_file = PdfFileWriter()

for i in page_lst:
    output_file.addPage(input_file.getPage(i))

if not args.out:
    args.out = str(page_lst[0]) + '_' + str(page_lst[-1]) + '.pdf'

with open(args.out, 'wb') as f:
    output_file.write(f)