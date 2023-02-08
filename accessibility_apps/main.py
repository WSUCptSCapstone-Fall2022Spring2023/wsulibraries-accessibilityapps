#!/usr/bin/env python

""" This file contains main() which is where our application begins.
It is used for testing purposes because the true application starts
in terminal_application.py.
"""
# * Modules
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

# Last Edit By: Trent Bultsma
# * Edit Details: Metadata adding testing
def main():
    """ This is where our application starts.
    """
    # metadata testing
    downloader = DocumentDownloader("./data/input")
    for _ in range(10):
        try:
            document = downloader.get_next_document()
            document._apply_metadata(document.file_path)
        except Exception as e:
            print("error " + str(e))

if __name__ == "__main__":
    main()