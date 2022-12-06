# ========================================================
# File: paragraph.py
# Author: Trent Bultsma
# Date: 11/15/2022
# Description: Defines a class to store a paragraph with 
# text, font size, font family, and font style data.
# =======================================================

from enum import Enum

class FontStyle(Enum):
    '''Represents the style of text.'''
    STANDARD = 1
    BOLD = 2
    ITALIC = 3
    BOLD_ITALIC = 4

class Paragraph():
    '''Defines a paragraph with text, font size, font family, and font style data.'''
    
    def __init__(self, text_info: list[tuple[str, FontStyle]], font_size: str, font_family: str):
        '''Initializes the `Paragraph`.'''
        self.font_size = font_size
        self.font_family = font_family
        self.text_info = text_info

    def get_raw_text(self):
        '''Returns the text of the paragraph without any style formatting.'''
        text_list = []
        for text, font_style in self.text_info:
            text_list.append(text)
        return " ".join(text_list)