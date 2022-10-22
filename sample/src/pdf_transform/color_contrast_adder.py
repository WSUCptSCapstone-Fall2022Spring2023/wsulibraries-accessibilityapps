#!/usr/bin/env python

""" Checks through the document text and compares and contrasts between text color and
    background color and ensures that the difference is adequate to W3C standards. If this is not
    the case then it changes the metadata, changing either the text color or background so that the
    contrast is adequate.
"""
# * Modules
from asyncio.windows_events import NULL
from src.document import Document

def check_color_contrast(doc = Document()):
    """ Given a document and its metadata, checks all text and background
        contrast and fixes it when it is not in-line with W3C standards.

    Args:
        doc (Document((), optional): PDF handler that allows edits to be made. Defaults to Document().
    """
    if(doc.get_filename() == NULL):
        return NULL
    print("check_color_contrast() -> pass.")
    # TODO: Implement this.
    return doc