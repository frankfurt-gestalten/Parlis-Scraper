#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
This modules creates a list of files names for use with the parlis scraper.

It will create a file called 'YYYY-IDlist.txt' where YYYY is the year.
"""
import logging
import re
import time

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

from bs4 import BeautifulSoup

LOGGER = logging.getLogger('parlisscraper')


class ParlisIndexFinder(object):
    """
    This class can be used to retrieve a list of documents IDs that can
    be used for scraping.

    It will create a file called 'YYYY-IDlist.txt' where YYYY is the
    year if no output file will be specified.
    """

    def __init__(self, year, outputFile=None):
        """
        Constructor

        @param year: The year for which the IDs shall be retrieved.
        @type year: int
        @param outputFile: Overrides the default output-file.
        @type outputFile: string
        """
        if outputFile is None:
            outputFile = "%s-IDlist.txt" % year

        # Configuration
        self.searchDelay = 2

        self.year = year
        self.outputFile = outputFile

        self.collectedItems = set()

        self.linkToDocumentPattern = re.compile(r"/PARLISLINK/DDW\?W%3DVORLAGEART\+INC\+%27OF%27\+AND\+JAHR\+%3D\+(?P<year>\d{4})\+AND\+DOKUMENTTYP\+%3D\+%27VORL%27\+ORDER\+BY\+SORTFELD/Descend%26M%3D\d+%26K%3D(?P<documentID>OF_\d{1,4}-\d{1,2}_\d{4})%26R%3DY%22%26U%3D1", re.IGNORECASE)
        self.itemCountPattern = re.compile("Dokumente:.*von\W+(?P<documentCount>\d+)")

    def startSearching(self):
        """
        Starts the search for indexes and writes the results into a file.
        """
        LOGGER.info("Starting to search for indexes for {0}".format(self.year))

        with open(self.outputFile, "w") as filehandle:
            for documentID in self._getDocumentIDs():
                if documentID not in self.collectedItems:
                    self.collectedItems.add(documentID)
                    filehandle.write("{0}\n".format(documentID))
                    LOGGER.info('.')

        LOGGER.info("Finished scraping the indexes.")

    def _getDocumentIDs(self):
        """
        Yields the document IDs for the current year.
        """
        for singleLink in self._getLinksFromOverview():
            link = str(singleLink)

            match = self.linkToDocumentPattern.search(link)
            if match:
                vorlagennummer = match.group('documentID')

                if vorlagennummer:
                    yield vorlagennummer

    def _getLinksFromOverview(self):
        """
        Yields the links to documents scraped from the overview pages.
        """
        start = 0
        end = 20
        retrievedTotalNumberOfDocuments = False

        while start < end:
            #Build the link to the page that contains the links
            linkcon = ("http://www.stvv.frankfurt.de/PARLISLINK/SDW?"
                "W%3DVORLAGEART+INC+%27OF%27+AND+JAHR+%3D+{year}+AND+"
                "DOKUMENTTYP+%3D+%27VORL%27+ORDER+BY+SORTFELD/Descend"
                "%26M%3D{startingpoint}%26R%3DY%22".format(
                    startingpoint=start,
                    year=self.year
                )
            )

            try:
                page = urlopen(linkcon)
                soup = BeautifulSoup(page)

                if not retrievedTotalNumberOfDocuments:
                    end = self.__getTotalNumberOfDocuments(soup)
                    retrievedTotalNumberOfDocuments = True

                for link in soup.findAll('a'):
                    yield link

            except AttributeError as aerr:
                #This is mostly a failure of getting the total number of items.
                LOGGER.error("Aborting the search for indexes: {0}".format(aerr))
                break

            LOGGER.info("Year {year}: {0} items left to process".format(end - start, year=self.year))
            start += 20

            #sleep a little bit. We don't want to crash the server (poor hardware ;))
            time.sleep(self.searchDelay)

    def __getTotalNumberOfDocuments(self, soupInstance):
        """
        Reads the total number of documents from the contents of the soup.

        @param soupInstance: A page containing the overall document count somewhere.
        @type soupInstance: BeautifulSoup
        @return: Total number of document for this year.
        @rtype: str
        """
        pageContent = str(soupInstance)
        patternResults = self.itemCountPattern.search(pageContent)
        itemCount = int(patternResults.group('documentCount'))

        LOGGER.info("Found total number of {0} documents".format(itemCount))

        return itemCount

    def __repr__(self):
        return "{classname}({year}, outputFile={file})".format(
            classname=self.__class__.__name__,
            year=self.year,
            outputFile=self.outputFile
        )
