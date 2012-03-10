# -*- coding: utf-8 -*-
"""
This is the PARLIS scraper module.

It will retrieve the pages from parlis and store there contents in a .csv-file.
"""
from BeautifulSoup import BeautifulSoup
import csv
import re
import time
import urllib2
import traceback

from proposition import Proposition
from extractors import DataExtractor, DataExtractor1990, DataExtractor2003, \
                       DataExtractor2006


class ParlisScraper(object):
    """
    This class scrapes the files from the webserver.
    The information scraped is saved into a textfile.
    """
    def __init__(self, year, inputFile=None, outputFile=None):
        """
        Constructor.
        The year is used to specify the filenames.
        If it is wished the filenames can be overridden.
        
        @param year: The year what shall be parsed
        @type year: int
        @param inputFile: File from wich the input is read.
        @type inputFile: str
        @param outputFile: File into wich the data is saved.
        @type outputFile: str
        """
        
        #This is the plan B if no filenames are specified.
        if(inputFile is None):
            inputFile = "%s-IDlist.txt" % year
        
        if(outputFile is None):
            outputFile = "%s-antraege.csv" % year
        
        #Configure the class
        self.year = year
        self.outputFile = outputFile
        self.inputFile = inputFile
        self.sleepingTimeInSeconds = 3

    def _getPage(self, link):
        """
        Receives the content of the supplied url.
        
        @param link: URL to the page to retrieve.
        @type link: str
        @return: A BeautifulSoup-instance for the supplied url.
                 None if no page could be retrieved.
        @type: BeautifulSoup
        """
        soup = None
        
        try:
            page = urllib2.urlopen(link)
            soup = BeautifulSoup(page)
        except Exception, err:
            print "Error receiving '%s':\n%s" % (link, err)
        
        return soup
    
    def _getExtractor(self, link):
        if(self._needs1990sWorkaround()):
            return DataExtractor1990(link, self._getPage(link))
        elif(self._needs2003Workaround()):
            return DataExtractor2003(link, self._getPage(link))
        elif(self._needs2006Workaround()):
            return DataExtractor2006(link, self._getPage(link))
        else:
            return DataExtractor(link, self._getPage(link))
    
    def _getPropositionFromExtractor(self, link):
        extractor = self._getExtractor(link)
        
        assert isinstance(extractor, DataExtractor)
        
        try:
            proposition = Proposition(
                                      extractor.getTitle(),
                                      extractor.getDate(),
                                      extractor.getLink(),
                                      extractor.getParty(),
                                      extractor.getPropositionNumber(),
                                      extractor.getOBNumber()
                                      )
            
            proposition.result = extractor.getResult()
            proposition.statement = extractor.getStatement()
            proposition.subject = extractor.getSubject()
            proposition.updateDate = extractor.getUpdateDate()
        except Exception, err:
            print ('Could not extract all the needed data: %s\n'
                   'Extractor used: %s' % (err, extractor))
            traceback.print_exc()
            #Throw this on to the next instance...
            raise
        
        return proposition
    
    def _quoteChange(self, text):
        """
        Removes the quotation mark (") from the text.
        
        @param text: Some text
        @type text: str
        @return: Cleaned version without quotation mark
        @rtype: str
        """
        return re.sub('"', '', text)

    def __writeInformationToFile(self, content):
        """
        Writes information to a file.
        Data will be attended to the file.
        
        @param outputFile: The file to write to.
        @type outputFile: str
        @param content: The data that shall be written to the file-
        @type content: str
        """
        try:
            csvWriter = csv.writer(open(self.outputFile, 'ab'),
                                   delimiter=',', quotechar='"')
            csvWriter.writerow(content)
        except IOError, ioerr:
            #Most obvious error will occur when writing the file...
            print "Error writing file '%s':\n%s" % (self.outputFile, ioerr)
        except Exception, err:
            #General error handling for everything else
            print err
    
    def __loadIndex(self, inputFile):
        """
        Starts processing of the supplied file.
        Reads the content of the files, creates a link from it and then
        starts scraping that page.
        The output is saved to a file.
        
        @param inputFile: input file with information to create the links.
        @type inputFile: str
        """
        collectedPropositions = []
        
        try:
            inputFileHandle = open(inputFile, 'r')
            
            for line in inputFileHandle:
                #Create url
                link = ("http://stvv.frankfurt.de/PARLISLINK/DDW?W=DOK_NAME="
                        "'%s'" % (re.sub("\n", "", line), ))
                
                #Some output for the user
                print "Nummer %i (%s)" % (len(collectedPropositions) + 1, link)
                
                try:
                    proposition = self._getPropositionFromExtractor(link)
                    collectedPropositions.append(proposition)
                except Exception, err:
                    print 'Failed to get proposition from %s: %s' % (link, err)
                    traceback.print_exc()
                
                #Wait a few seconds so the server can handle the load...
                time.sleep(self.sleepingTimeInSeconds)
        except IOError, ioe:
            print "Error reading from file '%s':\n%s" % (inputFile, ioe)
        
        return sorted(collectedPropositions, key=lambda prop: prop.updateDate,
                      reverse=True)
            
    def _needs2006Workaround(self):
        """
        Checks if the instances needs to make use of some workarounds for 2006.
        
        @return: True if a workaround is required. False if not.
        @rtype: boolean
        """
        return (self.year == 2006)
    
    def _needs1990sWorkaround(self):
        """
        Checks if the instances needs to make use of some workarounds for 1990s.
        
        @return: True if a workaround is required. False if not.
        @rtype: boolean
        """
        return (self.year >= 1990 and self.year <= 1994)
    
    def _needs2003Workaround(self):
        """
        Checks if the instances needs to make use of some workarounds for 2003s.
        
        @return: True if a workaround is required. False if not.
        @rtype: boolean
        """
        return (self.year >= 1995 and self.year <= 2003)
    
    def startScraping(self):
        """
        Start the scraping.
        """
        print "Starting to scrape..."
        scrapedPropositions = self.__loadIndex(self.inputFile)
        print "Finished scraping"
        
        return scrapedPropositions
        
    def __repr__(self):
        """
        String representation of the object.
        
        Built-in python function.
        """
        return "Scraper for %s. Outputfile: %s, Inputfile: %s, Delay between scraping files: %s seconds" % (self.year, self.outputFile, self.inputFile, self.sleepingTimeInSeconds)
#end class ParlisScraper
