#!/usr/bin/env python

""" Creates a pdf from a html link
"""
import linecache
from fpdf import FPDF
import subprocess

# Last Edit By: Marisa Loyd
# * Edit Details: Current code is from Marisa


def export_document(filename):
    """ Transforms the metadata from codable data structures back into a usable and readable
        format: PDF

    Args:
        filename (string): File address location where the PDF will be sent.
    """
    p = subprocess.Popen(['node', 'pdf_exporter.js', filename], stdout=subprocess.PIPE)
    print("export_document() -> pass.")
    return
    # TODO: Implement solution with Document class attributes.

