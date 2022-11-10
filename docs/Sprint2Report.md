#Sprint 2 Report (10/10/2022 - 11/9/2022)

## What's New (User Facing)
 * Document Tagger
 * Document Exporter
 * Document Harvester
 * Testing And Acceptance
 * Terminal Application
 * README
 * Sprint Report #2

## Work Summary (Developer Facing)
During this sprint our team began creating the code for our project. We started developing three of the main features of our project. The features we started developing are the document harvester, the document exporter and the document tagger. Trent has been working to get text and images extracted from pdf files into html documents and Marisa has been using the html document created to begin creating the document exporter. Trent has been having issues getting all the images from the original pdf to export correctly. Marisa has struggled with having a variable font size throughout the document since the function in python that sets the font size does not accept variable input. Reagan has been working on the document tagger and has created a tag tree structure. In doing so, he has realized that creating a tag tree structure of our own means that text to speech software might not recognize the tag tree and, as a result, won’t work properly. To create this documentation, our team has been creating branches on Github for each issue/feature and working on our individual features weekly.

## Unfinished Work
For this sprint, we did not finish the document exporter, the document harvester or the tag tree features. The document harvester still needs to be able to harvest images, the tag tree still needs to be implemented further and the document exporter needs to be able to register text style changes. These issues will be added to sprint 3 for completion.

## Completed Issues/User Stories
Here are links to the issues that we completed in this sprint:

* https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/30
* https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/31
* https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/35
*
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/22
*
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/27
*
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/26
*
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/25

## Incomplete Issues/User Stories
 Here are links to issues we worked on but did not complete in this sprint:

*
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/21
*
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/16
*
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/18


## Code Files for Review
Please review the following code files, which were actively developed during this sprint, for quality:
 * [main.py] https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/main/sample/main.py
* [pdf_exporter.py] https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/main/sample/pdf_exporter.py
* [terminal_application.py] https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/main/sample/terminal_application.py
* [TagTree.py] https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/main/sample/src/TagTree.py
* [accessible_document.py] https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/main/sample/src/accessible_document.py
* [document.py] https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/main/sample/src/document.py
* [document_harvester.py] https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/main/sample/src/document_harvester.py
* [image_extractor.py] https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/main/sample/src/image_extractor.py
* [pdf_extractor.py] https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/main/sample/src/pdf_extractor.py
 
## Retrospective Summary
Here's what went well:
  * We were better about getting assignments done earlier instead of starting them last minute
  * We started having weekly group meetings to discuss the project and our progress
  * Our client meetings have been consistent and have provided helpful feedback
 
Here's what we'd like to improve:
   * Combine our work together better and more frequently
   * Reviewing and approving pull requests as they’re made
 
Here are changes we plan to implement in the next sprint:
   * Spending more time on the project during the week
   * Using code created by other group members instead of just using what we have created