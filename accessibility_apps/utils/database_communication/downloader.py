# ===================================================
# File: downloader.py
# Author: Trent Bultsma
# Date: 10/19/2022
# Description: Searches for and downloads documents
#   from the WSU research exchange database.
# ==================================================

import requests
from xml.etree import ElementTree

response = requests.get(
    url="https://na01.alma.exlibrisgroup.com/view/oai/01ALLIANCE_WSU/request",
    params=
        {
            "verb":"ListIdentifiers",
            "metadataPrefix":"esploro",
            "set":"OA_Yes"
        }
    )

data = ElementTree.fromstring(response.content)
for id in data.findall(".//{http://www.openarchives.org/OAI/2.0/}identifier"):
    print(id.text)

resumptionToken = data.find(".//{http://www.openarchives.org/OAI/2.0/}resumptionToken").text

# could loop this more times to get more identifiers
for _ in range(3):
    response = requests.get(
        url="https://na01.alma.exlibrisgroup.com/view/oai/01ALLIANCE_WSU/request",
        params=
            {
                "verb":"ListIdentifiers",
                "resumptionToken":resumptionToken
            }
        )

    data = ElementTree.fromstring(response.content)
    for id in data.findall(".//{http://www.openarchives.org/OAI/2.0/}identifier"):
        print(id.text)