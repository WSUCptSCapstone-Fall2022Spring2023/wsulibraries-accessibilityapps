#!/usr/bin/env python

"""Checks through the images within the document and when necessary adds alternative text to describe the image.
"""

# * Modules
from asyncio.windows_events import NULL
from utils.document import Document

# Last Edit By: Reagan Kelley
# * Edit Details: Skeleton Code -- Not Done
def check_alt_text(doc:Document):
    """ Checks each image within a document, which can be found through the
        document's metadata, and checks to see if there is alternative text provided. If not, it
        runs an algorithm to generate the appropriate text.

    Args:
        doc (Document((), optional): PDF handler that allows edits to be made. Defaults to Document().
    """
    # If Document doc has no file opened, then do not run this algorithm.
    if(doc.get_filename() == NULL):
        return NULL
    # print("check_alt_text() -> pass.")
    # TODO: Implement this.
    return doc

# Last Edit By: Reagan Kelley
# * Edit Details: Skeleton Code -- Not Done
def create_alternative_text(doc:Document):
    """ Runs the machine learning algorithm (already trained), and returns the
        generated alternative text that represents the given image.


    Args:
        doc (Document((), optional): PDF handler that allows edits to be made. Defaults to Document().
    """
    if(doc.get_filename() == NULL):
        return NULL
    print("create_alternative_text() -> pass.")
    # TODO: Implement this.
    return doc
