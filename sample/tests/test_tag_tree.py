#!/usr/bin/env python
#! Run This test from the parent directory or module to avoid relative import errors. 

""" Test the Tag Tree Data Structure
"""

# * Modules
import unittest
from ..utils.TagTree import TagTree

# Last Edit By: Reagan Kelley
# * Edit Details: Initial implementation
class TestTagTree(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_init_tag_tree(self):
        """Tests if tag tree can be constructed without errors.
        """
        try:
            tree = TagTree()
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    
    def test_default2(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()