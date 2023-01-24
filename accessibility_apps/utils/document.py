#!/usr/bin/env python

""" This file contains the Document Class
"""

# * Modules
import os
from utils.harvest.pdf_extractor import export_to_html
from utils.harvest.pdf_extractor import extract_paragraphs_and_fonts_and_sizes

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

        # setup metadata values
        self.author = ""
        self.title = ""
        self.subject = ""
        self.creator = "WSU Library Accessibilty App"
        self.keywords = []

    def set_metadata(self, author, title, subject, keywords):
        """ Sets the Document metadata values as specified.
        
        Args:
            author (string): The author of the document.
            title (string): The title of the document.
            subject (string): A small description of what the document is about.
            keywords (list): A list of important words in the document.
        """
        self.author = author
        self.title = title
        self.subject = subject
        self.keywords = keywords
    
    # TODO resturcture open document so it is only called once (there should only be one path per doc and no changing the path)
    # TODO create a delete function to delete the pdf at the file path

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
            except:
                pass    

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

        # TODO integrate the pdf converter here and also save the metadata to that pdf

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