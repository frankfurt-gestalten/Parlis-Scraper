'''
Created on 09.10.2011

@author: niko
'''
import re
from DataExtractor import DataExtractor


class DataExtractor2003(DataExtractor):
    '''
    classdocs
    '''
    def _getSubjectPattern(self):
        return "Betreff:(.*)Antragstellende Fraktion:"
    
    def _getPartyPattern(self):
        return "Antragstellende Fraktion:(.*)Vertraulichkeit:"
    
    def _getStatementPattern(self):
        return "Begr\xc3\xbcndung:</p>(.*)Antragstellende Fraktion:"
    
    def _getSubjectNoooooow(self, matchBetreff):
        bet = self._quoteChange(matchBetreff.group(0))
        bet2 = re.sub("Betreff: </p>", "", bet)
        returnSubject = re.sub("Begr\xc3\xbcndung:", "", bet2)
        
        return returnSubject
    
    def _getTitleMatch(self, matchTitle):
        return matchTitle.group(1)
    
    def _getAntragstellerPattern(self):
        return "Antragstellende Fraktion:"
