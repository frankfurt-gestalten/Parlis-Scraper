# Parlis Scraper

## Introduction

The City of Frankfurt am Main / Germany offers information about the work of its city counsil in the so called Parlamentsinformationssystem (PARLIS; http://www.stvv.frankfurt.de/parlis2/index.htm).
Since there is no way to easily access the system via some API this is an approach to get the data there into formats that can be processed otherwise.
Besides that the usability of the system is - politely expressed - not very optimal (as is the HTML markup).

## Dependencies

* BeautifulSoup - http://pypi.python.org/pypi/BeautifulSoup/
* requests

## Installation

  git clone https://github.com/Frankfurt-Gestalten/Parlis-Scraper.git
  pip install Parlis-Scraper

## Usage

After successful installation you can use the ``parlisscraper`` command
for easy scraping.

  parlisscraper --startYear 2014

For more options please refer to ``parlisscraper --help``.

## Parts

The scraper consists of some indepedent parts.

### ParlisIndexFinder

It searches for document IDs from the parlis system that can be scraped later on.

### ParlisScraper

Does the actual scraping. Uses DataExtractors to retrieve the required
information from the page.

### DataExtractor

A DataExtractor that is used to parse the pages and split
them into the parts we use for further processing.

### Exporters

There are some basic exporters so the retrieved data will be persistent.
Currently we support an export into CSV and XML.


## ToDo

Some ideas that have been floating around for a while and may be a good starting point if you want to contribute.

* Support more document formats. Parlis holds a lot more information than we currently are able to scrape.
* More export formats
* Create awesome stuff with the retrieved data (yeah, we encourage you to do that!) (how about an easy to use interface?)
* Write tests :)
* Let the scraper decide for a year based on the DOK_NAME in the url (= the link parts the indexfinder creates)
