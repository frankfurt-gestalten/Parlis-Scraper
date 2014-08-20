#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

from parlisscraper.extractors.DataExtractor import DataExtractor


class DataExtractorTestCase(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(os.path.dirname(__file__), 'OF_1068-6_2014.html')) as f:
            self.extractor = DataExtractor("http://stvv.frankfurt.de/PARLISLINK/DDW?W=DOK_NAME='OF_1068-6_2014'", ''.join(f.readlines()))

    def tearDown(self):
        del self.extractor

    def testGetLink(self):
        self.assertEquals(
            "http://stvv.frankfurt.de/PARLISLINK/DDW?W=DOK_NAME='OF_1068-6_2014'",
            self.extractor.getLink()
        )


if __name__ == '__main__':
    unittest.main()