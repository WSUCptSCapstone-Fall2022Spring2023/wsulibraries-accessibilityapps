#!/usr/bin/env python

""" This file contains the AccessibleDocument class,
    a child class of Document that helps transform it into a W3C accessible document.
"""

# * Modules
from document import Document
from pdf_transform.document_tagger import generate_tags
from pdf_transform.alt_text_adder import check_alt_text, create_alternative_text
from pdf_transform.color_contrast_adder import check_color_contrast

# Last Edit By: Reagan Kelley
# * Edit Details: Added Generate Tags
class AccessibleDocument(Document):
    """Document class wrapped with accessibility transformation functionality.

    Args:
        Document (Document): Parent Class
    """

    def __init__(self, file_path=None):
        """Create a new instance of AccessibleDocument.

        Args:
            file_path (string): The path name of the PDF that will be processed.
        """
        super().__init__(file_path)

    # Last Edit By: Reagan Kelley
    # * Edit Details: Initial implementation
    def generate_tags(self):
        """Post-condition: Document will have proper tagging in accordance to W3C guidelines.
        """
        self = generate_tags(self)

    # Last Edit By: Reagan Kelley
    # * Edit Details: Initial implementation
    def create_alternative_text(self):
        """ Checks all images in the file and provides alt-text, describing the image.
        """
        self = check_alt_text(self)
        self = create_alternative_text(self)

    # Last Edit By: Reagan Kelley
    # * Edit Details: Initial implementation
    def check_color_contrast(self):
        """ Given a document and its metadata, checks all text and background
            contrast and fixes it when it is not in-line with W3C standards.
        """
        self = check_color_contrast(self)