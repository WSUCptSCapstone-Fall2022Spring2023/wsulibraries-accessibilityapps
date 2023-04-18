#!/usr/bin/env python

""" Creates a pdf from a html link
"""

import os
import sys
import subprocess

from bs4 import BeautifulSoup

from accessibility_apps.utils.harvest.pdf_extractor import _get_font_style_delimeter

path = os.path.abspath('../')
if path not in sys.path:
    sys.path.append(path)

    from utils.transform.TagTree import TagTree
    from utils.accessible_document import *
    from utils.document import Document

FONT_SIZE_STR = 'font-size'
FONT_FAMILY_STR = 'font-family'

# Last Edit By: Marisa Loyd
# * Edit Details: Current code is from Marisa
def export_document_to_pdf(input_file_path, output_file_path):
    """ Transforms the metadata from codable data structures back into a usable and readable
        format: PDF

    Args:
        filename (string): File address location where the PDF will be sent.
    """

    #name = filename.split('.')
    #pdfName = name[0]+'_pdf'

    # tag tree -> html
    # font & size correct
    #images ?
    # each section of tag tree have set font size
        #paragraph = 12 pt
        #h1 = 32 pt
        #h2 = 24 pt
        #h3 = 19 pt
        #h4 = 16 pt
        #h5 = 14 pt
        #h6 = 13 pt
        #script to set up python, node js, all other exceptions, maybe combine the two current ones
        
    
    p = subprocess.Popen(['node', os.path.dirname(os.path.abspath(__file__)) + '/pdf_exporter.js', input_file_path, output_file_path], stdout=subprocess.PIPE)
    p.wait()
    print("export_document() -> pass.")
    return

def export_to_html(doc : AccessibleDocument, output_html_path: str):
    '''Exports the pdf data from the `paragraphs` list into an html file in the location `output_html_path`.

    Args:
        paragraphs (list[Paragraph]): The data representing an extracted pdf file.
        output_html_path (str): The file location to output the html file.
    '''
    #generate_tags(doc)
    formatted_output = _get_exported_html_value(doc.tree)

    # write to an html file
    with open(output_html_path, 'w', encoding='utf-8') as output_file:
        output_file.write(formatted_output)

def _get_exported_html_value (doc : AccessibleDocument) -> str: #(tree: list[TagTree]) -> str:
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
#paragraph = 12 pt
        #h1 = 32 pt
        #h2 = 24 pt
        #h3 = 19 pt
        #h4 = 16 pt
        #h5 = 14 pt
        #h6 = 13 pt
    # add information to the html from the processed data
    for Tag in doc.tree:
        #text = Tag.get_data()
        if(doc.tree.getTag()=='<H1>'):
            font_size = '32px'
            font_family = 'TimesNewRoman'
            font_style = 'BOLD'
        elif(doc.tree.get_tag() == '<H2>'):
            font_size = '24px'
            font_family = 'TimesNewRoman'
            font_style = 'BOLD'
        elif(doc.tree.get_tag() == '<H3>'):
            font_size = '19px'
            font_family = 'TimesNewRoman'
            font_style = 'BOLD'
        elif(doc.tree.get_tag() == '<H4>'):
            font_size = '16px'
            font_family = 'TimesNewRoman'
            font_style = 'BOLD'
        elif(doc.tree.get_tag() == '<H5>'):
            font_size = '14px'
            font_family = 'TimesNewRoman'
            font_style = 'BOLD'
        elif(doc.tree.get_tag() == '<H6>'):
            font_size = '13px'
            font_family = 'TimesNewRoman'
            font_style = 'BOLD'
        else:
            font_size = '12px'
            font_family = 'TimesNewRoman'
            font_style = 'STANDARD'

        output_html_lines.append('<div style="' + FONT_SIZE_STR + ':' + font_size + '">')
        output_html_lines.append('<p style="' + FONT_FAMILY_STR + ':' + font_family + '">')
        for text, font_style in Tag.get_data():
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
    # TODO: Implement solution with Document class attributes.
