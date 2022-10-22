#!/usr/bin/env python

""" This file contains main() which is where our application begins.
"""
# * Modules
from src.accessible_document import AccessibleDocument

# ? VSCode Extensions Used:
# ?     - Better Comments
# ?     - autoDocstring

__author__ = "Trent Bultsma, Reagan Kelley, Marisa Loyd"
__copyright__ = "N/A"
__credits__ = ["Trent Bultsma", "Reagan Kelley", "Marisa Loyd"]
__license__ = "GNU GENERAL PUBLIC LICENSE"
__version__ = "3.0.0"
__maintainer__ = "Trent Bultsma"
__email__ = "trent.bultsma@wsu.edu"
__status__ = "Development"

# Last Edit By: Reagan Kelley
# * Edit Details: Initial implementation
def main():
    """ This is where our application starts.
    """
    doc1 = AccessibleDocument("example.pdf") # retrieved from .../data/input/example.pdf
    doc1.generate_tags()
    doc1.create_alternative_text()
    doc1.check_color_contrast()

if __name__ == "__main__":
    main()