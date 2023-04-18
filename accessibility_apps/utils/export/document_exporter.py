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
def export_document_to_pdf(input_file_path, output_file_path):
    """ Transforms the metadata from codable data structures back into a usable and readable
        format: PDF

    Args:
        input_file_path (str): File address of the input html.
        output_file_path (str): File address of the output pdf.
    """
    p = subprocess.Popen(['node', os.path.dirname(os.path.abspath(__file__)) + '/pdf_exporter.js', input_file_path, output_file_path], stdout=subprocess.PIPE)
    p.wait()
    print("export_document() -> pass.")
    return

    # TODO: Implement solution with Document class attributes.
