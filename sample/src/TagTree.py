#!/usr/bin/env python

"""TagTree includes definition of tags, a tag factory, and a tag tree (a data structure that utilizes tags).
"""

# * Modules
import inspect
import sys
from abc import ABC, abstractmethod

class TagTree():
    def __init__(self, tree_list):
        pass

# Last Edit By: Reagan Kelley
# * Edit Details: Initial implementation
def TagFactory(tag_name):
    """Given a tag name '<tag_name>', return a Tag class instance of it.

    Args:
        tag_name (str): The name of the tag in tag string format.

    Raises:
        Exception: If given tag name is not defined.

    Returns:
        Tag: A child class of type that is the type of tag requested.
    """
    for children in Tag.__subclasses__():
        child_class = children()
        if str(child_class) == tag_name:
            return child_class
    raise Exception("TagFactory Error: '{}' is not a defined tag.".format(tag_name))

# Last Edit By: Reagan Kelley
# * Edit Details: Initial implementation
class Tag(ABC):
    """ A tag marks a PDF tags making it possible to identify 
    content as such headings, lists, tables, etc., and to include 
    alternate text for images. This is an abstract class
    which specific type of tags inherent.

    Args:
        ABC (Abstract Class): Marks this as an abstract class.
    """
    def __init__(self):
        self.data = None
        self.child = None
        self.next = None

    @abstractmethod
    def __str__(self):
        pass


    def get_data(self):
        """Returns data contained within this tag.

        Returns:
            _type_: Could be anything
        """
        return self.data

    def set_data(self, data):
        self.data = data
        
    def get_child(self):
        """Returns the child tag

        Returns:
            Tag: Returns the child tag of this tag.
        """
        return self.child
    
    def get_next(self):
        """Returns the next tag in the tree.

        Returns:
            Tag: The next tag in the tag tree.
        """
        return self.next
    
    def set_child(self, child):
        """Sets the child of this tag.

        Args:
            child (Tag): This will lead to a lower hierarchy in the tree.
        """
        self.child = child
    
    def set_next(self, next):
        """Sets the next tag in the tree

        Args:
            next (Tag): This tag will have the same hierarchy as the given tag.
        """
        self.next = next
    
# ===========================================================
# ALL DEFINED TAG TYPES BELOW
# ===========================================================

# Last Edit By: Reagan Kelley
# * Edit Details: Initial implementation
class Document(Tag):
    """	Represents a complete document

    Args:
        Tag (Parent Class): A Tag marks a PDF tags making it possible to identify
        content such as headings, lists, tables, etc., and to include 
        alternate text for images. This is an abstract class
        which specific type of tags inherent.
    """
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        return "<document>"
    
class H1(Tag):
    """	Hierarchical headings on levels 1 to 6 (this is 1)

    Args:
        Tag (Parent Class): A Tag marks a PDF tags making it possible to identify
        content such as headings, lists, tables, etc., and to include 
        alternate text for images. This is an abstract class
        which specific type of tags inherent.
    """
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        return "<H1>"

# Last Edit By: Reagan Kelley
# * Edit Details: Initial implementation
class H2(Tag):
    """	Hierarchical headings on levels 1 to 6 (this is 2)

    Args:
        Tag (Parent Class): A Tag marks a PDF tags making it possible to identify
        content such as headings, lists, tables, etc., and to include 
        alternate text for images. This is an abstract class
        which specific type of tags inherent.
    """
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        return "<H2>"

# Last Edit By: Reagan Kelley
# * Edit Details: Initial implementation
class H3(Tag):
    """	Hierarchical headings on levels 1 to 6 (this is 3)

    Args:
        Tag (Parent Class): A Tag marks a PDF tags making it possible to identify
        content such as headings, lists, tables, etc., and to include 
        alternate text for images. This is an abstract class
        which specific type of tags inherent.
    """
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        return "<H3>"

# Last Edit By: Reagan Kelley
# * Edit Details: Initial implementation
class H4(Tag):
    """	Hierarchical headings on levels 1 to 6 (this is 4)

    Args:
        Tag (Parent Class): A Tag marks a PDF tags making it possible to identify
        content such as headings, lists, tables, etc., and to include 
        alternate text for images. This is an abstract class
        which specific type of tags inherent.
    """
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        return "<H4>"

# Last Edit By: Reagan Kelley
# * Edit Details: Initial implementation
class H5(Tag):
    """	Hierarchical headings on levels 1 to 6 (this is 5)

    Args:
        Tag (Parent Class): A Tag marks a PDF tags making it possible to identify
        content such as headings, lists, tables, etc., and to include 
        alternate text for images. This is an abstract class
        which specific type of tags inherent.
    """
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        return "<H5>"

# Last Edit By: Reagan Kelley
# * Edit Details: Initial implementation
class H6(Tag):
    """	Hierarchical headings on levels 1 to 6 (this is 6)

    Args:
        Tag (Parent Class): A Tag marks a PDF tags making it possible to identify
        content such as headings, lists, tables, etc., and to include 
        alternate text for images. This is an abstract class
        which specific type of tags inherent.
    """
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        return "<H6>"

# Last Edit By: Reagan Kelley
# * Edit Details: Initial implementation
class P(Tag):
    """	Ordinary paragraph

    Args:
        Tag (Parent Class): A Tag marks a PDF tags making it possible to identify
        content such as headings, lists, tables, etc., and to include 
        alternate text for images. This is an abstract class
        which specific type of tags inherent.
    """
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        return "<P>"
