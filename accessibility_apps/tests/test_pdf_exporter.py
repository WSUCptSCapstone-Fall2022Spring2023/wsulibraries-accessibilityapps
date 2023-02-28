# ===================================================
# File: test_pdf_exporter.py
# Author: Marisa Loyd
# Date: 2/28/2023
# Description: Tests the pdf exporter.
# ==================================================

import unittest
import os
from utils.export.document_exporter import export_document

class PdfExporterTests(unittest.TestCase):
    '''Tests pdf export function.'''
    
    def test_export(self):
       '''Tests the exporting of a html to pdf''' 
       try:
            export_document('example.html')
            self.assertTrue(True)
       except:
           self.assertTrue(False)
        
if __name__ == '__main__':
        unittest.main()