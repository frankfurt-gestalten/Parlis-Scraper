#! /usr/bin/env python
# -*- coding: utf-8 -*-

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
