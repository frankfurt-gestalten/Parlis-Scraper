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
Extractor for documents from 2006.

:author: Niko Wenselowski <der@nik0.de>
:license: GNU Affero General Public License version 3
"""
from __future__ import absolute_import

import re
from .DataExtractor import DataExtractor


class DataExtractor2006(DataExtractor):

    STATEMENT_REGEX = re.compile(u"Begr(\xc3\xbc|ü)ndung:</p>(?P<statement>.*)Antragstellende Fraktion:")

    def _getSubjectPattern(self):
        return "Betreff:(.*)Antragstellende Fraktion:"

    def _getPartyPattern(self):
        return "Antragstellende Fraktion:(.*)Vertraulichkeit:"

    def _getCSSclassTag(self):
        #TODO: Not sure if this is really needed that way. To be checked!
        return "class(\W)MsoNormal?"

    def _getSubjectNoooooow(self, matchBetreff):
        bet = self._quoteChange(matchBetreff.group(0))
        bet2 = re.sub("Betreff: </p>", "", bet)
        returnSubject = re.sub("Begr\xc3\xbcndung:", "", bet2)

        return returnSubject

    def _getSubjectWithAntragssteller(self, matchAntragssteller):
        return self._quoteChange(matchAntragssteller.group(0))

    def _getTitleMatch(self, matchTitle):
        return matchTitle.group(1)

    def _getAntragstellerPattern(self):
        return "Antragstellende Fraktion:"
