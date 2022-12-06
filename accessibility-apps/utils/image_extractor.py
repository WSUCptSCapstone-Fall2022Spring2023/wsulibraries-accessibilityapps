# ===================================================
# File: image_extractor.py
# Author: Trent Bultsma
# Date: 11/8/2022
# Description: Extracts the images from a pdf.
# ==================================================

import os
from PyPDF2 import PdfReader

TEST_PDF = os.path.dirname(os.path.abspath(__file__)) + '/../../tests/testInput.pdf'

reader = PdfReader(TEST_PDF)
count = 0
for page in reader.pages:
    for image_file_object in page.images:
        with open(TEST_PDF[:-4] + "image" + str(count) + ".png", "wb") as fp:
            fp.write(image_file_object.data)
            count += 1