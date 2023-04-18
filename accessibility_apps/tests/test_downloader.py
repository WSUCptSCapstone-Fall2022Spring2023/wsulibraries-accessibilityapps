# ===================================================
# File: test_downloader.py
# Author: Trent Bultsma
# Date: 2/28/2023
# Description: Runs the document downloader to download
#   and apply metadata to 10 documents which must be
#   manually verified if it works.
# ==================================================

from utils.database_communication.downloader import DocumentDownloader

downloader = DocumentDownloader("./data/input")
for _ in range(10):
    try:
        document = downloader.get_next_document()
        document._apply_metadata(document.file_path)
        print()
        print("-- Document: " + document.get_filename + " --")
        print("Author " + document.author)
        print("Title " + document.title)
        print("Subject " + document.subject)
        print("Creator " + document.creator)
        print("Keywords " + "; ".join(document.keywords))
        print()
    except Exception as e:
        print("error " + str(e))