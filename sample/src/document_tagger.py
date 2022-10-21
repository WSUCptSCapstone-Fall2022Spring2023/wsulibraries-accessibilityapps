#!/usr/bin/env python

""" Tagging documents involves marking content with labels such as a header,
    paragraph, row entries within a table, etc. Tagging helps define the
    reading order, which is another accessibility feature we aim to provide, 
    especially in tables, as well as being used to define alt text for images.
"""

# * Modules
from PyPDF2 import PdfReader
from src.document import Document

# Last Edit By: Reagan Kelley
# * Edit Details: Skeleton Code -- Not Done
def generate_tags(doc = Document()):
    """Post-condition: Document will be a PDF tagged document.

    Args:
        doc (Document((), optional): PDF handler that allows edits to be made. Defaults to Document().
    """
    print("generate_tags() -> pass.")
    # TODO: Implement PDF Tagging according to W3C guidelines.
    # TODO: Get tags from metadata and edit/add them.
    return doc
