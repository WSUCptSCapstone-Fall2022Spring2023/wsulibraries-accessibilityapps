# needs manual verification

#! Run this test from the parent directory or module (accessibility_apps) to avoid relative import errors.
# python -m tests.test_export

import os
from pathlib import Path
from utils.export.document_exporter import export_document_to_pdf, export_to_html
from utils.accessible_document import AccessibleDocument

output_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+ "/data/output"
input_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+ "/data/input"

example_pdf = input_folder+"/example.pdf"
doc1 = AccessibleDocument(str(example_pdf)) # retrieved from .../data/input/example.pdf
export_to_html(doc1, output_folder+"/example.html")

export_document_to_pdf(output_folder + "/example.html", output_folder + "/example.pdf")