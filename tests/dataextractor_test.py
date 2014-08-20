#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

from bs4 import BeautifulSoup

from parlisscraper.extractors.DataExtractor import DataExtractor


class DataExtractorTestCase(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(os.path.dirname(__file__), 'OF_1068-6_2014.html')) as f:
            self.extractor = DataExtractor("http://stvv.frankfurt.de/PARLISLINK/DDW?W=DOK_NAME='OF_1068-6_2014'", BeautifulSoup(f))

    def tearDown(self):
        del self.extractor

    def testGetLink(self):
        self.assertEquals(
            "http://stvv.frankfurt.de/PARLISLINK/DDW?W=DOK_NAME='OF_1068-6_2014'",
            self.extractor.getLink()
        )

    def testGetTitle(self):
        self.assertEquals('Trauerhalle in Zeilsheim',
                          self.extractor.getTitle())

    def testGetParty(self):
        self.assertEquals('SPD',
                          self.extractor.getParty())

    def testGetStatement(self):
        self.assertEquals('',
                          self.extractor.getStatement())

    def testGetUpdateDate(self):
        self.assertEquals('2014-07-16',
                          self.extractor.getUpdateDate())

    def testGetPropositionNumber(self):
        self.assertEquals('OF 1068/6', self.extractor.getPropositionNumber())

    def testGetOBNumber(self):
        self.assertEquals('6', self.extractor.getOBNumber())

    def testGetDate(self):
        self.assertEquals('2014-06-07', self.extractor.getDate())

    # def testGetResult(self):
    #     #     self.maxDiff = None
    #     self.assertEquals('2014-07-16',
    #                       self.extractor.getResult())

    # def test__repr__(self):
    #     extractor_repr = repr(self.extractor)

    #     self.assertFalse(extractor_repr)

    # def testGetSubject(self):
    #     self.maxDiff = None
    #     self.assertEquals('Trauerhalle in Zeilsheim',
    #                       self.extractor.getSubject())


if __name__ == '__main__':
    unittest.main()