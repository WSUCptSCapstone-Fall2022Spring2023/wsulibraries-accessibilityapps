# ===================================================
# File: bulk_word_harvester.py
# Author: Trent Bultsma
# Date: 2/2/2023
# Description: Harvests the text from many pdf files
#       from the research exchange repository and 
#       writes them to a .txt file for processing.
# ==================================================

import os
from utils.database_communication.downloader import DocumentDownloader

# get the directory of this file
current_dir = os.path.dirname(os.path.abspath(__file__))

words = []
downloader = DocumentDownloader(current_dir + "/../../../data/input")

# go through a few of the documents
for i in range(100):
    try:
        # grab the words from the document and store them
        document = downloader.get_next_document(True)
        if document is not None and not document.deleted:
            for paragraph in document.paragraphs:
                words.append(paragraph.get_raw_text())
            document.delete()
            print(str(i) + " - pass")
        else:
            print(str(i) + " - skip")
    except Exception as e:
        print(str(i) + " - fail " + str(e))

# write all the words to a text file
with open(current_dir + "/../../../data/output/bulk_words.txt", "w", encoding='utf-8') as file:
    file.writelines(words)