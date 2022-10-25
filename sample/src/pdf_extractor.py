# ===================================================
# File: pdf_extractor.py
# Author: Trent Bultsma
# Date: 10/12/2022
# Description: Extracts the data from a pdf as html.
# ==================================================

# imports
import os
from io import StringIO
from bs4 import BeautifulSoup
from pdfminer.layout import LAParams
from pdfminer.high_level import extract_text_to_fp

# constants
TEST_PDF = os.path.dirname(os.path.abspath(__file__)) + '/../../tests/testInput.pdf'
TEST_OUTPUT_HTML = os.path.dirname(os.path.abspath(__file__)) + '/../../tests/testOutput.html'
FONT_SIZE_STR = 'font-size'
FONT_FAMILY_STR = 'font-family'

# read the pdf
output_string = StringIO()
with open(TEST_PDF, 'rb') as fin:
    extract_text_to_fp(fin, output_string, laparams=LAParams(),output_type='html', codec=None)

# parse the html file
parsedHtml = BeautifulSoup(output_string.getvalue(), 'html.parser')

# format the parsed html file
formattedOutput = parsedHtml.prettify()

def getAttributes(attributeStr: str) -> 'dict[str, str]':
    '''Returns a name to value mapping of html attributes given an unparsed attribute str.

    Args:
        attributeStr (str): The string representing the unparsed attributes of the html.
    '''
    attributeDict = {}
    # the attributes will be formatted like 'font-family: TimesNewRoman; font-size:10px'
    # split up the attributes into each name:value pair
    for attribute in attributeStr.split(';'):
        # split the attribute into the name and value
        (name, value) = attribute.split(':')
        # remove the leading and trailing whitespace
        name = name.strip()
        value = value.strip()
        # add the attribute to the dictionary
        attributeDict[name] = value
    return attributeDict

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
        spanText = span.get_text().replace('\n', '').replace(
            '\t', '').replace('  ', ' ').strip()

        # skip over empty spans
        if spanText == '':
            continue

        # store the text and font style from the span
        spanAttributes = getAttributes(span.attrs['style'])
        spanTextSectionsAndFont.append((spanText, spanAttributes[FONT_FAMILY_STR]))
    
        # update the font size
        fontSize = spanAttributes[FONT_SIZE_STR]
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

# write to an html file
# (this will not be in the final product, but is 
# helpful to look around in to see what is going on)
with open(TEST_OUTPUT_HTML, 'w', encoding='utf-8') as output_file:
    output_file.write(formattedOutput)