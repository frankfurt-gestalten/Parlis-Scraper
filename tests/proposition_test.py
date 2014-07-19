# -*- coding: utf-8 -*-

import unittest

from parlisscraper.proposition import Proposition


class PropositionTest(unittest.TestCase):
	def setUp(self):
		self.prop = Proposition('foo', 20120430, 'http://www.frankfurt-gestalten.de', 'APPD', 'OF_1234', 1234)

	def tearDown(self):
		del self.prop

	def testTitle(self):
		self.assertEqual('foo', self.prop.title)

	def testURL(self):
		self.assertEqual('http://www.frankfurt-gestalten.de', self.prop.link)

	def testParty(self):
		self.assertEqual('APPD', self.prop.party)
