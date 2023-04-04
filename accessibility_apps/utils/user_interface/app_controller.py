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
from utils.harvest.metadata_csv_reader import read_metadata_csv
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
        # read the csv to get the metadata and names of files
        all_files_metadata = read_metadata_csv(metadata_csv_name)

        # get the number of documents needing to be processed
        num_of_documents = len(all_files_metadata.keys())

        # loop through the files from the csv and process each one of them
        for file_name, metadata in all_files_metadata.items():
            document = AccessibleDocument(folder + "/" + file_name, True)

            # set the metadata for the file

            # get the author(s)
            orgainzation = metadata.get("OCREATOR_ORGANIZATION")
            first_names = metadata.get("CREATOR_FAMNAME")
            last_names = metadata.get("CREATOR_GIVNAME")
            author = ""
            if orgainzation is not None:
                author = ", ".join(orgainzation)
            if first_names is not None and last_names is not None and len(first_names) == len(last_names):
                names = ", ".join([first_name + " " + last_name for (first_name, last_name) in zip(first_names, last_names)])
                if author == "":
                    author = names
                else:
                    author += ", " + names

            # get the title
            title = metadata.get("ASSET_TITLE")
            # either set it to be an empty string or the first element from the 
            # metadata list since there should only be one title so grab the first one
            title = "" if title is None else title[0]

            # get the subject 
            subject = metadata.get("ASSET_ABSTRACT")
            # either set it to be an empty string or the first element from the 
            # metadata list since there should only be one subject so grab the first one
            subject = "" if subject is None else subject[0]

            document.set_metadata(author, title, subject)

            # process the document
            self._run_accessibility_pipeline(document)

            # update the progress bar each time a document is completed
            progress_update_callback(100/num_of_documents)

        # broadcast that the folder processing finished
        finished_callback()

    def _process_document_id_list(self, id_list, progress_update_callback, finished_callback):
        """Processes documents within the id list.
        
        Args:
            id_list (list): A list of ids to process their corresponding documents.
            progress_update_callback (function): The function to call to update the progress for the processing.
            finished_callback (function): The function to call upon finishing the processing.
        """
        # setup variables for tracking progress
        num_documents = len(id_list)
        processed_documents = 0

        # for incrementing the number of documents processed
        def single_document_processing_finished(_ = None):
            nonlocal processed_documents
            processed_documents += 1
            progress_update_callback(100/num_documents)

            # end the processing once all the documents are done 
            if num_documents == processed_documents:
                finished_callback()

        # call all the threads to start processing
        for id in id_list:
            self.process_document_by_id(id, single_document_processing_finished)

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

    def process_document_by_id(self, id:str, finished_callback):
        """Processes a document by searching for it given the id.
        
        Args:
            id (str): The id number of the document.
            finished_callback (function): The function to call after the document has been processed.
        """
        # define a function to download and process the document
        def run_document_processing():
            # don't crash when a non-pdf is processed, just pass over it
            try:
                document = self.downloader.get_next_document(True, id)
                # make sure the document id is valid
                if document is None:
                    finished_callback("Error, document id incorrect")
                    return
                self._run_accessibility_pipeline(document)
                document.delete()
            except:
                pass
            finished_callback()

        # start the processing on a thread so it doesn't freeze the ui
        document_processing_thread = Thread(target=run_document_processing)
        document_processing_thread.start()

    def process_document_id_list(self, id_list_file_name: str, progress_update_callback, finished_callback):
        """Processes through a list of documents by there.
        
        Args:
            id_list_file_name (str): The name of a file containing the ids of documents to process.
            progress_update_callback (function): The function to call to update the progress for the processing.
            finished_callback (function): The function to call upon finishing the processing.
        """
        # get the list of ids from the file
        id_list = []
        with open(id_list_file_name, "r") as id_list_file:
            id_list = id_list_file.readlines()

        # start the thread to process the documents
        folder_processing_thread = Thread(target=self._process_document_id_list, args=[id_list, progress_update_callback, finished_callback])
        folder_processing_thread.start()