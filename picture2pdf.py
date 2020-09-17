#!/usr/bin/env python3
'''
Name:
    picture2pdf.py written by ypchen@764022822.com
Synopsis:
    Do convert mutiple pictures to pdf.
Dependency:
    1. Python 3+
    2. fpdf, PIL module
Usage:
    Pictures and script must be in the same directory. Double click the script, and the result=result.pdf 
'''
import os
import sys
from fpdf import FPDF
from PIL import Image

def makePdf(pdfFileName, listPages):
    cover = Image.open(listPages[0])
    width, height = cover.size

    pdf = FPDF(unit = "pt", format = [width, height])
    for page in listPages:
        pdf.add_page()
        pdf.image(page, 0, 0)
    pdf.output(pdfFileName, "F")

script = os.path.basename(sys.argv[0])
files_lst = os.listdir()
files_lst.remove(script)
files_lst.sort()
makePdf("result.pdf", files_lst)
print('result =', os.path.abspath('result.pdf'), file=sys.stdout, flush=True)
input('input "q" and type Enter-key to exit:')
