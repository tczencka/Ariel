# Compiler to turn all scripts into a list of lists

import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal
from pdfminer.converter import HTMLConverter,TextConverter,XMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

def parsedocument(path):
    # convert all horizontal text into a lines list (one entry per line)
    # document is a file stream
    lines = []
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    fp = open(path, 'rb')
    for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
            layout = device.get_result()
            for element in layout:
                if isinstance(element, LTTextBoxHorizontal):
                    lines.extend(element.get_text().splitlines())
    return lines

def pathfinder(titles_list):
    paths = []
    screenplays = []
    for show in titles_list:
    	# Will need to adjust the following line to match your system path.
        path = str('/Users/tylerzencka/metis_work/Ariel/BETA/' + str(show))  
        paths.append(path)
    for path in paths:
        screenplays.append(parsedocument(path))
    return screenplays
