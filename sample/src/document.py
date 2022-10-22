#!/usr/bin/env python

""" This file contains the Document Class
"""

# * Modules
from asyncio.windows_events import NULL
from PyPDF2 import PdfReader
from src.document_harvester import harvest_document
from src.document_exporter import export_document

# Last Edit By: Reagan Kelley
# * Edit Details: Skeleton Code
class Document:
    """Document is a class that allows us to alter and manipulate documents
    """
    # Last Edit By: Reagan Kelley
    # * Edit Details: Initial implementation
    def __init__(self, filename=NULL, using_directory=False):
        """Create instance of Document class object.

        Args:
            filename (string): The name of the PDF that will be processed.
            using_directory (bool, optional): If True: Path/filename.pdf given.
            If False: Just filename.pdf given. Defaults to False.
        """
        if(filename != NULL):
            self.reader = harvest_document(filename, using_directory)
        self.filename = filename
    
    # Last Edit By: Reagan Kelley
    # * Edit Details: Initial implementation
    def open_document(self, filename=NULL, using_directory=False):
        """ Opens a PDF for editing. If a file is already opened, 
            this will close it and start writing to this one instead.

        Args:
            filename (string): The name of the PDF that will be processed.
            using_directory (bool, optional): If True: Path/filename.pdf given.
            If False: Just filename.pdf given. Defaults to False.
        """
        if(filename != NULL):
            self.reader = harvest_document(filename, using_directory)
        self.filename = filename
    

    def IsOpen(self):
        """ Returns true if there is a file open for editing.

        Returns:
            Bool: If a file is opened.
        """
        return self.filename != NULL

    # Last Edit By: Reagan Kelley
    # * Edit Details: Initial implementation
    def export_document(self):
        """ Transforms the metadata from codable data structures back into a usable and readable
            format: PDF
        """
        export_document(self.filename)

    # Last Edit By: Reagan Kelley
    # * Edit Details: Initial implementation
    def get_filename(self):
        """Gets the title of the document

        Returns:
            string: document title
        """
        if(self.filename == NULL):
            return NULL
        return self.reader.metadata.title
    
    def get_info(self):
        # ! Debugging function: Currently testing proper reading of pdf.
        info = self.reader.getDocumentInfo()
        nb_pages = self.reader.getNumPages()
        info = dict(info)
        info['nb_pages'] = nb_pages
        for key, value in sorted(info.items()):
            print(f"{key:<15}: {value}")
    

        

