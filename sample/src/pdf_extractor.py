# ===================================================
# File: pdf_extractor.py
# Author: Trent Bultsma
# Date: 10/12/2022
# Description: Extracts the data from a pdf as html.
# ==================================================

# imports
import os
from enum import Enum
from io import StringIO
from bs4 import BeautifulSoup
from pdfminer.layout import LAParams
from pdfminer.high_level import extract_text_to_fp

# constants
TEST_PDF = os.path.dirname(os.path.abspath(__file__)) + '/../../tests/testInput.pdf'
TEST_OUTPUT_HTML = os.path.dirname(os.path.abspath(__file__)) + '/../../tests/testOutput.html'
FONT_SIZE_STR = 'font-size'
FONT_FAMILY_STR = 'font-family'

class FontStyle(Enum):
    '''Represents the style of text.'''
    STANDARD = 1
    BOLD = 2
    ITALIC = 3
    BOLD_ITALIC = 4
    # TODO maybe add underline or strikethrough here

def get_font_style_delimeter(style: FontStyle, is_start: bool) -> str:
    '''Returns the html delimeter for a font style.
    
    Args:
        style (FontStyle): The style of the font.
        
    Args:
        is_start (bool): Whether the delimeter is for the start of the text or for the end.'''
    
    if style == FontStyle.STANDARD:
        return ""
    elif style == FontStyle.BOLD:
        return "<" + ("" if is_start else "/") + "strong>"
    elif style == FontStyle.ITALIC:
        return "<" + ("" if is_start else "/") + "em>"
    elif style == FontStyle.BOLD_ITALIC:
        return get_font_style_delimeter(FontStyle.BOLD, is_start) + get_font_style_delimeter(FontStyle.ITALIC, is_start)

def get_font_style(font_family_name: str) -> FontStyle:
    '''Returns the font style of a font.

    Args:
        font_family_name (str): The name of the font.'''

    bold = False
    italic = False

    # TODO update detection substrings
    # Detect the font style.
    if 'bold' in font_family_name.lower():
        bold = True
    if 'italic' in font_family_name.lower():
        italic = True

    # Return the font style detected.
    if bold and italic:
        return FontStyle.BOLD_ITALIC
    elif bold:
        return FontStyle.BOLD
    elif italic:
        return FontStyle.ITALIC
    else:
        return FontStyle.STANDARD

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

# will be formatted as a list[tuple(span info, text size, font family)]
div_text_info = []
for div in parsed_html.findAll('div'):
    # keep track of the font sizes in the div, a list of tuples of (font size, text length using that size)
    # used to get a normalized font size for the div, which usually just ends up being the font
    # size for all the spans, but sometimes there are little variations and in that case, the most
    # commonly appearing font size is used for a unified div. TODO may want to investigate this approach later
    font_size_distribution = []
    # also keep track of the font to get the average font
    font_family_distribution = []

    # to store a list of tuples of (text, font style)
    span_text_sections_and_font_style = []
    for span in div.findAll('span'):
        # get the text from the span without indentation or line 
        # breaks or double spaces or trailing/leading whitespace
        span_text = span.get_text().replace('\n', '').replace(
            '\t', '').replace('  ', ' ').strip()

        # skip over empty spans
        if span_text == '':
            continue

        span_attributes = get_attributes(span.attrs['style'])
        
        # update the average font family
        font_family = span_attributes[FONT_FAMILY_STR]
        font_family_distribution.append((font_family, len(span_text)))

        # store the text and font style from the span
        span_text_sections_and_font_style.append((span_text, get_font_style(font_family)))
    
        # update the average font size
        font_size = span_attributes[FONT_SIZE_STR]
        font_size_distribution.append((font_size, len(span_text)))
    
    # skip empty spans
    if len(span_text_sections_and_font_style) == 0:
        continue

    # calculate the most commonly appearing font size in the div
    font_size_distribution_dict = {}
    for font_size, text_len in font_size_distribution:
        if font_size not in font_size_distribution_dict.keys():
            font_size_distribution_dict[font_size] = 0
        font_size_distribution_dict[font_size] += text_len
    div_font_size = sorted(font_size_distribution_dict.items(), key=lambda sizeLenTup : sizeLenTup[1], reverse=True)[0][0]

    # calculate the most commonly appearing font family in the div
    font_family_distribution_dict = {}
    for font_family, text_len in font_family_distribution:
        if font_family not in font_family_distribution_dict.keys():
            font_family_distribution_dict[font_family] = 0
        font_family_distribution_dict[font_family] += text_len
    div_font_family = sorted(font_family_distribution_dict.items(), key=lambda sizeLenTup : sizeLenTup[1], reverse=True)[0][0]

    # add the span data to the div info
    div_text_info.append((span_text_sections_and_font_style, div_font_size, div_font_family))

# start the output html lines
output_html_lines = [
    '<html>',
    '<head>',
    '<meta content="text/html" http-equiv="Content-Type"/>',
    '</head>',
    '<body>'
]

# add information to the html from the processed data
for (span_info, text_size, font_family) in div_text_info:
    output_html_lines.append('<div style="' + FONT_SIZE_STR + ':' + text_size + '">')
    output_html_lines.append('<p style="' + FONT_FAMILY_STR + ':' + font_family + '">')
    for text, font_style in span_info:
        output_html_lines.append(get_font_style_delimeter(font_style, True))
        output_html_lines.append(text)
        output_html_lines.append(get_font_style_delimeter(font_style, False))
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