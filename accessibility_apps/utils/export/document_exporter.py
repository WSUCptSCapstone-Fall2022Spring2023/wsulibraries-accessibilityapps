#!/usr/bin/env python

""" Creates a pdf from a html link
"""

import os
import sys
import subprocess

path = os.path.abspath('../')
if path not in sys.path:
    sys.path.append(path)

    from utils.transform.TagTree import TagTree
    from utils.accessible_document import generate_tags
    from utils.document import Document

# Last Edit By: Marisa Loyd
# * Edit Details: Current code is from Marisa
def export_document(filename):
    """ Transforms the metadata from codable data structures back into a usable and readable
        format: PDF

    Args:
        filename (string): File address location where the PDF will be sent.
    """

    name = filename.split('.')
    pdfName = name[0]+'_pdf'

    # tag tree -> html
    # font & size correct
    #images ?
    # each section of tag tree have set font size
        #paragraph = 12 pt
        #h1 = 32 pt
        #h2 = 24 pt
        #h3 = 19 pt
        #h4 = 16 pt
        #h5 = 14 pt
        #h6 = 13 pt
    
    p = subprocess.Popen(['node', os.path.dirname(os.path.abspath(__file__)) + '/pdf_exporter.js', filename], stdout=subprocess.PIPE)
    p.wait()
    print("export_document() -> pass.")
    return

    # TODO: Implement solution with Document class attributes.
