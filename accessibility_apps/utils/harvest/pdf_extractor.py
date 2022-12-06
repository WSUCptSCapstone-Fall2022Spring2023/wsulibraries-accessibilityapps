# ===================================================
# File: pdf_extractor.py
# Author: Trent Bultsma
# Date: 10/12/2022
# Description: Extracts the data from a pdf as html.
# ==================================================

# imports
from utils.harvest.paragraph import *
import re
from io import StringIO
from bs4 import BeautifulSoup
from pdfminer.layout import LAParams
from pdfminer.high_level import extract_text_to_fp

# constants
FONT_SIZE_STR = 'font-size'
FONT_FAMILY_STR = 'font-family'

def _get_font_style_delimeter(style: FontStyle, is_start: bool) -> str:
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
        return _get_font_style_delimeter(FontStyle.BOLD, is_start) + _get_font_style_delimeter(FontStyle.ITALIC, is_start)

def _get_font_style(font_family_name: str) -> FontStyle:
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

def _get_attributes(attribute_str: str) -> 'dict[str, str]':
    '''Returns a name to value mapping of html attributes given an unparsed attribute str.

    Args:
        attribute_str (str): The string representing the unparsed attributes of the html.
    '''
    attribute_dict = {}
    # the attributes will be formatted like 'font-family: TimesNewRoman; font-size:10px'
    # split up the attributes into each name:value pair
    for attribute in attribute_str.split(';'):
        if attribute != '':
            # split the attribute into the name and value
            (name, value) = attribute.split(':')
            # remove the leading and trailing whitespace
            name = name.strip()
            value = value.strip()
            # add the attribute to the dictionary
            attribute_dict[name] = value
    return attribute_dict

def _get_cid_character(cid: str) -> str:
    '''Returns the character corresponding to the cid value
    
    Args:
        cid (str): The cid value.
    '''

    # cid will be the format (cid:<a number>) and we want to get that number and turn it into a character
    return chr(int(cid[len('(cid:'):-len(')')]))

def _convert_cid_str(text: str) -> str:
    '''Returns a string with all (cid:xxx) parts converted to the unicode character they correspond to.
    
    Args:
        text (str): The text being converted.
    '''

    for cid in set(re.findall(r'\(cid\:\d+\)', text)):
        text = text.replace(cid, _get_cid_character(cid))

    return text

def extract_paragraphs_and_fonts_and_sizes(pdf_file_path: str) -> list[Paragraph]:
    '''Returns a list of `Paragraph` objects extracted from the input pdf.

    Args:
        pdf_file_path (str): The string path of the pdf file to extract data from.
    '''

    # read the pdf
    pdf_content = StringIO()
    with open(pdf_file_path, 'rb') as fin:
        extract_text_to_fp(fin, pdf_content, laparams=LAParams(), output_type='html', codec=None)

    # parse the html file
    parsed_html = BeautifulSoup(pdf_content.getvalue(), 'html.parser')

    paragraphs = []
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
            # get rid of the (cid:xxx) strings in the span text
            span_text = _convert_cid_str(span.get_text())

            # get the text from the span without indentation or line 
            # breaks or double spaces or trailing/leading whitespace
            span_text = span_text.replace('\n', '').replace(
                '\t', '').replace('  ', ' ').strip()

            # skip over empty spans
            if span_text == '':
                continue

            span_attributes = _get_attributes(span.attrs['style'])
            
            # update the average font family
            font_family = span_attributes[FONT_FAMILY_STR]
            font_family_distribution.append((font_family, len(span_text)))

            # store the text and font style from the span
            span_text_sections_and_font_style.append((span_text, _get_font_style(font_family)))
        
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
        paragraphs.append(Paragraph(span_text_sections_and_font_style, div_font_size, div_font_family))
    
    return paragraphs

def export_to_html(paragraphs: list[Paragraph], output_html_path: str):
    '''Exports the pdf data from the `paragraphs` list into an html file in the location `output_html_path`.

    Args:
        paragraphs (list[Paragraph]): The data representing an extracted pdf file.
        output_html_path (str): The file location to output the html file.
    '''

    formatted_output = _get_exported_html_value(paragraphs)

    # write to an html file
    with open(output_html_path, 'w', encoding='utf-8') as output_file:
        output_file.write(formatted_output)

def _get_exported_html_value(paragraphs: list[Paragraph]) -> str:
    '''Returns the contents of the html exported from the provided list of `Paragraph`s.

    Args:
        paragraphs (list[Paragraph]): The data representing an extracted pdf file.
    '''
    # start the output html lines
    output_html_lines = [
        '<html>',
        '<head>',
        '<meta content="text/html" http-equiv="Content-Type"/>',
        '</head>',
        '<body>'
    ]

    # add information to the html from the processed data
    for paragraph in paragraphs:
        output_html_lines.append('<div style="' + FONT_SIZE_STR + ':' + paragraph.font_size + '">')
        output_html_lines.append('<p style="' + FONT_FAMILY_STR + ':' + paragraph.font_family + '">')
        for text, font_style in paragraph.text_info:
            output_html_lines.append(_get_font_style_delimeter(font_style, True))
            output_html_lines.append(text)
            output_html_lines.append(_get_font_style_delimeter(font_style, False))
        output_html_lines.append('</p>')
        output_html_lines.append('</div>')

    # finish the output html lines
    output_html_lines.append('</body>')
    output_html_lines.append('</html>')

    # generate a formatted html from the lines
    formatted_output = BeautifulSoup('\n'.join(output_html_lines), 'html.parser').prettify()

    return formatted_output

# run the code in this file for testing purposes
if __name__ == '__main__':
    import os
    test_pdf = os.path.dirname(os.path.abspath(__file__)) + '/../../tests/testInput.pdf'
    test_output_html = os.path.dirname(os.path.abspath(__file__)) + '/../../tests/testOutput.html'
    div_text_info = extract_paragraphs_and_fonts_and_sizes(test_pdf)
    export_to_html(div_text_info, test_output_html)