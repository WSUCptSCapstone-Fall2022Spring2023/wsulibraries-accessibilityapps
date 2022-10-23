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

FONT_SIZE_STR = "font-size:"

# will be formatted as a list[tuple(span info, text size)]
divTextInfo = []
for div in parsedHtml.findAll('div'):
    # keep track of the font size in the div
    divFontSize = None

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
        spanAttributes = span.attrs['style']
        spanTextSectionsAndFont.append((spanText, spanAttributes))
    
        # update the font size
        # get the starting index of the font size
        fontSizeIndex = spanAttributes.find(FONT_SIZE_STR)
        if fontSizeIndex != -1:
            # get the end index of the font size
            textWithFontSizeAtStart = spanAttributes[fontSizeIndex + len(FONT_SIZE_STR):]
            fontSizeEndIndex = textWithFontSizeAtStart.find("px")
            if fontSizeEndIndex != -1:
                # get the font size
                fontSize = float(textWithFontSizeAtStart[:fontSizeEndIndex])

                # update the font size and make sure it matches previous font size in the div
                if divFontSize is None:
                    divFontSize = fontSize
                elif fontSize != divFontSize:
                    # font size in the div is not constant
                    # TODO round the font size to the most common one in the div
                    raise Exception("div contains varried font sizes, " +
                        "including at least " + str(fontSize) + " and " + str(divFontSize))

    # skip empty spans
    if len(spanTextSectionsAndFont) == 0:
        continue

    # no font size detected
    if divFontSize is None:
        raise Exception("No font size detected.")

    # add the span data to the div info
    divTextInfo.append((spanTextSectionsAndFont, fontSize))

    # TODO delete these lines later
    print(spanTextSectionsAndFont)
    print()

# write to an html file
# (this will not be in the final product, but is 
# helpful to look around in to see what is going on)
with open(TEST_OUTPUT_HTML, 'w', encoding='utf-8') as output_file:
    output_file.write(formattedOutput)