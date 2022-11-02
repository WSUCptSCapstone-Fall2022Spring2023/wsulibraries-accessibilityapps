#!/usr/bin/env python

"""TagTree includes definition of tags, a tag factory, and a tag tree (a data structure that utilizes tags).
"""

# * Modules
import inspect
import sys
from abc import ABC, abstractmethod

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
        self.__data = None
        self.__child = None
        self.__next = None

    @abstractmethod
    def __str__(self):
        pass


    def get_data(self):
        """Returns data contained within this tag.

        Returns:
            _type_: Could be anything
        """
        return self.__data

    def set_data(self, data):
        self.__data = data
        
    def get_child(self):
        """Returns the child tag

        Returns:
            Tag: Returns the child tag of this tag.
        """
        return self.__child
    
    def get_next(self):
        """Returns the next tag in the tree.

        Returns:
            Tag: The next tag in the tag tree.
        """
        return self.__next
    
    def set_child(self, child_tag_name, child_data=None):
        """Sets the child of this tag.

        Args:
            child (Tag): This will lead to a lower hierarchy in the tree.
        """
        self.__child = TagFactory(child_tag_name)
        if child_data is not None:
            self.__child.set_data(child_data)
        return self.__child
    
    def set_next(self, next_tag_name):
        """Sets the next tag in the tree

        Args:
            next (Tag): This tag will have the same hierarchy as the given tag.
        """
        self.__next = TagFactory(next_tag_name)
        return self.__next
    
# ===========================================================
# ALL DEFINED TAG TYPES BELOW
# ===========================================================

# Last Edit By: Reagan Kelley
# * Edit Details: Initial implementation
class DocumentTag(Tag):
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

class TagTree():
    class __cursor():
        def __init__(self, root = TagFactory('<document>')):
            self.__root = root
            self.__loc = self.__root
            self.__parent = []
            self.__sister = []
            self.__local_sister_count = 0
        def get_tag(self):
            return self.__loc
        
        def Up(self):
            """Move the cursor to point up to its parent tag.

            Raises:
                Exception: If at root, will throw error.

            Returns:
                Cursor: The cursor itself will be returned at its new position.
            """
            if(self.__loc == self.__root):
                raise Exception("Up: Out of bounds; currently at root.")
            self.__loc = self.__parent[-1]
            self.__parent.pop()
            while(self.__local_sister_count > 0):
                self.__sister.pop()
            return self
        
        def Down(self):
            """Move the cursor to point down to its child.

            Raises:
                Exception: If cursor has no children, will throw error.

            Returns:
                Cursor: The cursor itself will be returned at its new position.
            """
            if self.__loc.get_child() == None:
                raise Exception("Down: Out of bounds; current tag has no children.")
            self.__parent.append(self.__loc)
            self.__loc = self.__loc.get_child()
            self.__local_sister_count = 0
            return self

        def Next(self):
            """Move the cursor to the next tag in the same level hierarchy.

            Raises:
                Exception: If no more tags in this hierarchy, will throw error.

            Returns:
                Cursor: The cursor itself will be returned at its new position.
            """
            if self.__loc.get_next() == None:
                raise Exception("Next: Out of bounds; current tag has no following tag.")
            self.__sister.append(self.__loc)
            self.__loc = self.__loc.get_next()
            self.__local_sister_count += 1
            return self

        def Back(self):
            """Move the cursor to the left or previous tag in the same level hierarchy.

            Raises:
                Exception: If the first child at this level, will throw error.

            Returns:
                Cursor: The cursor itself will be returned at its new position.
            """
            if(self.__local_sister_count == 0):
                raise Exception("Next: Out of bounds; current tag is the first child.")
            self.__loc = self.__sister[-1]
            self.__sister.pop()
            self.__local_sister_count -= 1
            return self

    def __init__(self, root = '<document>'):
        self.__root = TagFactory(root)
        self.Cursor = self.__cursor(self.__root)
    
    def traverse_tree(self, print_it=True):
        return self.__traverse_tree_helper(self.__root, print_it)
    
    def __traverse_tree_helper(self, current, print_it=True):
        if(current == None):
            return None
        if print_it == True and (current.get_data() != None):
            print(current.get_data())
        self.__traverse_tree_helper(current.get_child(), print_it)
        self.__traverse_tree_helper(current.get_next(), print_it)
