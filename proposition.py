'''
Created on 03.10.2011

@author: niko
'''

class Proposition(object):
    def __init__(self, title, date, link, party, proposition_number, obnumber):
        #mandatory
        self.__title = title
        self.__date = date
        self.__link = link
        self.__party = party
        self.__proposition_nbr = proposition_number
        self.__obnumber = obnumber
        
        #optional
        self.__updateDate = None
        self.__statement = None
        self.__subject = None
        self.__result = None

    def get_obnumber(self):
        return self.__obnumber


    def set_obnumber(self, value):
        self.__obnumber = value


    def del_obnumber(self):
        del self.__obnumber

    
    def get_title(self):
        return self.__title
    
    
    def get_date(self):
        return self.__date
    
    
    def get_link(self):
        return self.__link
    
    
    def get_party(self):
        return self.__party
    
    
    def get_proposition_nbr(self):
        return self.__proposition_nbr
    
    
    def get_update_date(self):
        return self.__updateDate
    
    
    def get_statement(self):
        return self.__statement
    
    
    def get_subject(self):
        return self.__subject
    
    
    def get_result(self):
        return self.__result
    
    
    def set_title(self, value):
        self.__title = value
    
    
    def set_date(self, value):
        self.__date = value
    
    
    def set_link(self, value):
        self.__link = value
    
    
    def set_party(self, value):
        self.__party = value
    
    
    def set_proposition_nbr(self, value):
        self.__proposition_nbr = value
    
    
    def set_update_date(self, value):
        self.__updateDate = value
    
    
    def set_statement(self, value):
        self.__statement = value
    
    
    def set_subject(self, value):
        self.__subject = value
    
    
    def set_result(self, value):
        self.__result = value
    
    
    title = property(get_title, set_title, None, "The title of the document.")
    date = property(get_date, set_date, None, "The date that document records.")
    link = property(get_link, set_link, None, "Link to the document.")
    party = property(get_party, set_party, None, "The party that initiated the proposition")
    proposition_nbr = property(get_proposition_nbr, set_proposition_nbr, None, "Number of the proposition")
    updateDate = property(get_update_date, set_update_date, None, "The date the proposition was updated")
    statement = property(get_statement, set_statement, None, "The statement of the document")
    subject = property(get_subject, set_subject, None, "The subject of the document")
    result = property(get_result, set_result, None, "The result of the document")
    obnumber = property(get_obnumber, set_obnumber, del_obnumber, "obnumber's docstring")
#end class Proposition