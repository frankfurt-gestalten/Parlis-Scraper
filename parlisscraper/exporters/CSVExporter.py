#! /usr/bin/env python
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
Exporting data into CSV files.

:author: Niko Wenselowski <der@nik0.de>
:license: GNU Affero General Public License version 3
"""

from __future__ import absolute_import

import logging
from csv import writer
from .basicexporter import BaseExporter

LOGGER = logging.getLogger('parlisscraper')


class CSVExporter(BaseExporter):
    '''
    A class to export the propositions into a .csv-file.
    '''

    def __init__(self, filename, limit=0):
        self.outputFile = filename
        self.limit = limit

    def createExport(self, propositions):
        """
        This will append the proposition to the export file.
        """
        with open(self.outputFile, 'a') as outputFile:
            csvWriter = writer(outputFile, delimiter=';', quotechar='"')
            header = ["update", "link", "date", "partei", "nummer", "title",
                      "begruendung", "betreff", "ergebnisse", 'ob_nummer']
            csvWriter.writerow(header)

            for (index, proposition) in enumerate(propositions, start=1):
                if self.limit and index > self.limit:
                    break

                LOGGER.info("CSV: wrote item {0}".format(index))
                csvWriter.writerow(self._createSequenceFromProposition(proposition))

    def _createSequenceFromProposition(self, proposition):
        return [
            proposition.updateDate,
            proposition.link,
            proposition.date,
            proposition.party,
            proposition.proposition_nbr,
            proposition.title,
            proposition.statement,
            proposition.subject,
            proposition.result,
            proposition.obnumber
        ]
