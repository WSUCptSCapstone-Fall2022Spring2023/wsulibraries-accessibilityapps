# ===================================================
# File: document_harvester.py
# Author: Reagan Kelley
# Date: 10/13/2022
# Description: Currently extracts PDF using PyPDF2.
#              Nothing more.
# ==================================================

from PyPDF2 import PdfReader

def test_reader():
    reader = PdfReader("example.pdf")
    number_of_pages = len(reader.pages)
    page = reader.pages[0]
    text = page.extract_text()
    print(number_of_pages)


def main():
    test_reader()

if __name__ == "__main__":
    main()