# -*- coding: utf-8 -*-
'''
Created on 09.10.2011

@author: niko
'''
import re
from datetime import date


class DataExtractor(object):
    """
    This class is used to get data from a proposition page in PARLIS.
    """
    def __init__(self, link, pageContent):
        self._link = link
        self._pageContent = pageContent

        self._title = None
        self._date = None
        self._party = None
        self._proposition_nbr = None
        self._updateDate = None
        self._statement = None
        self._subject = None
        self._result = None

    def _getSourceCode(self):
        return str(self._pageContent)

    def getLink(self):
        return self._link

    def _quoteChange(self, text):
        """
        Removes the quotation mark (") from the text.

        @param text: Some text
        @type text: str
        @return: Cleaned version without quotation mark
        @rtype: str
        """
        return re.sub('"', '', text)

    def _getCSSclassTag(self):
        return " class=MsoNormal"

    def _cleanHTML(self, uncleanString):
        """
        Cleans before further processing.

        This includes removing and replacing specified tags.

        @param uncleanString: The string that shall be cleaned-
        @type uncleanString: str
        @return: The cleaned version of the string.
        @rtype: str
        """
        #Patterns...
        #...to remove:
        removeMS = self._getCSSclassTag()
        removeVer = "Vertraulichkeit:"
        removeBR = "<br />"
        removeLeer = "&nbsp;"
        removeBeg = "Begr\xc3\xbcndung:</p>"
        removeStyle = " style.*?>"
        removeA = "<a name.*?>"  # anchors inside the page
        removeTable = "tableTable\""
        removeP = "<p class=MsoNormal>&nbsp;.*?</p>"
        removeMSO = 'class="MsoNormal"'
        removeMSOB = 'class=MsoNormal'

        #...to replace:
        replaceA = "<a href=/PARLISLINK"
        removeRight = "align=right"

        replaceABy = "<a href=http://stvv.frankfurt.de/PARLISLINK"

        #Process...
        cleanPackage = uncleanString
        cleanPackage = re.sub(removeStyle, ">", cleanPackage)
        cleanPackage = re.sub(removeA, " ", cleanPackage)
        cleanPackage = re.sub(removeMS, "", cleanPackage)
        cleanPackage = re.sub(removeBeg, "", cleanPackage)
        cleanPackage = re.sub(replaceA, replaceABy, cleanPackage)
        cleanPackage = re.sub(removeLeer, " ", cleanPackage)
        cleanPackage = re.sub(removeBR, " ", cleanPackage)
        cleanPackage = re.sub(removeRight, "", cleanPackage)
        cleanPackage = re.sub(removeTable, "table ", cleanPackage)
        cleanPackage = re.sub(removeP, "", cleanPackage)
        cleanPackage = re.sub(removeMSO, "", cleanPackage)
        cleanPackage = re.sub(removeMSOB, "", cleanPackage)

        return cleanPackage

    def _getTitleMatch(self, matchTitle):
        return re.sub("\.", "\"", matchTitle.group(1))

    def _extractTitle(self):
        return self._getTitleMatch(re.search("var titel = '(.*)';",
                                   self._getSourceCode()))

    def getTitle(self):
        if(not self._title):
            self._title = self._extractTitle()

        return self._title

    def _getSubjectPattern(self):
        return "Betreff:(.*)Antragsteller:"

    def _getSubjectNoooooow(self, matchBetreff):
        bet = re.sub("Betreff: </p>", "", matchBetreff.group(0))
        returnSubject = re.sub("Begr\xc3\xbcndung:", "", bet)
        returnSubject = self._cleanHTML(returnSubject)
        returnSubject = re.sub("<p class=MsoNormal>&nbsp;.*?</p>",
                               "",
                               returnSubject)

        return returnSubject

    def _getSubjectWithAntragssteller(self, matchAntragssteller):
        return self._cleanHTML(matchAntragssteller.group(0))

    def _extractSubject(self):
        matchBetreff = re.search("Betreff:(.*)Begr\xc3\xbcndung:",
                                 self._getSourceCode())
        matchAntragssteller = re.search(self._getSubjectPattern(),
                                        self._getSourceCode())

        if not (matchBetreff is None):
            returnSubject = self._getSubjectNoooooow(matchBetreff)
        elif not (matchAntragssteller is None):
            returnSubject = re.sub("Betreff: </p>", "", self._getSubjectWithAntragssteller(matchAntragssteller))
        else:
            returnSubject = " "
            print("Betreff leer")

        #TODO: add function that removes all HTML tags
        returnSubject = re.sub("Antragsteller:", "", returnSubject)
        return returnSubject

    def getSubject(self):
        if(not self._subject):
            self._subject = self._extractSubject()

        return self._subject

    def _extractUpdateDate(self):
        javascriptCode = self._getSourceCode()
        matchDate = re.search("letzte Aktualisierung des Sachstandes:(.*)(\d{1,2}).(\d{1,2}).(\d{4})", javascriptCode)

        try:
            newDate = re.sub("letzte Aktualisierung des Sachstandes: ", "", matchDate.group(0))

            splittedDate = newDate.split('.')
            return date(int(splittedDate[2]), int(splittedDate[1]), int(splittedDate[0])).isoformat()
        except AttributeError:
            print "Could not get update date, assigning None."
            return None

    def getUpdateDate(self):
        if(not self._updateDate):
            self._updateDate = self._extractUpdateDate()

        return self._updateDate

    def _getPartyPattern(self):
        return "Antragsteller:(.*)Vertraulichkeit:"

    def _getAntragstellerPattern(self):
        return "Antragsteller:"

    def _extractParty(self):
        partei = ""

        matchPartei = re.search(self._getPartyPattern(), self._getSourceCode())
        if (matchPartei != None):
            cleanPartei = self._cleanHTML(matchPartei.group(1))

            #RE compilen für bessere performance. Case-insensitive matching
            reObj = re.compile("(FREIE WÄHLER|LINKE\.|[\wÜÖÄ]+)\s+", flags=re.I | re.L)

            parties = []

            for x in reObj.findall(cleanPartei):
                parties.append(x)

            partei = ', '.join(parties)
        else:
            print("Partei leer")

        return partei

    def getParty(self):
        if(not self._party):
            self._party = self._extractParty()

        return self._party

    def _getStatementPattern(self):
        return "Begr\xc3\xbcndung:</p>(.*)Antragsteller:"

    def _extractStatement(self):
        begruendung = ""

        matchBeg = re.search(self._getStatementPattern(), self._getSourceCode())

        if matchBeg != None:
            cleanBeg = self._quoteChange(matchBeg.group(0))
            begruendung = re.sub(self._getAntragstellerPattern(), "", cleanBeg)
            begruendung = self._cleanHTML(begruendung)
        else:

            print("Begruendung leer")

        return begruendung

    def getStatement(self):
        if(not self._statement):
            self._statement = self._extractStatement()

        return self._statement

    def __extractTableInformation(self, table):
        tableInformation = re.sub("\[", "", table)
        tableInformation = re.sub("\]", "", tableInformation)

        return tableInformation

    def _extractResult(self):
        table = self._pageContent.findAll('table')
        matchErg = re.search("Beratungsergebnisse:</b>(.*)<table", self._getSourceCode())

        if matchErg is not None:
            ergebnisse = self._quoteChange(matchErg.group(0))
            ergebnisse = re.sub("<table", "", ergebnisse)
            ergebnisse = re.sub("Beratungsergebnisse:</b>", "", ergebnisse)

            ergebnisse = self._cleanHTML(ergebnisse)

            ergebnisse = ergebnisse + self._quoteChange(self.__extractTableInformation(str(table)))
        else:
            ergebnisse = " "
            print("Ergebnisse leer")

        #Zusatz weil clean html hier nicht funktioniert
        ergebnisse = re.sub("<p class=MsoNormal>&nbsp;.*?</p>", "", ergebnisse)
        ergebnisse = re.sub("class=MsoNormal", "", ergebnisse)
        ergebnisse = re.sub("align=right", "", ergebnisse)
        replaceA = "<a href=/PARLISLINK"
        replaceABy = "<a href=http://stvv.frankfurt.de/PARLISLINK"
        ergebnisse = re.sub(replaceA, replaceABy, ergebnisse)
		# setzt ein nofollow in alle Links nach Parlis
        ergebnisse = re.sub("(DOK_NAME=%27)(\w{1,2})(.*)(20\d{2}%27)>", "\\1\\2\\3\\4 target=blank rel=nofollow>", ergebnisse)
        return ergebnisse

    def getResult(self):
        if(not self._result):
            self._result = self._extractResult()

        return self._result

    def _extractPropositionNumber(self):
        numberSearchResults = re.search("OF(.)(\d{1,4})/(\d{1,2})", self._getSourceCode())
        nummer = numberSearchResults.group(0)

        return nummer

    def getPropositionNumber(self):
        if(not self._proposition_nbr):
            self._proposition_nbr = self._extractPropositionNumber()

        return self._proposition_nbr

    def getOBNumber(self):
        numberSearchResults = re.search("OF.\d{1,4}/(\d{1,2})", self._getSourceCode())
        nummer = numberSearchResults.group(1)

        return nummer

    def _extractDate(self):
        dateSearchResults = re.search("Antrag vom \d{1,2}.\d{1,2}.\d{4}", self._getSourceCode())

        if(dateSearchResults):
            newDate = dateSearchResults.group(0)
            newDate = newDate.replace('Antrag vom ', '')

            splittedDate = newDate.split('.')

            return date(
                        int(splittedDate[2]),
                        int(splittedDate[1]),
                        int(splittedDate[0])
                        ).isoformat()

    def getDate(self):
        if(not self._date):
            self._date = self._extractDate()

        return self._date

    def __repr__(self):
        return '%s for %s.\nContent: %s' % (self.__class__.__name__, self.getLink(), self._getSourceCode())
#end class DataExtractor
