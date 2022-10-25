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
pdf_content = StringIO()
with open(TEST_PDF, 'rb') as fin:
    extract_text_to_fp(fin, pdf_content, laparams=LAParams(),output_type='html', codec=None)

# parse the html file
parsed_html = BeautifulSoup(pdf_content.getvalue(), 'html.parser')

def get_attributes(attribute_str: str) -> 'dict[str, str]':
    '''Returns a name to value mapping of html attributes given an unparsed attribute str.

    Args:
        attribute_str (str): The string representing the unparsed attributes of the html.
    '''
    attribute_dict = {}
    # the attributes will be formatted like 'font-family: TimesNewRoman; font-size:10px'
    # split up the attributes into each name:value pair
    for attribute in attribute_str.split(';'):
        # split the attribute into the name and value
        (name, value) = attribute.split(':')
        # remove the leading and trailing whitespace
        name = name.strip()
        value = value.strip()
        # add the attribute to the dictionary
        attribute_dict[name] = value
    return attribute_dict

# will be formatted as a list[tuple(span info, text size)]
div_text_info = []
for div in parsed_html.findAll('div'):
    # keep track of the font sizes in the div, a list of tuples of (font size, text length using that size)
    # used to get a normalized font size for the div, which usually just ends up being the font
    # size for all the spans, but sometimes there are little variations and in that case, the most
    # commonly appearing font size is used for a unified div. TODO may want to investigate this approach later
    font_size_distribution = []

    # to store a list of tuples of (text, font-style)
    span_text_sections_and_font = []
    for span in div.findAll('span'):
        # get the text from the span without indentation or line 
        # breaks or double spaces or trailing/leading whitespace
        span_text = span.get_text().replace('\n', '').replace(
            '\t', '').replace('  ', ' ').strip()

        # skip over empty spans
        if span_text == '':
            continue

        # store the text and font style from the span
        span_attributes = get_attributes(span.attrs['style'])
        span_text_sections_and_font.append((span_text, span_attributes[FONT_FAMILY_STR]))
    
        # update the font size
        font_size = span_attributes[FONT_SIZE_STR]
        font_size_distribution.append((font_size, len(span_text)))
    
    # skip empty spans
    if len(span_text_sections_and_font) == 0:
        continue

    # calculate the most commonly appearing font size in the div
    font_size_distribution_dict = {}
    for font_size, text_len in font_size_distribution:
        if font_size not in font_size_distribution_dict.keys():
            font_size_distribution_dict[font_size] = 0
        font_size_distribution_dict[font_size] += text_len
    div_font_size = sorted(font_size_distribution_dict.items(), key=lambda sizeLenTup : sizeLenTup[1], reverse=True)[0][0]

    # add the span data to the div info
    div_text_info.append((span_text_sections_and_font, div_font_size))

# start the output html lines
output_html_lines = [
    '<html>',
    '<head>',
    '<meta content="text/html" http-equiv="Content-Type"/>',
    '</head>',
    '<body>'
]

# add information to the html from the processed data
for (span_info, text_size) in div_text_info:
    output_html_lines.append('<div style="' + FONT_SIZE_STR + ':' + text_size + '">')
    for text, font in span_info:
        output_html_lines.append('<p style="' + FONT_FAMILY_STR + ':' + font + '">')
        output_html_lines.append(text)
        output_html_lines.append('</p>')
    output_html_lines.append('</div>')

# finish the output html lines
output_html_lines.append('</body>')
output_html_lines.append('</html>')

# generate a formatted html from the lines
formatted_output = BeautifulSoup('\n'.join(output_html_lines), 'html.parser').prettify()

# write to an html file
# (this will not be in the final product, but is 
# helpful to look around in to see what is going on)
with open(TEST_OUTPUT_HTML, 'w', encoding='utf-8') as output_file:
    output_file.write(formatted_output)