# ===================================================
# File: app_controller.py
# Author: Trent Bultsma
# Date: 2/28/2022
# Description: Defines a back end controller for the
#   user interface for the accessibility app, used
#   to control the functional workings of the app.
# ==================================================

import os
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
            
    def _process_local_folder(self, folder:str, metadata_csv_name:str, progress_update_callback, finished_callback):
        """Automatically processes documents in a specified folder with metadata given in a csv file.
        
        Args:
            folder (str): The folder to process documents from.
            progress_update_callback (function): The function to call to update the progress for the processing.
            finished_callback (function): The function to call to update the ui signifying that the job is done.
        """
        # TODO
        # read the csv to get the metadata and names of files

        # loop through the files from the csv and process each one of them

        # broadcast that the folder processing finished
        finished_callback()

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

    def process_local_folder(self, folder:str, progress_update_callback, finished_callback):
        """Automatically processes documents in a specified folder with metadata given in a csv file.
        
        Args:
            folder (str): The folder to process documents from.
            progress_update_callback (function): The function to call to update the progress for the processing.
            finished_callback (function): The function to call to update the ui signifying that the job is done.
        """
        # locate the metadata csv
        file_list = os.listdir(folder)
        csv_file_count = 0
        metadata_csv_name = None
        for file_name in file_list:
            if file_name.lower().endswith(".csv"):
                csv_file_count += 1
                metadata_csv_name = folder + "/" + file_name
        if csv_file_count != 1:
            raise Exception("There are " + str(csv_file_count) + " csv files in the folder. There should be exactly 1 and it should contain metadata information for the pdf files.")
        
        folder_processing_thread = Thread(target=self._process_local_folder, args=[folder, metadata_csv_name, progress_update_callback, finished_callback])
        folder_processing_thread.start()