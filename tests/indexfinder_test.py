# -*- coding: utf-8 -*-
import unittest

from parlisscraper.indexfinder import ParlisIndexFinder


class IndexFinderTestCase(unittest.TestCase):
    def setUp(self):
        self.indexfinder = ParlisIndexFinder(2014)

    def tearDown(self):
        del self.indexfinder

    def testYear(self):
        self.assertEqual(2014, self.indexfinder.year)

    def testFilenameIsSet(self):
        self.assertTrue(self.indexfinder.outputFile)

    def testLinkFindingPattern(self):
        unmatching_links = [
            '<a href="/PARLISLINK/SDW?W%3DVORLAGEART+INC+%27OF%27+AND+JAHR+%3D+2014+AND+DOKUMENTTYP+%3D+%27VORL%27+ORDER+BY+SORTFELD/Descend%26M%3D66%26R%3DY%22"><img src="/basisicons/mdown.png" alt="N&auml;chster Treffer" title="N&auml;chster Treffer" /></a>',
            '<a href="/PARLISLINK/SDW?W%3DVORLAGEART+INC+%27OF%27+AND+JAHR+%3D+2014+AND+DOKUMENTTYP+%3D+%27VORL%27+ORDER+BY+SORTFELD/Descend%26M%3D16%26R%3DY%22"><img src="/basisicons/mup.png" alt="Vorheriger Treffer" title="Vorheriger Treffer" /></a>',
            '<a href="/PARLISLINK/SDW?W%3DVORLAGEART+INC+%27OF%27+AND+JAHR+%3D+2014+AND+DOKUMENTTYP+%3D+%27VORL%27+ORDER+BY+SORTFELD/Descend%26M%3D1251%26R%3DY%22"><img src="/basisicons/mbottom.png" alt="Ende der Liste" title="Ende der Liste" /></a>',
            '<a href="#bottom" name="top"><img src="/basisicons/diverses/arrowdown2.gif" alt="Zum Ende der Seite" title="Zum Ende der Seite" /></a>',
            '<a class="flink" href="http://www.parlis.mobi/index.htm">Startseite</a>',
            '<a href="/PARLISLINK/SDW?W%3DVORLAGEART+INC+%27OF%27+AND+JAHR+%3D+2014+AND+DOKUMENTTYP+%3D+%27VORL%27+ORDER+BY+SORTFELD/Descend%26M%3D1%26R%3DY%22"><img src="/basisicons/mtop.png" alt="Anfang der Liste" title="Anfang der Liste" /></a>',
            '<a href="#top"><img src="/basisicons/diverses/arrowup2.gif" alt="Zum Anfang der Seite" title="Zum Anfang der Seite" /></a>',
            '<a name="bottom"></a>'
        ]

        for link in unmatching_links:
            self.assertFalse(self.indexfinder.linkToDocumentPattern.search(link))

        wanted_links = [
            '<a href="/PARLISLINK/DDW?W%3DVORLAGEART+INC+%27OF%27+AND+JAHR+%3D+2014+AND+DOKUMENTTYP+%3D+%27VORL%27+ORDER+BY+SORTFELD/Descend%26M%3D41%26K%3DOF_1038-6_2014%26R%3DY%22%26U%3D1">Bebauungsplan Nr. 911 - Nördlich Straßburger Straße</a>',
            '<a href="/PARLISLINK/DDW?W%3DVORLAGEART+INC+%27OF%27+AND+JAHR+%3D+2014+AND+DOKUMENTTYP+%3D+%27VORL%27+ORDER+BY+SORTFELD/Descend%26M%3D42%26K%3DOF_1037-6_2014%26R%3DY%22%26U%3D1">Maßvolle Bebauung in Sindlingen - Grüne Lunge erhalten und verbessern</a>',
            '<a href="/PARLISLINK/DDW?W%3DVORLAGEART+INC+%27OF%27+AND+JAHR+%3D+2014+AND+DOKUMENTTYP+%3D+%27VORL%27+ORDER+BY+SORTFELD/Descend%26M%3D43%26K%3DOF_1036-6_2014%26R%3DY%22%26U%3D1">Sicherheit für spielende Kinder in der Parkstadt Unterliederbach</a>',
            '<a href="/PARLISLINK/DDW?W%3DVORLAGEART+INC+%27OF%27+AND+JAHR+%3D+2014+AND+DOKUMENTTYP+%3D+%27VORL%27+ORDER+BY+SORTFELD/Descend%26M%3D52%26K%3DOF_1027-6_2014%26R%3DY%22%26U%3D1">Geländer auf dem Bürgersteig im Nieder Kirchweg entfernen</a>',
        ]

        for link in wanted_links:
            match = self.indexfinder.linkToDocumentPattern.search(link)

            self.assertTrue(match)
            self.assertTrue(match.group('documentID'))
