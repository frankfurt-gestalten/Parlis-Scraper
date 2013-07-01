#!/usr/bin/env python

from distutils.core import setup

setup(
    name='parlisscraper',
    version='0.3',
    description=('A scraper for the "Parlamentsinformationssystem" of '
                 'the city of Frankfurt am Main / Germany'),
    author='Niko Wenselowski',
    author_email='der@nik0.de',
    #url='http://www.frankfurt-gestalten.de/',
    requires=['BeautifulSoup (==3.2.0)'],
    packages=['parlisscraper', 'parlisscraper.exporters', 'parlisscraper.extractors'],
    scripts=['scripts/parlisscraper']
)
