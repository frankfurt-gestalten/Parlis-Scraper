#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Propositions.

Created on 03.10.2011

:author: Niko Wenselowski
'''


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
