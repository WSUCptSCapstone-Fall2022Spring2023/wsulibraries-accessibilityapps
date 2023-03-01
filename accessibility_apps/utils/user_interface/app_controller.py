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
                self.current_document = self.downloader.get_next_document(delete_on_fail=True)
                # updating the label in the thread after the thread has been stopped causes thread locking issues so return to get around these
                if finish_event.is_set():
                    self.current_document.delete()
                    # restore the previous identifier so the document that was just deleted gets re-downloaded 
                    # next time auto processing is resumed to avoid skipping the document when auto mode is paused
                    self.downloader.restore_previous_identifier()
                    return
                self.update_ui_current_auto_document(self.current_document.title)
                self._run_accessibility_pipeline(self.current_document)
                self.current_document.delete()
                self.auto_processed_docs_count += 1
                # same thread locking problem here
                if finish_event.is_set():
                    return
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
        # to update the count just in case the document 
        self.update_ui_current_document_count(self.auto_processed_docs_count)