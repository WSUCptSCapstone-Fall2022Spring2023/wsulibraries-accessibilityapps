#!/usr/bin/env python

""" This file contains the AccessibleDocument class,
    a child class of Document that helps transform it into a W3C accessible document.
"""

# * Modules
import os
from bs4 import BeautifulSoup
from accessibility_apps.utils.harvest.pdf_extractor import _get_font_style_delimeter
from utils.document import Document
from utils.transform.document_tagger import generate_tags, TagTree
from utils.transform.alt_text_adder import check_alt_text, create_alternative_text
from utils.transform.color_contrast_adder import check_color_contrast
from utils.export.document_exporter import export_to_html

output_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+ "/data/output/"
input_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+ "/data/input/"

# Last Edit By: Reagan Kelley
# * Edit Details: Added Generate Tags
class AccessibleDocument(Document):
    """Document class wrapped with accessibility transformation functionality.

    Args:
        Document (Document): Parent Class
    """

    def __init__(self, file_path:str, delete_on_fail=False, save_objects = False, search_saved_objects=False):
        """Create a new instance of AccessibleDocument.

        Args:
            file_path (string): The path name of the PDF that will be processed.
            delete_on_fail (bool): Whether to delete the document at the specified path if it fails to open.
        """
        self.tree : TagTree = None
        super().__init__(file_path, delete_on_fail, save_objects, search_saved_objects)


    # Last Edit By: Reagan Kelley
    # * Edit Details: Initial implementation
    def generate_tags(self):
        """Post-condition: Document will have proper tagging in accordance to W3C guidelines.
        """
        self = generate_tags(self)

        self.tree.traverse_tree(print_it=True)
        out_name = self.split(".")
        export_to_html(self,output_folder+out_name[0]+".html")


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
    
    # TODO: Implement solution with Document class attributes.
