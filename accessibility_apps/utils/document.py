#!/usr/bin/env python

""" This file contains the Document Class
"""

# * Modules
import os
from sys import platform
from yake import KeywordExtractor
from PyPDF2 import PdfReader, PdfWriter
from typing import List
from pathlib import Path
import pickle

from utils.harvest.pdf_extractor import export_to_html
from utils.export.document_exporter import export_document
from utils.harvest.document_harvester import OUTPUT_DIRECTORY
from utils.harvest.pdf_extractor import extract_paragraphs_and_fonts_and_sizes

try:
    from utils.harvest.document_layout import document_layout
    skip_layout_parser = False
except ImportError as e:
    print("Warning [document_layout] - Caught Error : {}".format(e))
    skip_layout_parser = True

# find or create directory to save objects through pickle
save_dir = Path(os.path.realpath(os.path.dirname(__file__))).parent.parent.absolute().joinpath('data')

if not save_dir.exists():
    raise FileNotFoundError(save_dir)

save_dir = save_dir.joinpath("saved_objects")
if not save_dir.exists():
    save_dir.mkdir() 


# Last Edit By: Trent Bultsma
# * Edit Details: Use the pdf_extractor to extract and export data.
class Document:
    """Document is a class that allows us to alter and manipulate documents
    """
    # Last Edit By: Trent Bultsma
    # * Edit Details: Use the pdf_extractor to extract and export data.
    def __init__(self, file_path:str, delete_on_fail=False, save_objects = False, search_saved_objects=False):
        """Create instance of Document class object.

        Args:
            file_path (string): The path name of the PDF that will be processed.
            delete_on_fail (bool): Whether to delete the document at the specified path if it fails to open.
        """
        self.file_path = file_path
        self.paragraphs = []
        self.page_count = 0

        # setup metadata values
        self.author = ""
        self.title = ""
        self.subject = ""
        self.creator = "WSU Library Accessibilty App"
        self.keywords = []

        # for checking when the file is deleted
        self.deleted = False

        self.save = save_objects

        # for saving pickle objects 
        self.save_dir = save_dir.joinpath(self.get_filename().split('.')[0])
        if not self.save_dir.exists():
            self.save_dir.mkdir()
            self.search_save_objects = False # if not created, don't bother looking
        else:
            self.search_save_objects = search_saved_objects

        # try to open the document
        try:
            self._open_document(file_path)
        except Exception as e:
            # if it doesn't work, delete the document if specified
            if delete_on_fail:
                self.delete()
                return
            else:
                raise e

    def set_metadata(self, author, title, subject):
        """ Sets the Document metadata values as specified.
        
        Args:
            author (string): The author of the document.
            title (string): The title of the document.
            subject (string): A small description of what the document is about.
            keywords (list): A list of important words in the document.
        """
        self.author = author
        self.title = title
        self.subject = subject
    
    # Last Edit By: Trent Bultsma
    # * Edit Details: Use the pdf_extractor to extract and export data.
    def _open_document(self, file_path:str):
        """ Opens a PDF for editing. It should only be called in the constructor.

        Args:
            file_path (string): The path name of the PDF that will be processed.
        """

        # make sure the file is a pdf
        if file_path is not None and file_path.lower().endswith(".pdf"):
            
            # extract the data
            self.batch_paragraphs = extract_paragraphs_and_fonts_and_sizes(file_path)
            self.page_count = len(self.paragraphs)
            
            self.paragraphs = [paragraph for batch in self.batch_paragraphs for paragraph in batch] 

            # look for layout blocks in saved objects first (if option is true)
            self.layout_blocks = []
            if self.search_save_objects:
                if self.save_dir.joinpath('layout_blocks.obj').exists():
                    ifile = open(str(self.save_dir.joinpath('layout_blocks.obj')), 'rb') 
                    self.layout_blocks = pickle.load(ifile)
            
            # if no layout blocks --> use layout parser
            if len(self.layout_blocks) == 0:
                if platform == "linux" or platform == "linux2":
                    # using self.paragraphs to validate and optimize layout results. Creates a list of (p.font_size as int, p.raw_text)
                    preprocessed_paragraphs = [[(int(''.join(c for c in p.font_size if c.isdigit())), p.get_raw_text()) for p in batch] for batch in self.batch_paragraphs]
                    self.layout_blocks : List[str, str] = document_layout(self.file_path, preprocessed_paragraphs, debug=False)
                else:
                    print("Layout Parsing Skipped: Non-Linux distributions not yet supported...")
                    self.layout_blocks = []
            
                # if save option is true --> Save to saved objects
                if self.save:
                    ofile = open(str(self.save_dir.joinpath('layout_blocks.obj')), 'wb') 
                    pickle.dump(self.layout_blocks, ofile)

            for type, data in self.layout_blocks:
                print (f"[{type}]")
                print(data, end='\n\n')
            quit()

            # calculate the keywords
            self.keywords = self._calculate_keywords()

        else:
            raise ValueError("Invalid file path, must be a pdf file")
        

    def is_open(self):
        """ Returns true if there is a file open for editing.

        Returns:
            Bool: If a file is opened.
        """
        return not self.deleted and self.file_path != None

    # Last Edit By: Trent Bultsma
    # * Edit Details: Use the pdf_extractor to extract and export data.
    def export_document(self, file_path:str=None):
        """ Transforms the metadata from codable data structures back into a usable and readable
            format: HTML

            Args:
            file_path (string): The path name of the html doc to be exported.
        """
        # TODO use the paragraph objects to write a better exporting function that actually goes to a pdf
        # (this is just a temporary exporting function before we get that working)

        # use the file path of the input file but change the extension to .html instead of .pdf if file path not specified
        if file_path is None:
            file_path = self.file_path[:-len("pdf")] + "html"

        # export the document
        export_to_html(self.paragraphs, file_path)

        # convert to pdf
        export_document(self.get_filename()[:-len("pdf")] + "html")

        # remove the html document
        os.remove(file_path)

        # add metadata to the pdf
        self._apply_metadata(OUTPUT_DIRECTORY + "/" + self.get_filename())

    # Last Edit By: Trent Bultsma
    # * Edit Details: Use the pdf_extractor to extract and export data.
    def get_filename(self):
        """Gets the title of the document

        Returns:
            string: document title
        """
        if self.file_path is None:
            return None
        return os.path.basename(self.file_path)

    def delete(self):
        """Deletes the open document."""
        os.remove(self.file_path)
        self.deleted = True

    def _apply_metadata(self, export_file_path:str):
        """Applies the document metadata to the inputted pdf file path.
        
            Args:
            export_file_path (str): the path of the pdf file to write the metadata to.
        """
        # make sure the file is a pdf
        if not export_file_path.lower().endswith(".pdf"):
            raise ValueError("Must be a pdf file")
        
        # setup the reader and writer
        reader = PdfReader(export_file_path)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        # add the metadata to the writer
        writer.add_metadata(
            {
                "/Author" : self.author,
                "/Title" : self.title,
                "/Subject" : self.subject,
                "/Creator" : self.creator,
                "/Keywords" : "; ".join(self.keywords)
            }
        )

        # overwrite the file now with metadata
        with open(export_file_path, "wb") as file:
            writer.write(file)

    def _calculate_keywords(self) -> str:
        """ Returns a list of key words for the document. This is done 
        by looking through the paragraphs of the document and determining 
        key words by looking at frequency and uniqueness of each word.
        """
        # preprocess the text from the current document
        document_raw_text = " . ".join([paragraph.get_raw_text().lower() for paragraph in self.paragraphs])

        # extract the key phrases from the text
        keywords_and_scores = []
        for phrase_len in range(1,4):
            # check for key phrases of length 1 to 3
            extractor = KeywordExtractor(top=5, n=phrase_len)
            keywords_and_scores += extractor.extract_keywords(document_raw_text)

        # remove duplicates
        keywords_and_scores = list(set(keywords_and_scores))
        # sort the key phrases so the "most important" one will be first
        keywords_and_scores.sort(key=lambda keyword_score_tuple: keyword_score_tuple[1])
        # only include the top 5 key phrases
        keywords = list(map(lambda keyword_score_tuple: keyword_score_tuple[0].title(), keywords_and_scores))[0:5]
        
        # TODO need to remove words that are part of tables from the paragraphs so that labels do not become key phrases
        return keywords