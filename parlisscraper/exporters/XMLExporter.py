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
Export data into an XML file.

:author: Niko Wenselowski <der@nik0.de>
:license: GNU Affero General Public License version 3
"""

from __future__ import absolute_import

import xml.dom

from .basicexporter import BaseExporter


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
