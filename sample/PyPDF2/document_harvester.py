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

def test_image_reader():
    reader = PdfReader("example.pdf")
    page = reader.pages[0]
    count = 0
    for image_file_object in page.images:
        with open(str(count) + image_file_object.name, "wb") as fp:
            fp.write(image_file_object.data)
            count += 1

def main():
    test_image_reader()

if __name__ == "__main__":
    main()