# ===================================================
# File: downloader.py
# Author: Trent Bultsma
# Date: 10/19/2022
# Description: Searches for and downloads documents
#   from the WSU research exchange database.
# ==================================================

import requests
from xml.etree import ElementTree
from utils.accessible_document import AccessibleDocument

REPOSITORY_URL = "https://na01.alma.exlibrisgroup.com/view/oai/01ALLIANCE_WSU/request"
OAI_STANDARD_PREFIX = ".//{http://www.openarchives.org/OAI/2.0/}"
LIBRARY_STANDARD_PREFIX = ".//{http://www.loc.gov/MARC21/slim}"

class DocumentDownloader():
    """Provides a stream of documents from the WSU research exchange repository."""

    def __init__(self, download_path:str):
        """Initializes the stream of documents.
        
        Args:
            download_path (str): the path of the folder to download new documents to.
        """
        self.download_path = download_path
        self.resumption_token = None
        self.identifiers = self._get_identifier_batch()

    def _get_identifier_batch(self) -> list[str]:
        """Returns the next batch of identifiers."""

        # setup the request paramaters
        request_params = {
            "verb":"ListIdentifiers",
            "metadataPrefix":"esploro",
            "set":"OA_Yes"
        }

        # when there is a resumption token set, go off of that 
        # instead of pulling from the start of the repository
        if self.resumption_token is not None:
            request_params = {
                "verb":"ListIdentifiers",
                "resumptionToken":self.resumption_token
            }

        # get the data from the repository
        response = requests.get(url=REPOSITORY_URL, params=request_params)
        data = ElementTree.fromstring(response.content)

        # update the resumption token for getting the next batch
        try:
            self.resumption_token = data.find(OAI_STANDARD_PREFIX + "resumptionToken").text
        except:
            self.resumption_token = None

        # create a list of the identifiers from the data
        identifiers = []
        for id in data.findall(OAI_STANDARD_PREFIX + "identifier"):
            identifiers.append(id.text)

        return identifiers

    def _get_next_identifier(self) -> str:
        """Gets the identifier for the next document from the repository."""

        # refill the identifier list if it is empty
        if len(self.identifiers) == 0:
            self.identifiers = self._get_identifier_batch()
        
        # at this point, we have run out of documents
        if len(self.identifiers) == 0:
            return None

        return self.identifiers.pop()

    def get_next_document(self, delete_on_fail=False):
        """Returns a Document object for the next document in the repository.
        
        Args:
            delete_on_fail (bool): Whether to delete documents that failed to open.
        """
        
        # get the next document identifier and setup the request to grab using it
        document_identifier = self._get_next_identifier()
        request_params = {
            "verb":"GetRecord",
            "identifier":document_identifier,
            "metadataPrefix":"esploro"
        }
        if document_identifier is None:
            return None

        # get the data from the repository
        response = requests.get(url=REPOSITORY_URL, params=request_params)
        data = ElementTree.fromstring(response.content)

        # download the document
        try:
            download_url = data.find(LIBRARY_STANDARD_PREFIX + "file.download.url").text
            file_name = data.find(LIBRARY_STANDARD_PREFIX + "file.name").text
        except:
            # cannot create a document if the download url is not found
            return None
        document_data = requests.get(download_url, allow_redirects=True)
        document_download_path = self.download_path + "/" + file_name
        open(document_download_path, "wb").write(document_data.content)

        # get document metadata

        # get the title of the document
        title = ""
        try:
            title = data.find(LIBRARY_STANDARD_PREFIX + "title").text
        except:
            pass

        # get the author(s) of the document
        authors_list = []
        for author in data.findall(LIBRARY_STANDARD_PREFIX + "creatorname"):
            authors_list.append(author.text)
        authors = ",".join(authors_list)

        # get the description of the document
        description = ""
        try:
            description = data.find(LIBRARY_STANDARD_PREFIX + "description.abstract").text
        except:
            pass

        document = AccessibleDocument(document_download_path, delete_on_fail)
        document.set_metadata(authors, title, description)
        return document