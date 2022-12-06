#!/usr/bin/env python

""" Tagging documents involves marking content with labels such as a header,
    paragraph, row entries within a table, etc. Tagging helps define the
    reading order, which is another accessibility feature we aim to provide, 
    especially in tables, as well as being used to define alt text for images.
"""

# * Modules
from utils.document import Document
from utils.TagTree import Tag, TagTree

# Last Edit By: Reagan Kelley
# * Edit Details: Started implementing tag trees
def generate_tags(doc = Document()):
    """Post-condition: Document will be a PDF tagged document.

    Args:
        doc (Document((), optional): PDF handler that allows edits to be made. Defaults to Document().
    """
    tree = TagTree()
    tree.Cursor.get_tag().set_data("This is a document")
    print(tree.Cursor.get_tag().get_data())

    tree.Cursor.get_tag().set_child('<H1>').set_data("This is a heading")
    print(tree.Cursor.Down().get_tag().get_data())
    tree.Cursor.get_tag().set_next('<H1>').set_data('This is the second heading.')
    print(tree.Cursor.Up().get_tag().get_data())
    
    print(tree.Cursor.Down().Next().get_tag().get_data())
    tree.Cursor.Back().get_tag().set_child("<P>", "This is a paragraph")
    print(tree.Cursor.Down().get_tag().get_data())

    print("\n")
    tree.traverse_tree()

    # TODO: Implement PDF Tagging according to W3C guidelines.
    # TODO: Get tags from metadata and edit/add them.
    return doc
