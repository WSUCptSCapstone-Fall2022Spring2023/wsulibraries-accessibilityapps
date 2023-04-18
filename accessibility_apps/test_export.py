# needs manual verification

#! Run this test from the parent directory or module (accessibility_apps) to avoid relative import errors.
# python -m tests.test_export

import os
from utils.export.document_exporter import export_document_to_pdf

output_folder = os.path.abspath(__file__) + "/../../data/output"

export_document_to_pdf(output_folder + "/example.html", output_folder + "/example.pdf")