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

    def __eq__(self, other: object) -> bool:
        '''Returns whether the other object is equivalent to this Paragraph object.'''
        
        # make sure the other object is a Paragraph
        if type(other) is not Paragraph:
            return False

        # make sure the text info, font size, and font family match for both objects
        if self.font_size != other.font_size:
            return False
        if self.font_family != other.font_family:
            return False
        for ((thisText, thisStyle), (otherText, otherStyle)) in zip(self.text_info, other.text_info):
            if thisText != otherText:
                return False
            if thisStyle != otherStyle:
                return False
        
        # if we got to here, they must have the same value for everything
        return True

    def __repr__(self) -> str:
        '''Returns the string representation of the this Paragraph object.'''
        return "Paragraph({}, {}, {})".format(self.text_info, self.font_size, self.font_family)

    def get_raw_text(self):
        '''Returns the text of the paragraph without any style formatting.'''
        text_list = []
        for text, font_style in self.text_info:
            text_list.append(text)
        return " ".join(text_list)