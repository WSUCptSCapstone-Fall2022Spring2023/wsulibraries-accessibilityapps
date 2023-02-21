#!/usr/bin/env python

""" This file contains the Document Class
"""

# * Modules
import os
from sys import platform

from utils.harvest.pdf_extractor import export_to_html
from utils.harvest.pdf_extractor import extract_paragraphs_and_fonts_and_sizes
from utils.harvest.document_layout import document_layout

# Last Edit By: Trent Bultsma
# * Edit Details: Use the pdf_extractor to extract and export data.
class Document:
    """Document is a class that allows us to alter and manipulate documents
    """
    # Last Edit By: Trent Bultsma
    # * Edit Details: Use the pdf_extractor to extract and export data.
    def __init__(self, file_path=None):
        """Create instance of Document class object.

        Args:
            file_path (string): The path name of the PDF that will be processed.
        """
        self.open_document(file_path)
    
    # Last Edit By: Trent Bultsma
    # * Edit Details: Use the pdf_extractor to extract and export data.
    def open_document(self, file_path:str=None):
        """ Opens a PDF for editing. If a file is already opened, 
            this will close it and start writing to this one instead.

        Args:
            file_path (string): The path name of the PDF that will be processed.
        """
        # default value for if opening the file fails
        self.file_path = None
        self.paragraphs = []

        # make sure the file is a pdf
        if file_path is not None and file_path.lower().endswith(".pdf"):
            try:
                # extract the data
                self.paragraphs = extract_paragraphs_and_fonts_and_sizes(file_path)
                self.file_path = file_path
            except Exception as e:
                print("Warning [document.py] - Caught Error : {}".format(e))

            if platform == "linux" or platform == "linux2":
                # get the layout of the document for tagging (it is ordered and includes tag type and data)
                self.layout_blocks = document_layout(self.file_path, True)
            else:
                print("Layout Parsing Skipped: Non-Linux distributions not yet supported...")
                self.layout_blocks = []

    def is_open(self):
        """ Returns true if there is a file open for editing.

        Returns:
            Bool: If a file is opened.
        """
        return self.file_path != None
    
    

    # Last Edit By: Trent Bultsma
    # * Edit Details: Use the pdf_extractor to extract and export data.
    def export_document(self, file_path:str=None):
        """ Transforms the metadata from codable data structures back into a usable and readable
            format: HTML

            Args:
            file_path (string): The path name of the html doc to be exported.
        """
        # TODO use the paragraph objects to write a better exporting function that actually goes to a pdf
        # (this is just a temporary exporting function before we get that working)

        # use the file path of the input file but change the extension to .html instead of .pdf if file path not specified
        if file_path is None:
            file_path = self.file_path[:-len("pdf")] + "html"

        # export the document
        export_to_html(self.paragraphs, file_path)

    # Last Edit By: Trent Bultsma
    # * Edit Details: Use the pdf_extractor to extract and export data.
    def get_filename(self):
        """Gets the title of the document

        Returns:
            string: document title
        """
        if self.file_path is None:
            return None
        return os.path.basename(self.file_path)