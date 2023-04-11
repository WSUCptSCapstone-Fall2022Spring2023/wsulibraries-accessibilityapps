#Semester 2 Sprint 3 Report (3/03/2023 - 4/02/2023)

## What's New (User Facing)
 * Document Exporter
 * Metadata Adder
 * MVP Project Report (Draft)
 * User Interface
 * Setup Script
 * CSV Files for input & output
 * README
 * Semester 2 Sprint Report #3

## Work Summary (Developer Facing)
During this sprint, our team continued to work on the document exporter, document harvester and metadata adder and the user interface. Throughout the sprint, Trent has worked on the graphical user interface and has also been working with Talea to create CSV files that will be useful for Talea and the WSU Libraries crew when uploading the accessible PDFs to the Research Exchange website. Reagan continued working on the a document layout parser. In this sprint, Reagan was trying to find machine learning tools to help identify columns in a document. Marisa created a branch for the formatting of the exported document which will include text size along with some additional formatting. To create this documentation, our team has been creating branches on Github for each issue/feature and working on our individual features weekly.

## Unfinished Work
Document Harvester
Document Tagger
Document Exporter
Color Contrast Adder
Metadata Adder
Setup Script

## Completed Issues/User Stories
Here are links to the issues that we completed in this sprint:

* https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/81
* https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/82
* https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/83
* https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/79

## Incomplete Issues/User Stories
 Here are links to issues we worked on but did not complete in this sprint:
*
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/66
*
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/67
*
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/69

## Code Files for Review
Please review the following code files, which were actively developed during this sprint, for quality:
 * [main.py] 
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/main/accessibility_apps/main.py
* [pdf_exporter.js] 
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/document-exporter/accessibility_apps/utils/export/pdf_exporter.js
* [document_exporter.py]
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/main/accessibility_apps/utils/export/document_exporter.py
* [color_contrast_adder.py]
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/document-harvester/accessibility_apps/utils/transform/color_contrast_adder.py
* [document_harvester.py] 
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/main/accessibility_apps/utils/harvest/document_harvester.py
* [alt_text_adder.py]
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/add-keywords-metadata/accessibility_apps/utils/transform/alt_text_adder.py
* [document_tagger.py]
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/add-keywords-metadata/accessibility_apps/utils/transform/document_tagger.py
* [app.py]
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/user-interface/accessibility_apps/utils/user_interface/app.py
* [document_layout.py]
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/document-harvester/accessibility_apps/utils/harvest/document_layout.py
* [bulk_word_harvester]
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/document-harvester/accessibility_apps/utils/harvest/bulk_word_harvester.py
 
## Retrospective Summary
Here's what went well:
  * We were better about getting assignments done earlier instead of starting them last minute
 
Here's what we'd like to improve:
   * Making contributions by group members more even in the project
   * Adding test cases immediately after a feature is finished
   * Update MVP Project Report draft more frequently
 
Here are changes we plan to implement in the next sprint:
   * Spending more time on the project during the week
   * Make test cases earlier and add them to the MVP Project Report draft
