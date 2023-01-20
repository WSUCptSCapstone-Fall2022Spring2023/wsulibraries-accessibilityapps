# ===================================================
# File: downloader.py
# Author: Trent Bultsma
# Date: 10/19/2022
# Description: Searches for and downloads documents
#   from the WSU research exchange database.
# ==================================================

import requests
from xml.etree import ElementTree

REPOSITORY_URL = "https://na01.alma.exlibrisgroup.com/view/oai/01ALLIANCE_WSU/request"
OAI_STANDARD_PREFIX = ".//{http://www.openarchives.org/OAI/2.0/}"

class DocumentDownloader():
    """Provides a stream of documents from the WSU research exchange repository."""

    def __init__(self):
        """Initializes the stream of documents."""
        self.resumption_token = None
        self.identifiers = self._get_identifier_batch(initial=True)

    def _get_identifier_batch(self, initial=False) -> list[str]:
        """Gets the next batch of identifiers."""

        # setup the request paramaters
        requestParams = {
            "verb":"ListIdentifiers",
            "metadataPrefix":"esploro",
            "set":"OA_Yes"
        }
        if not initial:

            # a subsequent batch of identifiers requires a resumption 
            # token so return an empty list if there is none because 
            # there will be no identifiers anyway as a result
            if self.resumption_token is None:
                return []

            requestParams = {
                "verb":"ListIdentifiers",
                "resumptionToken":self.resumption_token
            }

        # get the data from the repository
        response = requests.get(url=REPOSITORY_URL, params=requestParams)
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

    def get_next_document(self):
        """Gets the next document from the repository."""

        # refill the identifier list if it is empty
        if len(self.identifiers) == 0:
            self.identifiers = self._get_identifier_batch()
        
        # at this point, we have run out of documents
        if len(self.identifiers) == 0:
            return None

        # TODO download the document with the given identifier
        # but for now just return the identifier
        return self.identifiers.pop()

if __name__ == "__main__":
    downloader = DocumentDownloader()
    for _ in range(15):
        print(downloader.get_next_document())