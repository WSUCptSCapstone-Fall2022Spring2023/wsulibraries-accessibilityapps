#!/usr/bin/env python

""" This file contains the Document Class
"""

# * Modules
import os
from PyPDF2 import PdfReader, PdfWriter
from utils.harvest.pdf_extractor import export_to_html
from utils.harvest.pdf_extractor import extract_paragraphs_and_fonts_and_sizes

# Last Edit By: Trent Bultsma
# * Edit Details: Use the pdf_extractor to extract and export data.
class Document:
    """Document is a class that allows us to alter and manipulate documents
    """
    # Last Edit By: Trent Bultsma
    # * Edit Details: Use the pdf_extractor to extract and export data.
    def __init__(self, file_path:str):
        """Create instance of Document class object.

        Args:
            file_path (string): The path name of the PDF that will be processed.
        """
        self._open_document(file_path)

        # setup metadata values
        self.author = ""
        self.title = ""
        self.subject = ""
        self.creator = "WSU Library Accessibilty App"
        self.keywords = []

        # for checking when the file is deleted
        self.deleted = False

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
        # TODO add created date
    
    # Last Edit By: Trent Bultsma
    # * Edit Details: Use the pdf_extractor to extract and export data.
    def _open_document(self, file_path:str):
        """ Opens a PDF for editing. It should only be called in the constructor.

        Args:
            file_path (string): The path name of the PDF that will be processed.
        """

        # make sure the file is a pdf
        if file_path is not None and file_path.lower().endswith(".pdf"):
            # extract the data
            self.paragraphs = extract_paragraphs_and_fonts_and_sizes(file_path)
            self.file_path = file_path
        else:
            raise ValueError("Invalid file path, must be a pdf file")

    def is_open(self):
        """ Returns true if there is a file open for editing.

        Returns:
            Bool: If a file is opened.
        """
        return not self.deleted and self.file_path != None

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
        # self._apply_metadata("<exported pdf name goes here>")

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

    def delete(self):
        """Deletes the open document."""
        os.remove(self.file_path)
        self.deleted = True

    def _apply_metadata(self, export_file_path:str):
        """Applies the document metadata to the inputted pdf file path.
        
            Args:
            export_file_path (str): the path of the pdf file to write the metadata to.
        """
        # make sure the file is a pdf
        if not export_file_path.lower().endswith(".pdf"):
            raise ValueError("Must be a pdf file")
        
        # setup the reader and writer
        reader = PdfReader(export_file_path)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        # add the metadata to the writer
        writer.add_metadata(
            {
                "/Author" : self.author,
                "/Title" : self.title,
                "/Subject" : self.subject,
                "/Creator" : self.creator,
                "/Keywords" : ", ".join(self.keywords)
            }
        )

        # overwrite the file now with metadata
        with open(export_file_path, "wb") as file:
            writer.write(file)