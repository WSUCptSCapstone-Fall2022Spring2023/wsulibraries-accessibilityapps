#Semester 2 Sprint 2 Report (2/03/2023 - 3/02/2023)

## What's New (User Facing)
 * Document Exporter
 * Document Harvester
 * Metadata Adder
 * MVP Project Report (Draft)
 * User Interface
 * README
 * Semester 2 Sprint Report #2

## Work Summary (Developer Facing)
During this sprint, our team continued to work on the document exporter, document harvester and metadata adder. We also began working on the graphical user interface for our project. At the beginning of the sprint, Trent continued his work on the metadata adder and, after discussion between our team members, he decided to start working on the user interface. Reagan worked on creating a document layout parser to identify pieces of a document. Marisa finished the document exporter, which now works on a windows computer, although there is a weird pop-up that Trent gets when he runs the program. She tried a few fixes but was unable to find a solution at the present moment. Marisa also created the test cases for the document exporter. Along with coding the previously mentioned features, our team added test cases to our Minimum Viable Product (MVP) Project Report draft during this time. This added information tells the reader what aspect is being tested and how, the expected result, the observed result, whether the test case passed or not, and the requirements of the test case. To do this, we used a Google document and exported a pdf that we then pushed to the repo with our individual changes. To create this documentation, our team has been creating branches on Github for each issue/feature and working on our individual features weekly.

## Unfinished Work
Document Harvester
Document Tagger
Document Exporter
Color Contrast Adder
Metadata Adder

## Completed Issues/User Stories
Here are links to the issues that we completed in this sprint:

* https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/71
* https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/21
* https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/72
* https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/73

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
  * Our weekly meetings with each other have been going smoothly
  * We have been combining work together more frequently
 
Here's what we'd like to improve:
   * Reviewing and approving pull requests as they’re made
   * Adding test cases immediately after a feature is finished
 
Here are changes we plan to implement in the next sprint:
   * Spending more time on the project during the week
   * Make test cases earlier and add them to the MVP Project Report draft
