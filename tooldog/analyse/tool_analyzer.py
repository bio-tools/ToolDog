#!/usr/bin/env python3

import logging

from .code_collector import CodeCollector
from .language_analyzer import PythonAnalyzer

LOGGER = logging.getLogger(__name__)

class ToolAnalyzer(object):
    """
    Class to perform appropriate source code analysis of a tool.
    """

    def __init__(self, biotool, gen_format, language=None, source_code=None):
        """
        :param biotool: Biotool object
        :type biotool: :class:`tooldog.biotool_model.Biotool`
        :param gen_format: tool descriptor language (Galaxy XML or CWL)
        :type gen_format: STRING
        :param language: language of the tool
        :type language: STRING
        :param source_code: path to source code
        :type source_code: STRING
        """
        self.biotool = biotool
        self.gen_format = gen_format
        self.language = language
        self.source_code = source_code

    def _analyse_python(self):
        """
        Perform analysis of Python.
        """
        pa = PythonAnalyzer(self.gen_format)
        return pa.analyse()

    def _analyse_no_language(self):
        """
        Warning message to mention that no language was specified in bio.tools.

        In the future, we can imagine that a code analysis will be perform to check what is
        the coding language.
        """
        LOGGER.warn("Language was not specified for this tool on https://bio.tools. " +
                    "This feature is not processed for the moment.")

    def _analyse_multi_languages(self):
        """
        Warning message to mention that more than one language was given in bio.tools.

        In the future, need to find which language is the main language of the tool (at least
        the one used to run the tool).
        """
        LOGGER.warn("This tool is decribed as using more than one language. " +
                    "This feature is not processed for the moment.")

    def set_language(self):
        """
        Set the language attribute of the object based on the https://bio.tools description.
        """
        language = self.biotool.informations.language
        if len(language) > 1:
            self.language = "multi_languages"
        elif len(language) == 1:
            self.language = language[0]
        else:
            self.language = "no_language"

    def get_source(self):
        """
        Get source code to give to analyzer.
        """
        # At the end of this method, self.source_code should point to directory
        self.source_code = None

    def run_analysis(self):
        """
        Method to run analysis of source code of the entry.
        """
        if self.source_code is None:
            self.get_source()
        if self.language is None:
            self.set_language()
        language = self.language.lower().translate(str.maketrans(' ','_'))
        try:
            getattr(self, '_analyse_{}'.format(language))()
        except AttributeError:
            LOGGER.warn(language + " language is not processed yet by ToolDog.")
        # Need to return the generated code here
        return None
