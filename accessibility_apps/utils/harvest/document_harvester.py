#!/usr/bin/env python

""" Takes a PDF and converts it into a codable and transferable
    format via the Document Class. This class object is used to
    transform the document to be in accordance with W3C
    accessibility guidelines.
"""

# * Modules
import os
from PyPDF2 import PdfReader

# This path is where we can find PDFs for processing
INPUT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) + "\\data\\input"

# This path is where we can create or update our transformed PDF.
OUTPUT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) + "\\data\\output"

# Last Edit By: Reagan Kelley
# * Edit Details: Initial implementation
def set_input_directory(path, local=True):
    """Set global variable INPUT_DIRECTORY which is the application retrieves PDFs.

    Args:
        path (String): Path to input directory.
        local (bool, optional): If True: Given address is local to main.py. Defaults to True.
    """
    global INPUT_DIRECTORY
    if(local):
        INPUT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\" + path
    else:
        INPUT_DIRECTORY = path


# Last Edit By: Reagan Kelley
# * Edit Details: Initial implementation
def set_output_directory(path, local=True):
    """Set global variable OUTPUT_DIRECTORY which is where transformed files go.

    Args:
        path (String): Path to output directory.
        local (bool, optional): If True: Given address is local to main.py. Defaults to True.
    """
    # TODO: This variable should probably be added to document_exporter.py (whenever that is created)
    global OUTPUT_DIRECTORY
    if(local):
        OUTPUT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\" + path
    else:
        OUTPUT_DIRECTORY = path

# Last Edit By: Reagan Kelley
# * Edit Details: Initial implementation
def harvest_document(filename, using_directory=False):
    """Opens a PDF file and returns a reader for it.

    Args:
        filename (string): The name of the PDF that will be processed.
        using_directory (bool, optional): If True: Path/filename.pdf given.
        If False: Just filename.pdf given. Defaults to False.

    Returns:
        PdfReader: A PDF file reader for the given filename.
    """
    if(using_directory):
            return PdfReader(filename)
    else:
        return PdfReader(INPUT_DIRECTORY + "\\" + filename)

# ! temporary debugging function
def test_reader(h):
    reader = PdfReader("example.pdf")
    number_of_pages = len(reader.pages)
    page = reader.pages[0]
    text = page.extract_text()
    print(number_of_pages)

# ! temporary debugging function
def test_image_reader():
    reader = PdfReader("example.pdf")
    page = reader.pages[0]
    count = 0
    for image_file_object in page.images:
        with open(str(count) + image_file_object.name, "wb") as fp:
            fp.write(image_file_object.data)
            count += 1
