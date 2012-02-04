'''
This module contains various classes to export the retrieved data.

@author: Niko Wenselowski
'''
from csv import writer
import xml.dom
from scraper import Proposition

class Exporter(object):
    '''
    Abstract base class to export Propositions.
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def createExport(self, propositions):
        '''
        Exports the given Propositions.
        
        @param *propositions: The propositions to export.
        @type **propositions: sequence of Proposition.
        '''
        pass
    
class CSVExporter(Exporter):
    '''
    A class to export the propositions into a .csv-file. 
    '''
    
    def __init__(self, filename):
        self.outputFile = filename
        
    def createExport(self, propositions):
        """
        This will append the proposition to the export file.
        """
        csvWriter = writer(
                           open(self.outputFile, 'ab'), 
                           delimiter=';', 
                           quotechar='"'
                           )
        header = ["update","link","date","partei","nummer","title","begruendung","betreff","ergebnisse", 'ob_nummer']
        csvWriter.writerow(header)
        i = 1
        for singleProposition in propositions:
            if(singleProposition is not None and i <= 500):
                assert isinstance(singleProposition, Proposition)
                csvWriter.writerow(self._createSequenceFromProposition(singleProposition))
                i +=1

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
	
