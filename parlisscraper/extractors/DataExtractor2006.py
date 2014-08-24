#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 09.10.2011

@author: niko
'''
import re
from parlisscraper.extractors.DataExtractor import DataExtractor


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
