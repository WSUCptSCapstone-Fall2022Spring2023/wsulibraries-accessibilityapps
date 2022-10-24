#!/usr/bin/env python

""" Tagging documents involves marking content with labels such as a header,
    paragraph, row entries within a table, etc. Tagging helps define the
    reading order, which is another accessibility feature we aim to provide, 
    especially in tables, as well as being used to define alt text for images.
"""

# * Modules
from asyncio.windows_events import NULL
from src.document import Document

# Last Edit By: Reagan Kelley
# * Edit Details: Skeleton Code -- Not Done
def generate_tags(doc = Document()):
    """Post-condition: Document will be a PDF tagged document.

    Args:
        doc (Document((), optional): PDF handler that allows edits to be made. Defaults to Document().
    """
    # If Document doc has no file opened, then do not run this algorithm.
    if(doc.get_filename() == NULL):
        return NULL
    print(str(doc.reader.metadata))

    P1 = """Poachers come in the cover of night to rob her eggs. 
    Sometimes they come for her meat,killing all turtles on a beach; 
    sometimes they take them alive on cruel journeys to be 
    sold on the black market."""

    # (tag_name, value)
    # ? Tag name syntax ?
    # ? IMPORTANT NOTE: Every time a tag is added that point in the tree is remembered as the prev node.
    # ? '<tag>'    => the name of the tag. Is added to the tree.
    # ? '::<tag>'  => This tag will be a child of the prev node. '::' indicates go down hierarchy
    # ? ':<tag>'   => This tag will be a sister node of the prev node. ':' means this will be Node.next of prev node.
    # ? '-:<tag>'  => This tag will become the Node.next of prev node's parent. '-' go up on hierarchy level
    # ? '--:<tag>' => Same as '-:' but go up 2 levels. Every '-' signifies another parent node from prev node.
    # ? '<tag1>::<tag2>:<tag3>
    tree = TagTree([('<sect>', NULL), 
    ('::<H1>', "Save the turtles"), ('::<P>', P1), 
    ("-:<H1>", "Let's all save the whales"), ("<sect>::<H1>:<H1>::<P1>", "It isn't worth the blubber."),
    ("--:<sect>", NULL)], ("::<H1>", "Don't save pandas."))



    # TODO: Implement PDF Tagging according to W3C guidelines.
    # TODO: Get tags from metadata and edit/add them.
    return doc

class TagTree():
    class __Node():
        def __init__(self):
            self.tag_name = ""
            self.data = NULL
            self.child = []
            self.next = NULL

    def __init__(self, tree_list):
        pass