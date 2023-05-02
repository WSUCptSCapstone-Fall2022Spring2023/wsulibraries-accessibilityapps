#!/usr/bin/env python

""" This file contains main() which is where our application begins.
It is used for testing purposes because the true application starts
in terminal_application.py.
"""
# * Modules
from pathlib import Path
import os

from utils.accessible_document import AccessibleDocument
from utils.database_communication.downloader import DocumentDownloader


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
# * Edit Details: resolved merge conflicts between main branch and document layout branch.
def main():
    """ This is where our application starts.
    """
    downloader = DocumentDownloader("./data/input")
    # metadata testing
    # for _ in range(10):
    #     try:
    #         document = downloader.get_next_document()
    #         document._apply_metadata(document.file_path)
    #     except Exception as e:
    #         print("error " + str(e))

    example_pdf = DATA_INPUT_DIR.joinpath("example2.pdf")
    doc1 = AccessibleDocument(str(example_pdf), save_objects=True, search_saved_objects=True) # retrieved from .../data/input/example.pdf
    doc1.generate_tags()

if __name__ == "__main__":
    main()