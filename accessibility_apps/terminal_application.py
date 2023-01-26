#!/usr/bin/env python

""" This file contains main() which is where our application begins.
"""
# * Modules
from colorama import just_fix_windows_console
from termcolor import colored
from utils.accessible_document import AccessibleDocument
from utils.harvest.document_harvester import INPUT_DIRECTORY, OUTPUT_DIRECTORY


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
# * Edit Details: Use the pdf_extractor to get data from the pdf.
class TerminalApplication():
    """Command line interface for Accessible Document application.
    """

    # Last Edit By: Reagan Kelley
    # * Edit Details: Initial implementation
    def __init__(self):
        """ Create new instance of TerminalApplication object.
        """
        self.doc = None
        self.val = 0
        self.exit_number = 2
    
    # Last Edit By: Reagan Kelley
    # * Edit Details: Initial implementation
    def __IsInt(self, response):
        try:
            self.val = int(response)
            return True
        except:
            return False
    
    # Last Edit By: Reagan Kelley
    # * Edit Details: Initial implementation
    def IsRunning(self):
        """Returns true if the user has not yet chosen to exit.

        Returns:
            Bool: If application is running.
        """
        return self.val != self.exit_number

    # Last Edit By: Reagan Kelley
    # * Edit Details: Initial implementation
    def Interact(self):
        """ Proceed to next logical frame within application.
            1. Get User input
            2. Perform proper response.
        """
        self.exit_number = self.__print_menu()
        self.response = input("> ")

        if(self.__IsInt(self.response)):
            self.val = int(self.response)
            if(self.val == 1):
                self.__get_new_document()
            if(self.val == 2 and self.exit_number != 2):
                self.__run_accessibility_pipeline()
            if(self.val == 3 and self.exit_number != 3):
                self.__export_document()
        print("")

    # Last Edit By: Reagan Kelley
    # * Edit Details: Initial implementation
    def __print_menu(self):
        """Print the main menu and options.

        Returns:
            int: The exit option number.
        """
        print("---------------------------------------------")
        print("WSU Libraries: Document Transformer")
        print("Current File: ", end='')
        print(colored("{}".format("Nothing Open" if self.doc is None else self.doc.get_filename()), 'magenta'))
        print("---------------------------------------------")
        option_number = 1
        
        print("\t{}. Open new file".format(option_number))
        option_number += 1

        if(self.doc is not None and self.doc.is_open()):
            print("\t{}. Run Accessibility Pipeline".format(option_number))
            option_number += 1
            print("\t{}. Export File".format(option_number))
            option_number += 1

        print("\t{}. Exit".format(option_number))
        return option_number
    
    # Last Edit By: Trent Bultsma
    # * Edit Details: Use the pdf_extractor to get data from the pdf.
    def __get_new_document(self):
        """ Opens a new document to edit.
        """
        filename = INPUT_DIRECTORY + "/" + input("Name of Document (local path): \n{}\\".format(INPUT_DIRECTORY))
        try:
            self.doc = AccessibleDocument(filename)
        except:
            print(colored("No file opened: Invalid Path", "red"))

    # Last Edit By: Trent Bultsma
    # * Edit Details: Change document exporting to go to the output directory.
    def __export_document(self):
        """ Opens a new document to edit.
        """
        filename = OUTPUT_DIRECTORY + "/" + self.doc.get_filename()[:-len("pdf")] + "html"
        self.doc.export_document(filename)
    
    # Last Edit By: Reagan Kelley
    # * Edit Details: Initial implementation
    def __run_accessibility_pipeline(self):
        """ Run all accessibility pipeline functions.
        """
        self.doc.generate_tags()
        self.doc.create_alternative_text()
        self.doc.check_color_contrast()
        self.__export_document()

# Last Edit By: Reagan Kelley
# * Edit Details: Initial implementation
def main():
    """ This is where our application starts.
    """
    just_fix_windows_console()
    app = TerminalApplication()
    while(app.IsRunning()):
        app.Interact()

if __name__ == "__main__":
    main()