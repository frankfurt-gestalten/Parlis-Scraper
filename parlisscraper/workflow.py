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
