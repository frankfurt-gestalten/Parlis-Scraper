import xml.dom

from parlisscraper.exporters import BaseExporter


class XMLExporter(BaseExporter):
    """
    This class creates XML
    """

    def __init__(self, filename, limit=0):
        self.xmlfile = filename
        self.limit = limit

    def createExport(self, propositions):
        implement = xml.dom.getDOMImplementation()
        xmlDocument = implement.createDocument(
            None, "PARLIS_propositions", None)

        for (index, proposition) in enumerate(propositions, start=1):
            if self.limit and index > self.limit:
                break

            xmlDocument.documentElement.appendChild(
                self._createDOMEntryFromProposition(xmlDocument, proposition))

        with open(self.xmlfile, 'w') as fileWriter:
            xmlDocument.writexml(fileWriter, '\n', ' ')

    def _createDOMEntryFromProposition(self, document, proposition):
        def createDOMElement(parentElement, name, value):
            element = document.createElement(name)
            parentElement.appendChild(element)
            nameTextElem = document.createTextNode(str(value))
            element.appendChild(nameTextElem)

            return element

        propositionElement = document.createElement("Proposition")

        propositionElement.appendChild(
            createDOMElement(propositionElement, "link", proposition.link))
        propositionElement.appendChild(
            createDOMElement(propositionElement, "update_date", proposition.updateDate))
        propositionElement.appendChild(
            createDOMElement(propositionElement, "date", proposition.date))
        propositionElement.appendChild(
            createDOMElement(propositionElement, "party", proposition.party))
        propositionElement.appendChild(
            createDOMElement(propositionElement, "proposition_number", proposition.proposition_nbr))
        propositionElement.appendChild(
            createDOMElement(propositionElement, "ob_number", proposition.obnumber))
        propositionElement.appendChild(
            createDOMElement(propositionElement, "title", proposition.title))
        propositionElement.appendChild(
            createDOMElement(propositionElement, "statement", proposition.statement))
        propositionElement.appendChild(
            createDOMElement(propositionElement, "subject", proposition.subject))
        propositionElement.appendChild(
            createDOMElement(propositionElement, "result", proposition.result))

        return propositionElement
