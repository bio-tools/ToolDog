#!/usr/bin/env python3

"""
Functions to perform analysis of source code.
"""

#  Import  ------------------------------

# General libraries
import logging

from .tool_analyzer import ToolAnalyzer

#  Constant(s)  ------------------------------

LOGGER = logging.getLogger(__name__)

#  Function(s)  ------------------------------


def analyse(biotool, args):
    """
    Run analysis of the source code from bio.tools or given locally.

    :param biotool: Biotool object.
    :type biotool: :class:`tooldog.model.Biotool`
    :param args: Parsed arguments.
    """
    LOGGER.warn("Analysis feature is not available yet for this version.")
    # Instantiate ToolAnalyzer object
    if args.GALAXY:
        ta = ToolAnalyzer(biotool, 'galaxy')
    else:
        ta = ToolAnalyzer(biotool, 'cwl')
    # Run analysis
    return ta.run_analysis()
