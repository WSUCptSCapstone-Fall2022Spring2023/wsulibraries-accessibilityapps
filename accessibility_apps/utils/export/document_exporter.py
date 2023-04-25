#!/usr/bin/env python

""" Creates a pdf from a html link
"""

import os
import subprocess
from bs4 import BeautifulSoup
from utils.transform.TagTree import Tag
from utils.harvest.pdf_extractor import _get_font_style_delimeter


# Last Edit By: Marisa Loyd
# * Edit Details: Current code is from Marisa
def export_document_to_pdf(input_file_path, output_file_path):
    """ Transforms the metadata from codable data structures back into a usable and readable
        format: PDF

    Args:
        filename (string): File address location where the PDF will be sent.
    """     
    
    p = subprocess.Popen(['node', os.path.dirname(os.path.abspath(__file__)) + '/pdf_exporter.js', input_file_path, output_file_path], stdout=subprocess.PIPE)
    p.wait()
    return

def export_to_html(doc, output_html_path: str):
        '''Exports the pdf data from the TagTree into an html file in the location `output_html_path`.

        Args:
            doc : The accessible document object.
            output_html_path (str): The file location to output the html file.
        '''
 
        formatted_output = _get_exported_html_value(doc)

    # write to an html file
        with open(output_html_path, 'w', encoding='utf-8') as output_file:
            output_file.write(formatted_output)

def _get_exported_html_value (doc) -> str: #(tree: list[TagTree]) -> str:
    '''Returns the contents of the html exported from the provided TagTree.

    Args:
        doc : The accessible document.
    '''
    FONT_SIZE_STR = 'font-size'
    FONT_FAMILY_STR = 'font-family'
    # start the output html lines
    output_html_lines = [
        '<html>',
        '<head>',
        '<meta content="text/html" http-equiv="Content-Type"/>',
        '</head>',
        '<body>'
    ]

    # add information to the html from the processed data
    for Tag.get_data in doc.tree.traverse_tree():
        #determine font size based on tag type
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
        for text, font_style in Tag:
            text = Tag.get_data()
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
