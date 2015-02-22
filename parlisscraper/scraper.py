#! /usr/bin/python
# -*- coding: utf-8 -*-

# parlisscraper - Scraper for city of Frankfurt / Main's PARLIS
# Copyright (C) 2011-2015 Niko Wenselowski

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
This is the PARLIS scraper module.

It will retrieve the pages from parlis and store there contents
in a .csv-file.

:author: Niko Wenselowski <der@nik0.de>
:license: GNU Affero General Public License version 3
"""

from __future__ import absolute_import

import logging
import requests
import time
import traceback

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
    def __init__(self, year, documentIDs=None, scrapingDelayInSeconds=1):
        """
        Constructor.
        The year is used to specify the filenames.
        If it is wished the filenames can be overridden.

        @param year: The year what shall be parsed
        @type year: int
        :param documentIDs: An iterator with IDs of the documents to scrape
        @param outputFile: File into wich the data is saved.
        @type outputFile: str
        """
        self.year = year
        self._documentIDs = documentIDs
        self.sleepingTimeInSeconds = scrapingDelayInSeconds

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
            page = requests.get(link).text
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
        for documentId in self._documentIDs:
            link = "http://stvv.frankfurt.de/PARLISLINK/DDW?W=DOK_NAME='{id}'".format(
                id=documentId.replace('\n', '')
            )

            LOGGER.debug('Scraping {0}'.format(link))

            try:
                yield self._getPropositionFromExtractor(link)
            except Exception as err:
                LOGGER.error('Failed to get proposition from {link}: {error}'.format(link=link, error=err))

            #Wait a few seconds so the server can handle the load...
            time.sleep(self.sleepingTimeInSeconds)

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
        LOGGER.info("Starting to scrape {0}...".format(self.year))
        for proposition in self.__loadIndex():
            yield proposition
        LOGGER.info("Finished scraping")

    def __iter__(self):
        return (proposition for proposition in self.__loadIndex())

    def __repr__(self):
        """
        String representation of the object.

        Built-in python function.
        """
        return ("<{class}({year}, documentIDs={documentIDs}, "
                "scrapingDelayInSeconds={delay})>").format(year=self.year,
                                                           documentIDs=self._documentIDs,
                                                           scrapingDelayInSeconds=self.sleepingTimeInSeconds)
