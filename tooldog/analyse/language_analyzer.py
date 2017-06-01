#!/usr/bin/env python3

import logging

LOGGER = logging.getLogger(__name__)

class LanguageAnalyzer(object):
    """
    This should be the abstract class for all analyzer
    I have to check the way to properly do that you might be able to help for that :).
    """

    def __init__(self):
        """
        :param biotool: Biotool object
        :type biotool: :class:`tooldog.biotool_model.Biotool`
        """
        self.biotool = biotool

    def analyse(self):
        """
        Run source code analysis
        """
        pass


class PythonAnalyzer(LanguageAnalyzer):
    """
    Object to specifically analyze Python source code.
    """

    def __init__(self, gen_format):
        """
        :param gen_format: tool description language (Galaxy XML or CWL)
        :type gen_format: STRING
        """
        self.gen_format = gen_format  # To be used as an option when running Docker

    def analyse(self):
        """
        Run source code analysis
        """
        LOGGER.info("Running analysis of Python source code...")
        return None
