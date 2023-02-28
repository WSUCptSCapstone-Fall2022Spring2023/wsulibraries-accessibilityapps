# ===================================================
# File: app_controller.py
# Author: Trent Bultsma
# Date: 2/28/2022
# Description: Defines a back end controller for the
#   user interface for the accessibility app, used
#   to control the functional workings of the app.
# ==================================================

from threading import Event, Thread
from utils.accessible_document import AccessibleDocument
from utils.database_communication.downloader import DocumentDownloader
from utils.harvest.document_harvester import INPUT_DIRECTORY, OUTPUT_DIRECTORY

class AccessibilityAppController():
    """Serves as a bridge between the user interface of the accessibility application and the back end functionality."""

    def __init__(self):
        self.current_document = None
        self.auto_processed_docs_count = 0
        self.downloader = DocumentDownloader(INPUT_DIRECTORY)
        self.update_ui_current_auto_document = lambda document_name: None
        self.update_ui_current_document_count = lambda document_count: None

    def _export_document(self, document:AccessibleDocument):
        """Exports a document object to a pdf file.

        Args:
            document (AccessibleDocument): The document to export.
        """
        filename = OUTPUT_DIRECTORY + "/" + document.get_filename()[:-len("pdf")] + "html"
        document.export_document(filename)
    
    def _run_accessibility_pipeline(self, document:AccessibleDocument):
        """Run all accessibility pipeline functions over a given document.

        Args:
            document (AccessibleDocument): The document to run the accessibility pipeline over.
        """
        document.generate_tags()
        document.create_alternative_text()
        document.check_color_contrast()
        # TODO add more accessibility functions here
        self._export_document(document)

    def _auto_download_and_process_documents(self, finish_event:Event):
        """Downloads documents on a loop and runs them through the accessibility pipeline until the passed threading `Event` is set."""
        while True:
            try:
                # TODO figure out why the ui callbacks aren't working
                self.current_document = self.downloader.get_next_document(delete_on_fail=True)
                self.update_ui_current_auto_document(self.current_document.title)
                self._run_accessibility_pipeline(self.current_document)
                self.current_document.delete()
                self.auto_processed_docs_count += 1
                self.update_ui_current_document_count(self.auto_processed_docs_count)
            except:
                pass

            if finish_event.is_set():
                return

    def start_auto_mode(self):
        """Starts the automatic processing of documents."""
        self.auto_mode_pause_event = Event()
        self.auto_document_processing_thread = Thread(target=self._auto_download_and_process_documents, args=[self.auto_mode_pause_event])
        self.auto_document_processing_thread.start()

    def stop_auto_mode(self):
        """Stops the automatic processing of documents."""
        self.auto_mode_pause_event.set()
        self.auto_document_processing_thread.join()






    # TODO this needs to be redone completely
    def _run_auto_mode(self):
        """Automatically downloads and processes documents."""

        # create and start the thread for processing documents
        pause_event = Event()
        document_processing_thread = Thread(target=self._auto_download_and_process_documents, args=[pause_event])
        document_processing_thread.start()

        # input loop
        while True:
            print("---------------------------------------------")
            print("WSU Libraries: Automatic Document Processing")
            print("---------------------------------------------")
            print("\t1. Status")
            print("\t2. Pause")

            option = input("> ")
            if(self._IsInt(option)):
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
                    document_processing_thread = Thread(target=self._auto_download_and_process_documents, args=[pause_event])
                    document_processing_thread.start()
                # stop processing documents
                elif val == 2:
                    print("One moment...")
                    # stop the thread
                    pause_event.set()
                    document_processing_thread.join()
                    return
                else:
                    print("Invalid input", "red")