'''
Created on 25.06.2011

@author: niko
'''
import datetime
import indexfinder
import scraper
import exporters
from optparse import OptionParser


def startWorkflow(startYear=None, endYear=None, onlySearchIndexes=False, onlyScrapeFiles=False):
	if startYear is None:
		startYear = 1992
		
	if endYear is None:
		endYear = datetime.date.today().year
		
	for year in range(startYear, endYear + 1):
		print "Processing year %s" % year
		
		if(onlyScrapeFiles == False):
			print "Start looking for indexes"
			indexer =  indexfinder.ParlisIndexFinder(year)
			indexer.startSearching()
			print "Finished looking for indexes"
		
		if(onlySearchIndexes == False):
			scrape = scraper.ParlisScraper(year) 
			
			scrapingResults = scrape.startScraping()
			try:
				csvExporter = exporters.CSVExporter(scrape.outputFile)
				csvExporter.createExport(scrapingResults)
			except Exception, err:
				print "%s\n-> Failed to write CSV. Writing XML." % (err, )
				xmlExporter = exporters.XMLExporter('%s.xml' % scrape.outputFile)
				xmlExporter.createExport(scrapingResults)


if __name__ == '__main__':
	optionParser = OptionParser()
	optionParser.add_option('-s', '--startYear', dest='startYear', type=int, default=1992, help='The year from which one the scraping shall start')
	optionParser.add_option('-e', '--endYear', dest='endYear', type=int, default=None, help='The year to which the scraping will work')
	optionParser.add_option('-i', '--onlyIndexes', dest='onlyIndexes', default=False, action="store_true", help='Only create index files.')
	optionParser.add_option('-d', '--onlyScraping', dest='onlyScraping', default=False, action="store_true", help='Only scrape webpages.')
	
	(options, unparseableArguments) = optionParser.parse_args()
	
	startWorkflow(options.startYear, options.endYear, options.onlyIndexes, options.onlyScraping)
