#Sprint 3 Report (11/10/2022 - 12/9/2022)

## What's New (User Facing)
 * Document Tagger
 * Document Exporter
 * Document Harvester
 * Project Report Draft
 * Project Report
 * Document Tagger Testing
 * Document Harvester Testing
 * README
 * Sprint Report #3

## Work Summary (Developer Facing)
During this sprint, our team continued work on the document exporter, document harvester and document tagger. Trent continued his work on the document harvester and has been trying to get the image extraction working. As of right now, he is using a built in python function to extract images but it’s not working quite right so he is going to start researching alternatives we could use. Trent also created test cases for the document harvester. Reagan has continued working on the document tagger and has completed a non-automated tag tree structure. Trent and Reagan worked together to restructure our project. Together they organized files into folders and got rid of unnecessary files. Marisa continued to work on the document exporter. This included researching alternatives to writing the code to create a pdf from a html. She originally attempted to use java and built in jvm (java virtual machine) functions to create the exporter but was unable to properly set up the jvm so she looked into a method Trent suggested that uses node js. Using this method, she was able to create a working document exporter. Trent and Reagan are unable to use it, so we are looking into getting the document exporter working for all of us. Along with coding the three previously mentioned features, our team created our Project Report draft during this time. To do this, we used a google document and exported a pdf that we then pushed to the repo with our individual changes. To create this documentation, our team has been creating branches on Github for each issue/feature and working on our individual features weekly.

## Unfinished Work
Document Harvester
Document Tagger
Document Exporter
Color Contrast Adder
Metadata Adder

## Completed Issues/User Stories
Here are links to the issues that we completed in this sprint:

* https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/44
* https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/39
* https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/40
*
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/43
*
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/48
* https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/49
* https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/50

## Incomplete Issues/User Stories
 Here are links to issues we worked on but did not complete in this sprint:
*
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/45
*
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/21
*
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/18
* https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/issues/16


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
* [accessible_document.py] 
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/main/accessibility_apps/utils/accessible_document.py
* [document.py] 
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/main/accessibility_apps/utils/document.py
* [document_harvester.py] 
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/main/accessibility_apps/utils/harvest/document_harvester.py
* [image_extractor.py] 
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/main/accessibility_apps/utils/harvest/image_extractor.py
* [pdf_extractor.py] 
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/main/accessibility_apps/utils/harvest/pdf_extractor.py
* [paragraph.py]
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/main/accessibility_apps/utils/harvest/paragraph.py
* [test_pdf_extractory.py]
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/main/accessibility_apps/tests/test_pdf_extractor.py
* [test_tag_tree.py]
https://github.com/WSUCptSCapstone-Fall2022Spring2023/wsulibraries-accessibilityapps/blob/main/accessibility_apps/tests/test_tag_tree.py
 
## Retrospective Summary
Here's what went well:
  * We were better about getting assignments done earlier instead of starting them last minute
  * We continued having our weekly meetings to discuss progress and hash out details of the project and what we want to complete for the week
  * Our client meetings have been consistent and have provided helpful feedback
 
Here's what we'd like to improve:
   * Combine our work together better and more frequently
   * Reviewing and approving pull requests as they’re made
 
Here are changes we plan to implement in the next sprint:
   * Spending more time on the project during the week
   * Using code created by other group members instead of just using what we have created
   * Start coding the accessibility features
