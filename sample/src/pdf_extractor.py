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

divTextSectionsAndFontSize = [] # TODO need to get the size of the font and make sure it is consistent in the div
for div in parsedHtml.findAll('div'):
    # to store a list of tuples of (text, font-style)
    spanTextSectionsAndFont = []
    for span in div.findAll('span'):
        # get the text from the span without indentation or line 
        # breaks or double spaces or trailing/leading whitespace
        spanText = span.get_text().replace("\n", "").replace(
            "\t", "").replace("  ", " ").strip()

        # skip over empty spans
        if spanText == "":
            continue

        # store the text and font style from the span
        spanTextSectionsAndFont.append((spanText, span.attrs['style']))
    print(spanTextSectionsAndFont)
    
    print()

# write to an html file
# (this will not be in the final product, but is 
# helpful to look around in to see what is going on)
with open(TEST_OUTPUT_HTML, 'w', encoding='utf-8') as output_file:
    output_file.write(formattedOutput)