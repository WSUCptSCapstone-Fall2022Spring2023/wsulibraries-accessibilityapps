#!/usr/bin/env python

""" Creates a pdf from a html link
"""

import linecache
from fpdf import FPDF
import subprocess

# Last Edit By: Reagan Kelley
# * Edit Details: Current code is from Marisa


def export_document(filename):
    """ Transforms the metadata from codable data structures back into a usable and readable
        format: PDF

    Args:
        filename (string): File address location where the PDF will be sent.
    """
    print("export_document() -> pass.")
    p = subprocess.Popen(['node', 'pdf_exporter.js', 'example.html'], stdout=subprocess.PIPE)
    return
    # TODO: Implement solution with Document class attributes.
    pdf = FPDF()
    
    pdf.add_page()
    
    # heading font size = 27
    pdf.set_font("Arial", size = 27)

    #get heading of pdf 
    line = linecache.getline(filename,1)

    #iterative variable for lines 2 -> end of pdf
    n = 2

    #create pdf cell aligned in center
    pdf.cell(200, 10, txt = line, ln = 1, align = 'C')
    with open(filename) as f:
        for line in f:
            #body font size = 12
            pdf.set_font("Arial", size = 12)
            line = linecache.getline(filename,n)
            #next line 
            n = n+1
            #add current line to pdf aligned to the left
            pdf.cell(200, 10, txt = line, ln = 1, align = 'L')

    pdf.output("test.pdf")

