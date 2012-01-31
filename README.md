Parlis Scraper
==============

Introduction
------------
The City of Frankfurt am Main / Germany offers information about the work of its city counsil in the so called Parlamentsinformationssystem (PARLIS; http://www.stvv.frankfurt.de/parlis2/index.htm).
Since there is no way to easily access the system via some API this is an approach to get the data there into formats that can be processed otherwise.
Besides that the usability of the system is - politely expressed - not very optimal (as is the HTML markup).

Dependencies
------------
* BeautifulSoup - http://pypi.python.org/pypi/BeautifulSoup/


Function
--------
There are three main components.
The first one is the ParlisIndexFinder. It searches for document IDs from the parlis system that can be scraped later on. The IDs are stored in a text file.
The second one is ParlisScraper. It accesses the pages, uses a matching DataExtractor to get the content of the page and then returns an list of Proposition-objects with the information of the single propositions.
The third component is the one that exports the retrieved propositions.


ToDo
----
Some ideas that have been floating around for a while and may be a good starting point if you want to contribute.

* Nicer packages. And moooore!
* Support more document formats. Parlis holds a lot more information than we currently are able to scrape.
* Implementing the scraper and/or indexfinder as generators.
* More export formats
* Create awesome stuff with the retrieved data (yeah, we encourage you to do that!) (how about an easy to use interface?)
* Test how much load the upgraded PARLIS hardware can handle. There have been problems in the past and it would be nice to speed up the retrival from the website. Right now there is a delay between getting the pages to avoid crashing servers ;)
* Easier commandline usage.
* Write tests :)

