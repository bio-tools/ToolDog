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

    :type biotool: :class:`tooldog.biotool_model.Biotool`
    :return: Main language of the tool.
    :rtype: STRING
    """
    language = biotool.informations.language
    if len(language) > 1:
        LOGGER.warn("This tool is described as using more than one language. " +
                    "This feature is not processed for the moment.")
        return None
    elif len(language) == 1:
        return language[0]
    else:
        LOGGER.warn("Language was not specified for this tool on http://bio.tools. " +
                    "This feature is not processed for the moment.")
        return None


def __get_source_code(biotool):
    """
    Find the source code of the bio.tools entry.

    :type biotool: :class:`tooldog.biotool_model.Biotool`
    :return: link to download source code
    :rtype: STRING
    """
    LOGGER.warn("__get_source_code feature is not avaible yet.")
    return None


def __run_analysis(biotool, source_code, args):
    """
    Run analysis of source code and generate tool descriptor in a Docker container.

    :type biotool: :class:`tooldog.biotool_model.Biotool`
    :param source_code: path to source code
    :type source_code: STRING
    :param args: Parsed arguments
    :return: path to generated file
    :rtype: STRING
    """
    # Find source code
    if source_code is None:
        source_code = __get_source_code(biotool)
    if args.GALAXY:
        # Need to run argparse2tool to generate galaxy XML
        # and return path to genetared file
        pass
    elif args.CWL:
        # Need to run argparse2tool to generate CWL
        # and return path to genetared file
        pass
    # Alternative approach is to generate both in the docker container
    # and only use the one we need
    return None


def analyse(biotool, args):
    """
    Run analysis of the source code from bio.tools or given locally.

    :param biotool: Biotool object.
    :type biotool: :class:`tooldog.model.Biotool`
    :param args: Parsed arguments.
    """
    LOGGER.warn("Analysis feature is not available yet for this version.")
    # Instantiate ToolAnalyzer object
    ta = ToolAnalyzer(biotool, )
    # Check language
    if language is None:
        language = __check_language(biotool)
    # Perform analysis
    if language == 'Python':
        return __run_analysis(biotool, source_code, args)
    else:
        LOGGER.warn("Tool is not recognized as being coded in Python. " +
                    "This feature is not processed for the moment.")
        return None
