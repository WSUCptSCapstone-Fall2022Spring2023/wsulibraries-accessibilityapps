#!/usr/bin/env python

""" Tagging documents involves marking content with labels such as a header,
    paragraph, row entries within a table, etc. Tagging helps define the
    reading order, which is another accessibility feature we aim to provide, 
    especially in tables, as well as being used to define alt text for images.
"""

# * Modules
from utils.document import Document
from utils.transform.TagTree import TagTree, tag_cmp, TagFactory
from typing import List

# Last Edit By: Reagan Kelley
# * Edit Details: Started implementing tag trees
def generate_tags(doc : Document):
    """Post-condition: Document will be a PDF tagged document.

    Args:
        doc (Document((), optional): PDF handler that allows edits to be made. Defaults to Document().
    """
    doc.tree = create_tag_tree_from_blocks(doc.layout_blocks)
    return doc

def type_to_tag(block_type : str):
    """ Returns the tag equivalent to the layout parsers block types.

    Args:
        block_type (str): The str name of the type for the current layout block.

    Raises:
        Exception: Raises if the layout block name is not defined as a tag.

    Returns:
        str: The str name of the tag equivalent
    """
    block_type = str.lower(block_type)

    if block_type == 'title':
        return '<H1>'
    elif block_type == 'text':
        return '<P>'
    elif block_type == 'figure':
        return '<Figure>'
    elif block_type == 'list':
        return '<L>'
    elif block_type == 'table':
        return '<Table>'
    else:
        err_msg = f'Unknown block type: [{block_type}]. Cannot determine tag label.'
        raise Exception(err_msg)

def create_tag_tree_from_blocks(blocks : List[tuple[str, str]]):
    """ Creates a tag tree from a list of layout blocks (from the document parser)

    Args:
        blocks (List[tuple[str, str]]): A layout block where tuple[0] is the type of block and tuple[1] is the data.

    Returns:
        TagTree: A new tag tree data object.
    """
    tree = TagTree()

    for tag_label, data in blocks:


        current_tag = tree.Cursor.get_tag()
        new_tag = type_to_tag(tag_label)
        
        #print(f"[{tag_label}]")
        #print(data, end='\n')
        #print("\tCurrent Tag: {}".format(current_tag.get_data()))

        precedence_val = tag_cmp(current_tag, TagFactory(new_tag))

        if precedence_val < 0:
            # current tag is of higher precedence, so this new tag must be a child.
            tree.Cursor.get_tag().set_child(new_tag, data)
            tree.Cursor.Down()
        
        elif precedence_val == 0:
            # current tag and new tag is same precedence, must be a sister tag.
            tree.Cursor.get_tag().set_next(new_tag, data)
            tree.Cursor.Next()

        else:
            # new tag is of higher precedence, so this new tag must be the sister of a parent.
            
            # move up tree until parent tag matches precedence or is of higher precedence 
            while tag_cmp(tree.Cursor.Up().get_tag(), TagFactory(new_tag)) > 0:
                continue

            #print("\tMoved to parent tag: {}".format(tree.Cursor.get_tag().get_data()))
            
            # if moved to root of tree, make the new tag, the next sister of children from root.
            if tree.Cursor.get_tag() == '<document>':
                tree.Cursor.Down()

                last_sister = False
                while not last_sister:
                    try:
                        tree.Cursor.Next()
                    except:
                        last_sister = True
                
            tree.Cursor.get_tag().set_next(new_tag, data)
            tree.Cursor.Next()
    return tree


if __name__ == '__main__':
    create_tag_tree_from_blocks([('h1', 'this is a header.')])
