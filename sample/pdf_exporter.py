#!/usr/bin/env python

""" Creates a pdf from a text file
"""

import linecache
import textwrap
from fpdf import FPDF
 
pdf = FPDF()
 
pdf.add_page()

textName = input("Enter the name of the text file you want to convert to a pdf : ")
baseName = textName.split('.')
dotPdf = ".pdf"
pdfName = baseName[0] + dotPdf
# heading font size = 27
#pdf.set_font("Arial", size = 27)

#get heading of pdf 
#line = linecache.getline(textName,1)

#iterative variable for lines 2 -> end of pdf
n = 1

#create pdf cell aligned in center
#pdf.cell(200, 10, txt = line, ln = 1, align = 'C')
with open(textName) as f:
    for line in f:
        #body font size = 12
        pdf.set_font("Arial", size = 12)
        line = linecache.getline(textName,n)
        #next line 
        n = n+1
        #add current line to pdf aligned to the left
        pdf.cell(200, 10, txt = line, ln = 1, align = 'L')

pdf.output(pdfName)
 