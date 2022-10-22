#!/usr/bin/env python

""" This file contains main() which is where our application begins.
"""
# * Modules
from asyncio.windows_events import NULL
from operator import truth
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
class TerminalApplication():
    """Command line interface for Accessible Document application.
    """

    # Last Edit By: Reagan Kelley
    # * Edit Details: Initial implementation
    def __init__(self):
        """ Create new instance of TerminalApplication object.
        """
        self.doc = AccessibleDocument()
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
            
            if(self.response == 1):
                self.__get_new_document()
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
        print("Current File: {}".format("Nothing Open" if not self.doc.IsOpen() else self.doc.get_filename()))
        print("---------------------------------------------")
        option_number = 1
        
        print("\t{}. Open new file".format(option_number))
        option_number += 1

        print("\t{}. Exit".format(option_number))
        return option_number
    
    # Last Edit By: Reagan Kelley
    # * Edit Details: Initial implementation
    def __get_new_document(self):
        """ Opens a new document to edit.
        """
        filename = input("\tName of Document (local to data): ")
        self.doc.open_document(filename=filename)


# Last Edit By: Reagan Kelley
# * Edit Details: Initial implementation
def main():
    """ This is where our application starts.
    """
    app = TerminalApplication()
    while(app.IsRunning()):
        app.Interact()
    

if __name__ == "__main__":
    main()