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
        
class XMLExporter(Exporter):
    """
    This class creates XML 
    """
    def __init__(self, filename):
        self.xmlfile = filename
        
    def createExport(self, propositions):                
        implement = xml.dom.getDOMImplementation()
        xmlDocument = implement.createDocument(None, "PARLIS_propositions", None)
        
        for proposition in propositions:
            if proposition is not None:
                assert isinstance(proposition, Proposition)
                
                xmlDocument.documentElement.appendChild(self._createDOMEntryFromProposition(xmlDocument, proposition))
        
        fileWriter = open(self.xmlfile, 'w')    
        xmlDocument.writexml(fileWriter, '\n', ' ')
        fileWriter.close()
    
    def _createDOMEntryFromProposition(self, document, proposition):
        def createDOMElement(parentElement, name, value):
            element = document.createElement(name)
            parentElement.appendChild(element)
            nameTextElem = document.createTextNode(str(value))
            element.appendChild(nameTextElem)
            
            return element
        
        assert isinstance(proposition, Proposition)
        propositionElement = document.createElement("Proposition")
        
        propositionElement.appendChild(createDOMElement(propositionElement, "link", proposition.link))
        propositionElement.appendChild(createDOMElement(propositionElement, "update_date", proposition.updateDate))
        propositionElement.appendChild(createDOMElement(propositionElement, "date", proposition.date))
        propositionElement.appendChild(createDOMElement(propositionElement, "party", proposition.party))
        propositionElement.appendChild(createDOMElement(propositionElement, "proposition_number", proposition.proposition_nbr))
        propositionElement.appendChild(createDOMElement(propositionElement, "ob_number", proposition.obnumber))
        propositionElement.appendChild(createDOMElement(propositionElement, "title", proposition.title))
        propositionElement.appendChild(createDOMElement(propositionElement, "statement", proposition.statement))
        propositionElement.appendChild(createDOMElement(propositionElement, "subject", proposition.subject))
        propositionElement.appendChild(createDOMElement(propositionElement, "result", proposition.result))
        return propositionElement