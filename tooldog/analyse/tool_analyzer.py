#!/usr/bin/env python3

class ToolAnalyzer(object):
    '''
    Class to perform appropriate source code analysis of a tool
    '''

    def __init__(self, biotool, gen_format, language=None, source_code=None):
        '''
        :param biotool: Biotool object
        :type biotool: :class:`tooldog.biotool_model.Biotool`
        :param gen_format: tool descriptor language (Galaxy XML or CWL)
        :type gen_format: STRING
        :param language: language of the tool
        :type language: STRING
        :param source_code: path to source code
        :type source_code: STRING
        '''
        self.biotool = biotool
        self.gen_format = gen_format
        self.language = language
        self.source_code = source_code
