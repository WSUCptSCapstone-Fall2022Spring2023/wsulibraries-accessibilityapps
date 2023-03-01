#Semester 2 Sprint 1 Report (1/09/2023 - 2/02/2023)

## What's New (User Facing)
 * Document Tagger
 * Document Exporter
 * Document Harvester
 * Metadata Adder
 * MVP Project Report (Draft)
 * README
 * Semester 2 Sprint Report #1

## Work Summary (Developer Facing)
During this sprint, our team continued to work on the document exporter, document harvester and document tagger. We also began working on the metadata adder. At the beginning of the sprint, Trent continued his work on the document harvester and, after discussion between our team members, he decided to start working on the metadata adder. Reagan worked on the tag tree until he was unable to continue without the attributes from a downloaded document. After Trent began working on the metadata adder, Reagan took over the document harvester and is currently working on finding a way to classify the pieces of a document such as the headers and paragraphs. This will allow us to add the pieces to the tag tree later on. Marisa has been working on making the document exporter work on a windows computer since she has a linux system. She has been doing research to solve the issues presented while on a windows system and was able to implement a working solution. She also began working on finding a way to use the exporter in python since it was implemented in node js and not python. Along with coding the previously mentioned features, our team created our Minimum Viable Product (MVP) Project Report draft during this time. To do this, we used a google document and exported a pdf that we then pushed to the repo with our individual changes. To create this documentation, our team has been creating branches on Github for each issue/feature and working on our individual features weekly.

## Unfinished Work
Document Harvester
Document Tagger
Document Exporter
Color Contrast Adder
Metadata Adder

## Completed Issues/User Stories
Here are links to the issues that we completed in this sprint:

* https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/57
* https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/61
* https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/62

## Incomplete Issues/User Stories
 Here are links to issues we worked on but did not complete in this sprint:
*
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/21
*
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/18
*
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/16
*
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/60
*
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/58


## Code Files for Review
Please review the following code files, which were actively developed during this sprint, for quality:
 * [main.py] 
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/main/accessibility_apps/main.py
* [pdf_exporter.js] 
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/document-exporter/accessibility_apps/utils/export/pdf_exporter.js
* [terminal_application.py] 
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/main/accessibility_apps/terminal_application.py
* [TagTree.py] 
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/main/accessibility_apps/utils/transform/TagTree.py
* [document_harvester.py] 
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/main/accessibility_apps/utils/harvest/document_harvester.py
* [downloader.py]
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/document-downloader/accessibility_apps/utils/database_communication/downloader.py
* [alt_text_adder.py]
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/add-keywords-metadata/accessibility_apps/utils/transform/alt_text_adder.py
* [document_tagger.py]
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/add-keywords-metadata/accessibility_apps/utils/transform/document_tagger.py

 
## Retrospective Summary
Here's what went well:
  * We were better about getting assignments done earlier instead of starting them last minute
  * We easily picked up our weekly meetings as soon as the semester started
  * Our weekly client meetings have resumed with no conflicts
 
Here's what we'd like to improve:
   * Combine our work together better and more frequently
   * Reviewing and approving pull requests as they’re made
 
Here are changes we plan to implement in the next sprint:
   * Spending more time on the project during the week
   * Using code created by other group members instead of just using what we have created
   * Start coding the accessibility features
