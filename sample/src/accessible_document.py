#!/usr/bin/env python

""" This file contains the AccessibleDocument class,
    a child class of Document that helps transform it into a W3C accessible document.
"""

# * Modules
from src.document import Document
from src.document_tagger import generate_tags

class AccessibleDocument(Document):
    def __init__(self, filename, using_directory=False):
        super().__init__(filename, using_directory)

    # Last Edit By: Reagan Kelley
    # * Edit Details: Initial implementation
    def generate_tags(self):
        """Post-condition: Document will have proper tagging in accordance to W3C guidelines.
        """
        self = generate_tags(self)