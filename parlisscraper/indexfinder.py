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
    This class can be used to retrieve a list of IDs that can be used for scraping.
    It will create a file called 'YYYY-IDlist.txt' where YYYY is the year.
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
        self.start = 1
        self.end = 20
        self.searchDelay = 5

        self.year = year
        self.outputFile = outputFile

        self.retrievedTotalNumberOfDocuments = False
        self.collectedItems = []

        self.linkToDocumentPattern = re.compile(r"/PARLISLINK/DDW\?W%3DVORLAGEART\+INC\+%27OF%27\+AND\+JAHR\+%3D\+(?P<year>\d{4})\+AND\+DOKUMENTTYP\+%3D\+%27VORL%27\+ORDER\+BY\+SORTFELD/Descend%26M%3D\d+%26K%3D(?P<documentID>OF_\d{1,4}-\d{1,2}_\d{4})%26R%3DY%22%26U%3D1", re.IGNORECASE)
        self.itemCountPattern = re.compile("Dokumente:.*von\W+(?P<documentCount>\d+)")

    def __getLinkList(self):
        """
        Get a list with links.

        @param year: The year for which the links should be received. Should be in format YYYY.
        @type year: int
        @param start: How many links to skip
        @type start: int
        @return: A list with links.
        @rtype: list
        """
        linkListe = []

        #Build the link to the page that contains the links
        linkcon = ("http://www.stvv.frankfurt.de/PARLISLINK/SDW?"
            "W%3DVORLAGEART+INC+%27OF%27+AND+JAHR+%3D+{year}+AND+"
            "DOKUMENTTYP+%3D+%27VORL%27+ORDER+BY+SORTFELD/Descend"
            "%26M%3D{startingpoint}%26R%3DY%22".format(
                startingpoint=self.start,
                year=self.year
            )
        )

        try:
            page = urlopen(linkcon)
            soup = BeautifulSoup(page)

            linkListe = soup.findAll('a')

            if self.retrievedTotalNumberOfDocuments is False:
                self.end = self.__getTotalNumberOfDocuments(soup)
                self.retrievedTotalNumberOfDocuments = True
        except AttributeError as aerr:
            #This is mostly a failure of getting the total number of items.
            LOGGER.error("Aborting the search for indexes: {0}".format(aerr))
            self.end = 0
        except Exception as err:
            #Problems? Give out some information
            LOGGER.error(err)

        return linkListe

    def __graspID(self, listWithLinks):
        """
        Search for IDs.

        @param listWithLinks: A list with links. Format tbd.
        @type listWithLinks: list
        @return: list with links to documents.
        @rtype: list
        """
        for singleLink in listWithLinks:
            link = str(singleLink)

            match = self.linkToDocumentPattern.search(link)
            if match:
                vorlagennummer = match.group('documentID')

                if vorlagennummer:
                    yield vorlagennummer


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

    def startSearching(self):
        """
        Starts the search for indexes and writes the results into a file.
        """
        LOGGER.info("Starting to search for indexes")
        self.collectedItems = set()

        with open(self.outputFile, "w") as filehandle:
            while self.start < self.end:
                links = self.__getLinkList()

                for documentID in self.__graspID(links):
                    if documentID not in self.collectedItems:
                        self.collectedItems.add(documentID)
                        filehandle.write("{0}\n".format(documentID))

            LOGGER.info("Year {year}: {0} items left to process".format(self.end - self.start, year=self.year))
            self.start += 20

            #sleep a little bit. We don't want to crash the server (poor hardware ;))
            time.sleep(self.searchDelay)

        LOGGER.info("Finished scraping the indexes.")

    def __repr__(self):
        """
        String representation of the object.

        Built-in python function.
        """
        return "{classname}({year}, outputFile={file})".format(
            classname=self.__class__.__name__,
            year=self.year,
            outputFile=self.outputFile
        )
