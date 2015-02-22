#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Basic workflow for scraping documents.

:author: Niko Wenselowski <der@nik0.de>
:license: GNU Affero General Public License version 3
"""
import datetime
import logging

from parlisscraper.exporters.CSVExporter import CSVExporter
from parlisscraper.indexfinder import ParlisIndexFinder
from parlisscraper.scraper import ParlisScraper

LOGGER = logging.getLogger('parlisscraper')


def startWorkflow(startYear=None, endYear=None, onlySearchIndexes=False,
                  onlyScrapeFiles=False, exportLimit=None):
    if startYear is None:
        startYear = 1992

    if endYear is None:
        endYear = datetime.date.today().year

    for year in range(startYear, endYear + 1):
        LOGGER.info("Processing year {0}".format(year))

        if not onlyScrapeFiles:
            indexer = ParlisIndexFinder(year)
        else:
            indexer = open('{year}-IDlist.txt'.format(year=year))

        if not onlySearchIndexes:
            scraper = ParlisScraper(year, indexer)

            csvExporter = CSVExporter("{0}-antraege.csv".format(year),
                                      exportLimit)
            csvExporter.createExport(scraper)
        else:
            with open('{year}-IDlist.txt'.format(year=year), "w") as output:
                for documentId in indexer:
                    output.write('{id}\n'.format(id=documentId))
