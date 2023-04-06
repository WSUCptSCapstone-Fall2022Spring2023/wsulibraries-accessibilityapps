#!/usr/bin/env python

""" Tagging documents involves marking content with labels such as a header,
    paragraph, row entries within a table, etc. Tagging helps define the
    reading order, which is another accessibility feature we aim to provide, 
    especially in tables, as well as being used to define alt text for images.
"""

# * Modules
from utils.document import Document
from utils.transform.TagTree import TagTree

# Last Edit By: Reagan Kelley
# * Edit Details: Started implementing tag trees
def generate_tags(doc : Document):
    """Post-condition: Document will be a PDF tagged document.

    Args:
        doc (Document((), optional): PDF handler that allows edits to be made. Defaults to Document().
    """
    doc.tree = create_tag_tree_from_blocks(doc.layout_blocks)

    return doc

def type_to_tag(type):
    if str.lower(type) == 'title':
        return '<H1>'

def create_tag_tree_from_blocks(blocks):
    tree = TagTree()

    print(tree.Cursor.get_tag())
    for type, data in blocks:
        current_tag = tree.Cursor.get_tag()
        new_tag = type_to_tag(type)

        if current_tag == '<document>':
            tree.Cursor.get_tag().set_child(new_tag, data)
            tree.Cursor.Down()
        
        elif current_tag == new_tag:
            tree.Cursor.get_tag().set_next(new_tag, data)




    return tree


if __name__ == '__main__':
    create_tag_tree_from_blocks([('h1', 'this is a header.')])
