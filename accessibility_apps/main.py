#!/usr/bin/env python

""" This file contains main() which is where our application begins.
"""
# * Modules
from pathlib import Path
import os

from utils.accessible_document import AccessibleDocument

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

DATA_INPUT_DIR = Path(os.path.realpath(os.path.dirname(__file__))).parent.absolute().joinpath("data").joinpath("input")

# Last Edit By: Reagan Kelley
# * Edit Details: Initial implementation
def main():
    """ This is where our application starts.
    """

    example_pdf = DATA_INPUT_DIR.joinpath("example.pdf")
    doc1 = AccessibleDocument(str(example_pdf)) # retrieved from .../data/input/example.pdf
    doc1.generate_tags()

if __name__ == "__main__":
    main()