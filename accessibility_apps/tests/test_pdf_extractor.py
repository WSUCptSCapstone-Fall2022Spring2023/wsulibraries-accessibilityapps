# ===================================================
# File: test_pdf_extractor.py
# Author: Trent Bultsma
# Date: 11/29/2022
# Description: Tests the pdf extractor.
# ==================================================

#! Run This test from the parent directory or module (accessibility_apps) to avoid relative import errors.
# python -m unittest -v tests.test_pdf_extractor

import unittest
from utils.harvest.paragraph import *
from utils.harvest.pdf_extractor import _get_font_style_delimeter, _get_font_style, _get_attributes, extract_paragraphs_and_fonts_and_sizes, _get_exported_html_value

class PdfExtractionTests(unittest.TestCase):
    '''Tests pdf extraction functions.'''

    def setUp(self):
        '''Sets up data for the test cases.'''
        self.test_paragraphs = [
            Paragraph([('This is a PDF', FontStyle.STANDARD)], '27px', 'Helvetica'),
            Paragraph([('This is information.', FontStyle.STANDARD)], '12px', 'Helvetica'),
            Paragraph([('Information continued.', FontStyle.STANDARD)], '12px', 'Helvetica'),
            Paragraph([('This is the end of the pdf.', FontStyle.STANDARD)], '12px', 'Helvetica')
        ]
        self.test_html_value = [
            '<html>',
                '<head>',
                    '<meta content="text/html" http-equiv="Content-Type"/>',
                '</head>',
                '<body>',
                    '<div style="font-size:27px">',
                        '<p style="font-family:Helvetica">',
                            'This is a PDF',
                        '</p>',
                    '</div>',
                    '<div style="font-size:12px">',
                        '<p style="font-family:Helvetica">',
                            'This is information.',
                        '</p>',
                    '</div>',
                    '<div style="font-size:12px">',
                        '<p style="font-family:Helvetica">',
                            'Information continued.',
                        '</p>',
                    '</div>',
                    '<div style="font-size:12px">',
                        '<p style="font-family:Helvetica">',
                            'This is the end of the pdf.',
                        '</p>',
                    '</div>',
                '</body>',
            '</html>'
        ]

    def test_get_font_style_delimeter(self):
        '''Tests getting the delimeter for the font style.'''
        self.assertEqual(_get_font_style_delimeter(FontStyle.BOLD, True), '<strong>')
        self.assertEqual(_get_font_style_delimeter(FontStyle.ITALIC, False), '</em>')
        self.assertEqual(_get_font_style_delimeter(FontStyle.STANDARD, False), '')
        self.assertEqual(_get_font_style_delimeter(FontStyle.BOLD_ITALIC, True), '<strong><em>')

    def test_get_font_style(self):
        '''Tests getting the style of a font.'''
        self.assertEqual(_get_font_style('Arial-BoldMT'), FontStyle.BOLD)
        self.assertEqual(_get_font_style('Georgia'), FontStyle.STANDARD)
        self.assertEqual(_get_font_style('TimesNewRomanPS-ItalicMT'), FontStyle.ITALIC)

    def test_get_attributes(self):
        '''Tests getting the html attributes from an attribute string.'''
        self.assertEqual(_get_attributes('position:absolute; border: textbox 1px solid; writing-mode:lr-tb; left:185px; top:100px; width:351px; height:36px;'), 
        {
            'position' : 'absolute',
            'border' : 'textbox 1px solid',
            'writing-mode' : 'lr-tb',
            'left' : '185px',
            'top' : '100px',
            'width' : '351px',
            'height' : '36px'
        })
        self.assertEqual(_get_attributes('font-family: Georgia; font-size:36px'),
        {
            'font-family' : 'Georgia',
            'font-size' : '36px'
        })

    def test_paragraph_comparison(self):
        '''Tests checking equality between Paragraph objects.'''
        p_1 = Paragraph([('This is information.', FontStyle.STANDARD)], '12px', 'Helvetica')
        p_2 = Paragraph([('Information continued.', FontStyle.STANDARD)], '15px', 'Georgia')
        p_3 = Paragraph([('This is information.', FontStyle.STANDARD)], '12px', 'Helvetica')
        p_4 = Paragraph([('This is information.', FontStyle.STANDARD)], '13px', 'Helvetica')

        self.assertEqual(p_1, p_3)
        self.assertNotEqual(p_1, p_2)
        self.assertNotEqual(p_3, p_4)
    
    def test_extract_paragraphs_and_fonts_and_sizes(self):
        '''Tests extracting paragraphs from the html.'''
        for paragraph_1, paragraph_2 in zip(extract_paragraphs_and_fonts_and_sizes('../data/input/pdf_extractor_test.pdf'), self.test_paragraphs):
            self.assertEqual(paragraph_1, paragraph_2)

    def test_export_html(self):
        '''Tests the data of exporting an html.'''
        html_result_value = _get_exported_html_value(self.test_paragraphs)
        # get rid of all the extra whitespace and new line characters for equality checking
        html_lines = [line.strip() for line in html_result_value.splitlines()]
        self.assertEqual(html_lines, self.test_html_value)

if __name__ == '__main__':
    unittest.main()