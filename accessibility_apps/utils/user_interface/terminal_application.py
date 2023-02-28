#!/usr/bin/env python

""" This file contains main() which is where our application begins.
"""
# * Modules
from termcolor import colored
from threading import Event, Thread
from colorama import just_fix_windows_console
from utils.accessible_document import AccessibleDocument
from utils.database_communication.downloader import DocumentDownloader
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
        self.auto_processed_docs_count = 0
        self.downloader = DocumentDownloader(INPUT_DIRECTORY)
        self._auto_status = (0,"")
    
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
            if(self.val == 2):
                self.__run_auto_mode()
            if(self.val == 3 and self.exit_number != 3):
                self.__run_accessibility_pipeline(self.doc)
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

        print("\t{}. Run Auto Mode".format(option_number))
        option_number += 1

        if(self.doc is not None and self.doc.is_open()):
            print("\t{}. Run Accessibility Pipeline".format(option_number))
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
    def __export_document(self, document:AccessibleDocument):
        """ Opens a new document to edit.

        Args:
            document (AccessibleDocument): The document to run the pipeline over.
        """
        filename = OUTPUT_DIRECTORY + "/" + document.get_filename()[:-len("pdf")] + "html"
        document.export_document(filename)
    
    # Last Edit By: Reagan Kelley
    # * Edit Details: Initial implementation
    def __run_accessibility_pipeline(self, document:AccessibleDocument):
        """ Run all accessibility pipeline functions.

        Args:
            document (AccessibleDocument): The document to run the pipeline over.
        """
        document.generate_tags()
        document.create_alternative_text()
        document.check_color_contrast()
        self.__export_document(document)

    def __auto_download_and_process_documents(self, finish_event:Event) -> tuple[int, str]:
        """Downloads documents on a loop and runs them through the 
        accesibility pipeline until the passed threading Event is set.

        Returns a tuple of the number of documents processed and the name of the document most recently exported.
        """
        doc_count = 0
        while True:
            try:
                document = self.downloader.get_next_document(delete_on_fail=True)
                self.__run_accessibility_pipeline(document)
                document.delete()
                doc_count += 1
            except:
                pass

            if finish_event.is_set():
                self._auto_status = (doc_count, document.get_filename())
                return

    # TODO improve ui for this function
    def __run_auto_mode(self):
        """Automatically downloads and processes documents."""

        # create and start the thread for processing documents
        pause_event = Event()
        document_processing_thread = Thread(target=self.__auto_download_and_process_documents, args=[pause_event])
        document_processing_thread.start()

        # input loop
        while True:
            print("---------------------------------------------")
            print("WSU Libraries: Automatic Document Processing")
            print("---------------------------------------------")
            print("\t1. Status")
            print("\t2. Pause")

            option = input("> ")
            if(self.__IsInt(option)):
                val = int(option)
                # display the status of the document processing and resume
                if val == 1:
                    print("One moment...")
                    # stop the thread
                    pause_event.set()
                    document_processing_thread.join()
                    # get the data from the thread
                    doc_count_increase, recent_doc = self._auto_status
                    self.auto_processed_docs_count += doc_count_increase
                    # display the status
                    print("Total documents processed: " + str(self.auto_processed_docs_count))
                    print("Most recent document: " + recent_doc)
                    print()
                    # create a new thread and keep going
                    pause_event.clear()
                    document_processing_thread = Thread(target=self.__auto_download_and_process_documents, args=[pause_event])
                    document_processing_thread.start()
                # stop processing documents
                elif val == 2:
                    print("One moment...")
                    # stop the thread
                    pause_event.set()
                    document_processing_thread.join()
                    return
                else:
                    print(colored("Invalid input", "red"))

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
    # NOTE this file must be in the `accessibility_apps` directory for this to run
    main()