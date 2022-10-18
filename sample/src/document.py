#!/usr/bin/env python

""" This file contains the Document Class
"""

# * Modules
from PyPDF2 import PdfReader
from src.document_harvester import harvest_document
from src.create_document_tags import create_document_tags

# Last Edit By: Reagan Kelley
# * Edit Details: Skeleton Code
class Document:
    """Document is a class that allows us to alter and manipulate documents
    """
    # Last Edit By: Reagan Kelley
    # * Edit Details: Initial implementation
    def __init__(self, filename, using_directory=False):
        """Create instance of Document class object.

        Args:
            filename (string): The name of the PDF that will be processed.
            using_directory (bool, optional): If True: Path/filename.pdf given.
            If False: Just filename.pdf given. Defaults to False.
        """
        self.reader = harvest_document(filename, using_directory)
    
    # Last Edit By: Reagan Kelley
    # * Edit Details: Initial implementation
    def get_title(self):
        """Gets the title of the document

        Returns:
            string: document title
        """
        return self.reader.metadata.title
    
    # Last Edit By: Reagan Kelley
    # * Edit Details: Initial implementation
    def create_document_tags(self):
        """Post-condition: Document will have proper tagging in accordance to W3C guidelines.
        """
        self.reader = create_document_tags(self.reader)

        

