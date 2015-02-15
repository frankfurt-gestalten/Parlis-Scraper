#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is the PARLIS scraper module.

It will retrieve the pages from parlis and store there contents in a .csv-file.
"""
from __future__ import absolute_import

import csv
import logging
import re
import time
import traceback

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

from bs4 import BeautifulSoup

from .proposition import Proposition
from .extractors import (DataExtractor, DataExtractor1990, DataExtractor2003,
                         DataExtractor2006)

LOGGER = logging.getLogger('parlisscraper')


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
        if inputFile is None:
            inputFile = "%s-IDlist.txt" % year

        if outputFile is None:
            outputFile = "%s-antraege.csv" % year

        self.year = year
        self.outputFile = outputFile
        self.inputFile = inputFile
        self.sleepingTimeInSeconds = 3

    def _getExtractor(self, link):
        if self._needs1990sWorkaround():
            return DataExtractor1990(link, self._getPage(link))
        elif self._needs2003Workaround():
            return DataExtractor2003(link, self._getPage(link))
        elif self._needs2006Workaround():
            return DataExtractor2006(link, self._getPage(link))
        else:
            return DataExtractor(link, self._getPage(link))

    def _getPage(self, link):
        """
        Receives the content of the supplied url.

        @param link: URL to the page to retrieve.
        @type link: str
        @return: A BeautifulSoup-instance for the supplied url.
                 None if no page could be retrieved.
        @type: BeautifulSoup
        """
        try:
            page = urlopen(link)
            return BeautifulSoup(page, 'lxml')
        except Exception as err:
            LOGGER.error("Error receiving '{link}': {error}".format(link=link, error=err))

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
        except Exception as err:
            LOGGER.error('Could not extract all the needed data (extractor: {0}): {error}'.format(extractor, error=err))
            traceback.print_exc()
            raise err

        return proposition

    def __loadIndex(self):
        """
        Starts processing of the supplied file.
        Reads the content of the files, creates a link from it and then
        starts scraping that page.
        The output is saved to a file.

        @param inputFile: input file with information to create the links.
        @type inputFile: str
        """
        proposition_links = set()
        with open(inputFile, 'r') as inputFileHandle:
            for line in inputFileHandle:
                #Create url
                link = "http://stvv.frankfurt.de/PARLISLINK/DDW?W=DOK_NAME='{id}'".format(
                    id=re.sub("\n", "", line)
                )
                proposition_links.add(link)

        collectedPropositions = []
        for link in sorted(proposition_links):
            LOGGER.info("Nummer {0} ({link})".format(len(collectedPropositions) + 1, link=link))

            try:
                proposition = self._getPropositionFromExtractor(link)
                collectedPropositions.append(proposition)
            except Exception as err:
                LOGGER.error('Failed to get proposition from {link}: {error}'.format(link=link, error=err))
                traceback.print_exc()

            #Wait a few seconds so the server can handle the load...
            time.sleep(self.sleepingTimeInSeconds)

        return collectedPropositions

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
        LOGGER.info("Starting to scrape...")
        scrapedPropositions = self.__loadIndex(self.inputFile)
        LOGGER.info("Finished scraping")

        return scrapedPropositions

    def __repr__(self):
        """
        String representation of the object.

        Built-in python function.
        """
        return "Scraper for %s. Outputfile: %s, Inputfile: %s, Delay between scraping files: %s seconds" % (self.year, self.outputFile, self.inputFile, self.sleepingTimeInSeconds)
#end class ParlisScraper
