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
Proposition documents.

:author: Niko Wenselowski <der@nik0.de>
:license: GNU Affero General Public License version 3
"""


class Proposition(object):
    """
    A single proposition document.
    """
    def __init__(self, title, date, link, party, proposition_number, obnumber):
        """
        Constructor.

        :param title: The title of the document.
        :param date: The date that document records.
        :param link: Link to the document.
        :param party: The party that initiated the proposition.
        :param obnumber: Number of the proposition.
        """
        self.title = title
        self.date = date
        self.link = link
        self.party = party
        self.proposition_nbr = proposition_number
        self.obnumber = obnumber

        self.updateDate = None
        self.statement = None
        self.subject = None
        self.result = None

    def __repr__(self):
        return ("Proposition({title}, {date}, {link}, {party}, "
                "{proposition_number}, {obnumber})".format(
                    title=repr(self.title),
                    date=self.date,
                    link=self.link,
                    party=self.party,
                    proposition_number=self.proposition_nbr,
                    obnumber=self.obnumber
            )
        )
