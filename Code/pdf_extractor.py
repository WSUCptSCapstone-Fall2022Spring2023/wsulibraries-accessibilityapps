# ===================================================
# File: pdf_extractor.py
# Author: Trent Bultsma
# Date: 10/12/2022
# Description: Extracts the data from a pdf as html.
# ==================================================

import os

TEST_PDF = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/testInput.pdf"
TEST_OUTPUT_HTML = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/testOutput.html"

from io import StringIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

output_string = StringIO()
with open(TEST_PDF, 'rb') as fin:
    extract_text_to_fp(fin, output_string, laparams=LAParams(),output_type='html', codec=None)

with open(TEST_OUTPUT_HTML, 'w', encoding='utf-8') as output_file:
    output_file.write(output_string.getvalue())

# TODO how do we get the images?