# ===================================================
# File: pdf_extractor.py
# Author: Trent Bultsma
# Date: 10/12/2022
# Description: Extracts the data from a pdf as html.
# ==================================================

import os
from io import StringIO
from bs4 import BeautifulSoup
from pdfminer.layout import LAParams
from pdfminer.high_level import extract_text_to_fp

TEST_PDF = os.path.dirname(os.path.abspath(__file__)) + "/../../tests/testInput.pdf"
TEST_OUTPUT_HTML = os.path.dirname(os.path.abspath(__file__)) + "/../../tests/testOutput.html"

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
    # keep track of the font sizes in the div, a list of tuples of (font size, text length using that size)
    # used to get a normalized font size for the div, which usually just ends up being the font
    # size for all the spans, but sometimes there are little variations and in that case, the most
    # commonly appearing font size is used for a unified div. TODO may want to investigate this approach later
    fontSizeDistribution = []

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

                fontSizeDistribution.append((fontSize, len(spanText)))
    
    # skip empty spans
    if len(spanTextSectionsAndFont) == 0:
        continue

    # calculate the most commonly appearing font size in the div
    fontSizeDistributionDict = {}
    for fontSize, textLen in fontSizeDistribution:
        if fontSize not in fontSizeDistributionDict.keys():
            fontSizeDistributionDict[fontSize] = 0
        fontSizeDistributionDict[fontSize] += textLen
    divFontSize = sorted(fontSizeDistributionDict.items(), key=lambda sizeLenTup : sizeLenTup[1], reverse=True)[0][0]

    # add the span data to the div info
    divTextInfo.append((spanTextSectionsAndFont, divFontSize))

print(divTextInfo)

# write to an html file
# (this will not be in the final product, but is 
# helpful to look around in to see what is going on)
with open(TEST_OUTPUT_HTML, 'w', encoding='utf-8') as output_file:
    output_file.write(formattedOutput)