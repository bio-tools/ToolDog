#!/usr/bin/env python3

"""
Functions to perform analysis of source code.
"""

#  Import  ------------------------------

# General libraries
import logging

#  Constant(s)  ------------------------------

LOGGER = logging.getLogger(__name__)

#  Function(s)  ------------------------------


def __check_language(biotool):
    """
    Find in what language the tool is developed.

    :return: Main language of the tool.
    :rtype: STRING
    """


def analyse(biotool, args):
    """ 
    Run analysis of the source code from bio.tools or given locally.

    :param biotool: Biotool object.
    :type biotool: :class:`tooldog.model.Biotool`
    :param args: Parsed arguments.
    """
    # Check language, 
    LOGGER.warn("Analysis feature is not available yet for this version.")
