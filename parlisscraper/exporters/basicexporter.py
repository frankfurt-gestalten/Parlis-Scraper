'''
This module contains various classes to export the retrieved data.

@author: Niko Wenselowski
'''


class BaseExporter(object):
    '''
    Abstract base class to export Propositions.
    '''

    def createExport(self, propositions):
        '''
        Exports the given Propositions.

        @param *propositions: The propositions to export.
        @type **propositions: sequence of Proposition.
        '''
        raise NotImplementedError("Can't export.")
