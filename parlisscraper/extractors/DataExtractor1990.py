'''
Created on 09.10.2011

@author: niko
'''
import re

from parlisscraper.extractors.DataExtractor import DataExtractor


class DataExtractor1990(DataExtractor):

    def _getSubjectNoooooow(self, matchBetreff):
        bet = self._quoteChange(matchBetreff.group(0))
        bet2 = re.sub("Betreff: </p>", "", bet)
        returnSubject = re.sub("Begr\xc3\xbcndung:", "", bet2)

        return returnSubject

    def _getTitleMatch(self, matchTitle):
        return matchTitle.group(1)
