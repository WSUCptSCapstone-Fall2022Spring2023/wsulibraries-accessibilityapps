# ===================================================
# File: pdf_extractor.py
# Author: Trent Bultsma
# Date: 10/12/2022
# Description: Extracts the data from a pdf as html.
# ==================================================

import os
from bs4 import BeautifulSoup

TEST_PDF = os.path.dirname(os.path.abspath(__file__)) + "/../../tests/testInput.pdf"
TEST_OUTPUT_HTML = os.path.dirname(os.path.abspath(__file__)) + "/../../tests/testOutput.html"

from io import StringIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

# read the pdf
output_string = StringIO()
with open(TEST_PDF, 'rb') as fin:
    extract_text_to_fp(fin, output_string, laparams=LAParams(),output_type='html', codec=None)

# parse the html file
parsedHtml = BeautifulSoup(output_string.getvalue(), 'html.parser')

# format the parsed html file
formattedOutput = parsedHtml.prettify()

# write to an html file
with open(TEST_OUTPUT_HTML, 'w', encoding='utf-8') as output_file:
    output_file.write(formattedOutput)