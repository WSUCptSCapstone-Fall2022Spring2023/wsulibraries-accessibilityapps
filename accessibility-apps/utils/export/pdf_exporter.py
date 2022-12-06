#!/usr/bin/env python

""" Creates a pdf from a text file
"""

import linecache
from fpdf import FPDF
 
pdf = FPDF()
 
pdf.add_page()
textName = input("Enter the name of the text file you want to convert to a pdf : ")
#textName = 'htmlTest.txt'
baseName = textName.split('.')
dotPdf = ".pdf"
pdfName = baseName[0] + dotPdf
# heading font size = 27
#pdf.set_font("Arial", size = 27)

#get heading of pdf 
#line = linecache.getline(textName,1)

#iterative variable for lines 2 -> end of pdf
n = 1
fontSize1 = 17
#create pdf cell aligned in center
#pdf.cell(200, 10, txt = line, ln = 1, align = 'C')
with open(textName) as f:
    for line in f:
        #n = n+1
        #body font size = 12
        line = linecache.getline(textName,n)
        if(len(line.split('='))>=2) and (line.split('=')[0] == "  <div style"):
            fSize = line.split("=")
            szSent = fSize[0]
        else:
            szSent = line
        if(szSent == "  <div style"):
            #print("Hi\n")
            splLine = line.split(":") #split line by :
            fs = splLine[1].split("px") #split line by px to get font size
            fSize = fs[0] #the font size
            n = n+1 #move to next line
            line = linecache.getline(textName,n) #read next line
            f = line.split("\"") #split line by "
            fStyle = f[1].split(":") #split line by :
            f = fStyle[1] #font style
        #next line 
            n = n+1 #go to next line
        #fontSty = fontSpl[1]
            if len(f.split("-"))>=2: #font has a specific style (bold or italic)
                fontSpl = f.split("-") #split font by - to see if it's bold or italicized
                fontSty = fontSpl[1] #either BoldMT or Italic
                if(fontSty == "BoldMT"):
                    pdf.set_font("Arial", 'B', size = 12) #set to bold size 12 Arial
                    line = linecache.getline(textName,n) #read line
                    pdf.cell(200, 10, txt = line, ln = 1, align = 'L') #put line in pdf w/correct font style
                    n = n+1
            else:
                pdf.set_font("Arial", size = 12) #set to size 12 Arial
                line = linecache.getline(textName,n) #read line
                pdf.cell(200, 10, txt = line, ln = 1, align = 'L') #put line in pdf w/correct font style
                n = n+1
        else:
                pdf.set_font("Arial", size = 12) #set to size 12 Arial
                line = linecache.getline(textName,n) #read line
                pdf.cell(200, 10, txt = line, ln = 1, align = 'L') #put line in pdf w/correct font style
                n = n+1
pdf.output(pdfName)
 