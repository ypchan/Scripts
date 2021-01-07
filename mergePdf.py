#!/usr/bin/env python3

'''
MergePdf.py -- merge all pdf files within the same folder

USAGE:
    Double click mergePdf.py in working directory.
    Wkdir:
    mergePdf.py
    pdf_folder
    Result: merge.pdf
'''

import os
from PyPDF2 import PdfFileReader, PdfFileWriter

def merge_pdf():
    
    merge_pdf_fh = PdfFileWriter()

    pdf_lst = os.listdir('pdf_folder')
    for pdf in pdf_lst:
        pdf_fh = PdfFileReader(open(pdf_file, 'rb'))
        pages = pdf_fh.getNumPages()

        for page in range(pages):
            merge_pdf_fh.addPage(pdf_fh.getPage(page))

    merge_pdf_out = open('merge.pdf', "wb")
    merge_pdf_fh.write(merge_pdf_out)
    merge_pdf_out.close()
    
if __name__ == '__main__':
    merge_pdf()