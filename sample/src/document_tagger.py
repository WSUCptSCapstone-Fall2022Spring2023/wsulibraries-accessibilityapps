#!/usr/bin/env python

""" Tagging documents involves marking content with labels such as a header,
    paragraph, row entries within a table, etc. Tagging helps define the
    reading order, which is another accessibility feature we aim to provide, 
    especially in tables, as well as being used to define alt text for images.
"""

# * Modules
from PyPDF2 import PdfReader

# Last Edit By: Reagan Kelley
# * Edit Details: Skeleton Code -- Not Done
def create_document_tags(reader):
    """Post-condition: Document will be a PDF tagged document.

    Args:
        reader (PdfReader): PDF Handler that gives editable access to a PDF
    """
    # TODO: Implement PDF Tagging according to W3C guidelines.
    # TODO: Get tags from metadata and edit/add them.
    pass
