#!/usr/bin/env python
#! Run This test from the parent directory or module to avoid relative import errors. 
# python -m unittest -v sample.tests.test_tag_tree

""" Test the Tag Tree Data Structure (unit tests)
"""

# * Modules
import unittest
from utils.transform.TagTree import TagTree

# Last Edit By: Reagan Kelley
# * Edit Details: Initial implementation
class TestTagTree(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()
    
    # Test if tag tree constructor works
    def test_init_tag_tree(self):
        try:
            tree = TagTree()
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    # Test if tag tree can run traverse on newly constructed tree
    def test_init_tag_tree_run(self):
        tree = TagTree()
        tree_data = tree.traverse_tree(print_it=False)
        self.assertEqual(tree_data, "")
    
    # Tests if tag tree cursor get tag works
    def test_cursor_get_tag(self):
        tree = TagTree()
        document_tag = tree.Cursor.get_tag()

        self.assertEqual(str(document_tag), "<document>")

    # Tests if tag tree cursor can create a child, move to it, and access it
    def test_cursor_create_child(self):
        tree = TagTree()
        try:
            tree.Cursor.get_tag().set_child("<H1>")
            header_tag = tree.Cursor.Down().get_tag()
            self.assertEqual(str(header_tag), "<H1>")
        except:
            self.assertTrue(False)
    
    # Tests if tag tree cursor can create a next tag, move to it, and access it
    def test_cursor_move_next(self):
        tree = TagTree()
        tree.Cursor.get_tag().set_child("<H1>")
        tree.Cursor.Down().get_tag().set_next("<H1>", "This is the second header.")
        header_text = tree.Cursor.Next().get_tag().get_data()
        self.assertEqual(header_text, "This is the second header.")
    
    # Tests if tag tree cursor can create new next tags, move to it, and then move back to a previous tag and access it.
    def test_cursor_move_back(self):
        tree = TagTree()
        tree.Cursor.get_tag().set_child("<H1>")
        tree.Cursor.Down().get_tag().set_next("<H1>", "This is the second header.")
        tree.Cursor.Next().get_tag().set_next("<H1>", "This is the third header.")
        
        third_header_text = tree.Cursor.Next().get_tag().get_data()
        second_header_text = tree.Cursor.Back().get_tag().get_data()

        self.assertEqual(third_header_text, "This is the third header.")
        self.assertEqual(second_header_text, "This is the second header.")

    def test_cursor_move_up(self):
        tree = TagTree()
        tree.Cursor.get_tag().set_child("<H1>", "This is the first header.")
        tree.Cursor.Down().get_tag().set_child("<P>")
        
        p_tag = tree.Cursor.Down().get_tag()
        header_text = tree.Cursor.Up().get_tag().get_data()

        self.assertEqual(str(p_tag), "<P>")
        self.assertEqual(header_text, "This is the first header.")

    # Tests a standard use of tag tree where we use the cursor
    # to create it and then traverse tree to read the document in order.
    def test_tree_construction(self):
        tree = TagTree()

        h1 = "The Theory of relativity.\n"
        p1 = "The theory of relativity usually encompasses two interrelated theories by Albert Einstein: " +\
            "special relativity and general relativity, proposed and published in 1905 and 1915, respectively. " +\
            "Special relativity applies to all physical phenomena in the absence of gravity. General relativity " +\
            "explains the law of gravitation and its relation to the forces of nature. It applies to the cosmological " +\
            "and astrophysical realm, including astronomy.\n"

        p2 = "The theory transformed theoretical physics and astronomy during the 20th century, superseding a 200-year-old " +\
            "theory of mechanics created primarily by Isaac Newton. It introduced concepts including 4-dimensional spacetime " +\
            "as a unified entity of space and time, relativity of simultaneity, kinematic and gravitational time dilation, and length " +\
            "contraction. In the field of physics, relativity improved the science of elementary particles and their fundamental interactions, " +\
            "along with ushering in the nuclear age. With relativity, cosmology and astrophysics predicted extraordinary astronomical " +\
            "phenomena such as neutron stars, black holes, and gravitational waves.\n"
        
        h2 = "Development and Acceptance"

        p3 = "Albert Einstein published the theory of special relativity in 1905, building on many theoretical results and " +\
            "empirical findings obtained by Albert A. Michelson, Hendrik Lorentz, Henri Poincaré and others. Max Planck, " +\
            "Hermann Minkowski and others did subsequent work.\n"
        
        p4 = "Einstein developed general relativity between 1907 and 1915, with contributions by many others after 1915. " +\
            "The final form of general relativity was published in 1916.\n"
        
        p5 = 'The term "theory of relativity" was based on the expression "relative theory" (German: Relativtheorie) used ' +\
            'in 1906 by Planck, who emphasized how the theory uses the principle of relativity. In the discussion section of ' +\
            'the same paper, Alfred Bucherer used for the first time the expression "theory of relativity" (German: Relativitätstheorie).\n'
        
        tree.Cursor.get_tag().set_child("<H1>", h1)
        tree.Cursor.Down().get_tag().set_child("<P>", p1)
        tree.Cursor.Down().get_tag().set_next("<P>", p2)
        tree.Cursor.Up().get_tag().set_next("<H1>", h2)
        tree.Cursor.Next().get_tag().set_child("<P>", p3)
        tree.Cursor.Down().get_tag().set_next("<P>", p4)
        tree.Cursor.Next().get_tag().set_next("<P>", p5)
        
        tree_data = tree.traverse_tree(print_it=False)
        self.assertEqual(tree_data, h1 + p1 + p2 + h2 + p3 + p4 + p5)




if __name__ == '__main__':
    unittest.main()