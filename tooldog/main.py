#!/usr/bin/env python3

"""
Main functions used by ToolDog.
"""

#  Import  ------------------------------

# General libraries
import argparse
import os
import sys
import json
import copy
import logging

# External libraries
import requests

# Class and Objects
from tooldog import __version__, Biotool
from tooldog.annotate.galaxy import GalaxyToolGen
from tooldog.annotate.cwl import CwlToolGen
from tooldog.analyse import analyse

# Constant(s)  ------------------------------

LOG_FILE = os.path.dirname(__file__) + '/tooldog.log'
global LOGGER
LOGGER = logging.getLogger(__name__)  # for tests

#  Function(s)  ------------------------------


def parse_arguments():
    """
    Define parser for ToolDog.
    """
    parser = argparse.ArgumentParser(description='Generates XML or CWL from bio.tools entry.')
    # Common arguments for analysis and annotations
    parser.add_argument('biotool_entry', help='bio.tools entry from online resource' +
                        ' (ID/VERSION, e.g. SignalP/4.1) or from local file (ENTRY.json,' +
                        ' e.g. signalp4.1.json)')
    ana_or_desc = parser.add_mutually_exclusive_group(required=False)
    ana_or_desc.add_argument('--analyse', dest='ANALYSE', action='store_true',
                             help='run only analysis step of ToolDog.')
    parser.add_argument('--annotate', dest='ANNOTATE', action='store_true',
                        help='run only annotation step of ToolDog.')
    ana_or_desc.add_argument('--existing_desc', dest='ORI_DESC', default=None,
                             help='Existing Tool descriptor that you want to annotate.')
    parser.add_argument('-f', '--file', dest='OUTFILE', help='write in the OUTFILE instead ' +
                        'of STDOUT.')
    parser.add_argument('-v', '--verbose', action='store_true', dest='VERBOSE',
                        help='display info on STDERR.')
    parser.add_argument('--version', action='version', version=__version__,
                        help='show the version number and exit.')
    # Group for the choice of tool descriptor
    choice_desc = parser.add_argument_group('Choice of tool descriptor')
    exc_group = choice_desc.add_mutually_exclusive_group(required=True)
    exc_group.add_argument('-g', '--galaxy', action='store_true',
                           help='generates XML for Galaxy.', dest='GALAXY')
    exc_group.add_argument('-c', '--cwl', action='store_true', help='generates CWL tool ' +
                           'descriptor.', dest='CWL')
    # Group for Galaxy options
    galaxy_opt = parser.add_argument_group('Options for Galaxy XML generation (-g/--galaxy)')
    galaxy_opt.add_argument('--galaxy_url', dest='GAL_URL', default=None,
                            help='url of the Galaxy instance (default: https://usegalaxy.org' +
                            ' ).')
    galaxy_opt.add_argument('--edam_url', dest='EDAM_URL', default=None,
                            help='EDAM.owl file either online url or local path ' +
                            '(default: http://edamontology.org/EDAM.owl).')
    galaxy_opt.add_argument('--mapping_file', dest='MAP_FILE', default=None,
                            help='Personalized EDAM to datatypes mapping json file ' +
                            'generated previously by ToolDog.')
    # Group for logger options
    log_group = parser.add_argument_group('Logs options')
    log_group.add_argument('-l', '--logs', action='store_true',
                           help='Write logs in tooldog_activity.log.',
                           dest='LOGS')
    log_group.add_argument('--log_level', dest='LOG_LEVEL', default='WARN',
                           help='set up the level of the logger.')
    log_group.add_argument('--log_file', dest='LOG_FILE', default='tooldog_activity.log',
                           help='define an output LOG_FILE.')

    try:
        return parser.parse_args()
    except SystemExit:
        sys.exit(1)


def config_logger(write_logs, log_level, log_file, verbose):
    """
    Initialize the logger for ToolDog. By default, only WARNING, ERROR and CRITICAL are
    written on STDERR. You can also write logs to a log file.

    :param write_logs: Decide to write logs to output log file.
    :type write_logs: BOOLEAN
    :param log_level: Select the level of logs. 'debug', 'info' or 'warn'. Other value
    is considered as 'warn'.
    :type log_level: STRING
    :param log_file: path to output log file.
    :type log_file: STRING

    :return: Config dictionnary for logger.
    :rtype: DICT
    """
    cfg = {'version': 1,
           'formatters': {'written': {'format': '%(asctime)s :: %(name)s ' +
                                                ':: %(levelname)s :: %(message)s'},
                          'printed': {'format': '%(name)s :: ' +
                                      '%(levelname)s :: %(message)s'}},
           'handlers': {},
           'loggers': {}}
    # Configure handler for all logs if user specified so
    if write_logs:
        cfg_logfile = {'class': 'logging.handlers.RotatingFileHandler',
                       'formatter': 'written',
                       'maxBytes': 1000000,
                       'backupCount': 1}
        cfg_logfile['level'] = log_level
        cfg_logfile['filename'] = log_file
        cfg['handlers']['logfile'] = cfg_logfile
    # Configure handler for Errors, warnings on stderr
    cfg_stderr = {'class': 'logging.StreamHandler',
                  'formatter': 'printed'}
    cfg_stderr['level'] = 'WARNING'
    if verbose:
        cfg_stderr['level'] = 'INFO'
    cfg['handlers']['stderr'] = cfg_stderr
    # Configure loggers for everymodule
    modules = ['annotate.galaxy', 'annotate.cwl', 'annotate.edam_to_galaxy',
               'analyse', 'analyse.tool_analazer', 'analyse.code_collector',
               'analyse.language_analyzer', 'main', 'analyse']
    logger = {'handlers': ['stderr'],
              'propagate': False,
              'level': 'DEBUG'}
    if write_logs:
        logger['handlers'].append('logfile')
    for module in modules:
        cfg['loggers']['tooldog.' + module] = logger
    return cfg


def json_from_biotools(tool_id, tool_version):
    """
    Import JSON of a tool from https://bio.tools.

    :param tool_id: ID of the tool.
    :type tool_id: STRING
    :param tool_version: Version of the tool.
    :type tool_version: STRING

    :return: dictionnary corresponding to the JSON from https://bio.tools.
    :rtype: DICT
    """
    LOGGER.info("Loading tool entry from https://bio.tools: " + tool_id + '/' + tool_version)
    biotools_link = "https://bio.tools/api/tool/" + tool_id + "/version/" + tool_version
    # Access the entry with requests and get the JSON part
    http_tool = requests.get(biotools_link)
    json_tool = http_tool.json()
    if len(json_tool.keys()) == 1:
        # The content of JSON only contains one element which is the results we obtain
        # on bio.tools when an entry does not exist.
        LOGGER.error('Entry not found on https://bio.tools.com. Exit.')
        sys.exit(1)
    return json_tool


def json_from_file(json_file):
    """
    Import JSON of a tool from a local JSON file.

    :param json_file: path to the file
    :type json_file: STRING

    :return: dictionnary corresponding to the JSON.
    :rtype: DICT
    """
    LOGGER.info("Loading tool entry from local file: " + json_file)
    # parse file in JSON format
    with open(json_file, 'r') as tool_file:
        json_tool = json.load(tool_file)
    return json_tool


def json_to_biotool(json_file):
    """
    Takes JSON file from bio.tools description and loads its content to
    :class:`tooldog.model.Biotool` object.

    :param json: dictionnary of JSON file from bio.tools description.
    :type param_json: DICT

    :return: Biotool object.
    :rtype: :class:`tooldog.biotool_model.Biotool`
    """
    LOGGER.info("Converting biotool entry (JSON) to Biotool object...")
    # Initialize Biotool object with basic parameters
    biotool = Biotool(json_file['name'], json_file['id'], json_file['version'],
                      json_file['description'], json_file['homepage'])
    # Add informations
    biotool.set_informations(json_file['credit'], json_file['contact'],
                             json_file['publication'], json_file['documentation'],
                             json_file['language'], json_file['link'], json_file['download'])
    # Add Function(s)
    biotool.add_functions(json_file['function'])
    # Add Topics(s)
    biotool.add_topics(json_file['topic'])
    return biotool


def write_xml(biotool, outfile=None, galaxy_url=None, edam_url=None, mapping_json=None,
              existing_tool=None):
    """
    This function uses :class:`tooldog.galaxy.GalaxyToolGen` to write XML using galaxyxml.

    :param biotool: Biotool object.
    :type biotool: :class:`tooldog.biotool_model.Biotool`
    :param outfile: path to output file to write the XML.
    :type outfile: STRING
    """
    LOGGER.info("Writing XML file with galaxy.py module...")
    biotool_xml = GalaxyToolGen(biotool, galaxy_url=galaxy_url, edam_url=edam_url,
                                mapping_json=mapping_json, existing_tool=existing_tool)
    # Add EDAM annotation and citations
    if not getattr(biotool_xml, 'edam_topics', None):
        for topic in biotool.topics:
            biotool_xml.add_edam_topic(topic)
    if not getattr(biotool_xml, 'edam_operations', None):
        for function in biotool.functions:
            for operation in function.operations:
                biotool_xml.add_edam_operation(operation)
    if not getattr(biotool_xml, 'citations', None):
        for publi in biotool.informations.publications:
            biotool_xml.add_citation(publi)
    # Add inputs and outputs
    if existing_tool:
        biotool_xml.write_xml(out_file=outfile, keep_old_command=True)
    else:
        # This will need to be changed when incorporating argparse2tool...
        for function in biotool.functions:
            # First make a copy of the tool to add function infos
            function_xml = copy.deepcopy(biotool_xml)
            for inpt in function.inputs:
                function_xml.add_input_file(inpt)
            for output in function.outputs:
                function_xml.add_output_file(output)
            # Write tool
            if len(biotool.functions) > 1:
                function_xml.write_xml(outfile, biotool.functions.index(function) + 1)
            else:
                function_xml.write_xml(outfile)


def write_cwl(biotool, outfile=None, existing_tool=None):
    """
    This function uses :class:`tooldog.cwl.CwlToolGen` to write CWL using cwlgen.
    CWL is generated on STDOUT by default.

    :param biotool: Biotool object.
    :type biotool: :class:`tooldog.model.Biotool`
    :param outfile: path to output file to write the CWL.
    :type outfile: STRING
    """
    LOGGER.info("Writing CWL file with cwl.py module...")
    biotool_cwl = CwlToolGen(biotool, existing_tool=existing_tool)
    # Add operations and inputs
    if existing_tool:
        # For the moment, there is no way to add metadata to the cwl
        biotool_cwl.write_cwl(outfile)
    else:
        for function in biotool.functions:
            # First make a copy of the tool to add function infos
            function_cwl = copy.deepcopy(biotool_cwl)
            for inp in function.inputs:
                function_cwl.add_input_file(inp)
            for outp in function.outputs:
                function_cwl.add_output_file(outp)
            # Write tool
            if len(biotool.functions) > 1:
                function_cwl.write_cwl(outfile, biotool.functions.index(function) + 1)
            else:
                function_cwl.write_cwl(outfile)


def annotate(biotool, args, existing_desc=None):
    """
    Run annotation (generated by analysis or existing_desc).

    :param biotool: Biotool object.
    :type biotool: :class:`tooldog.model.Biotool`
    :param args: Parsed arguments.
    :param existing_desc: Existing tool descriptor path.
    :type existing_desc: STRING
    """
    if args.GALAXY:
        # Probably need to check if existing_desc right format
        write_xml(biotool, outfile=args.OUTFILE, galaxy_url=args.GAL_URL,
                  edam_url=args.EDAM_URL, mapping_json=args.MAP_FILE,
                  existing_tool=existing_desc)
    elif args.CWL:
        # Write corresponding CWL
        write_cwl(biotool, args.OUTFILE, existing_tool=existing_desc)


def run():
    """
    Running function called by Tooldog.
    """

    # Parse arguments
    args = parse_arguments()

    # Logger configuration
    import logging.config
    logging.config.dictConfig(config_logger(args.LOGS, args.LOG_LEVEL,
                                            args.LOG_FILE, args.VERBOSE))
    # Reset LOGGER with new config
    LOGGER = logging.getLogger(__name__)

    # Get JSON of the tool
    if '.json' in args.biotool_entry:
        # Importation from local file
        json_tool = json_from_file(args.biotool_entry)
    elif ('/' in args.biotool_entry) and (len(args.biotool_entry.split('/')) == 2):
        # Importation from https://bio.tools
        tool_ids = args.biotool_entry.split('/')
        json_tool = json_from_biotools(tool_ids[0], tool_ids[1])
    else:
        # Wrong argument given for the entry
        LOGGER.error('biotool_entry does not have the correct syntax. Exit')
        parser.print_help()
        sys.exit(1)

    # Load Biotool object
    biotool = json_to_biotool(json_tool)

    if args.ORI_DESC:
        annotate(biotool, args, args.ORI_DESC)
    elif args.ANALYSE and not args.ANNOTATE:
        try:
           # TODO create temporary directory to work in
           analyse(biotool, args)
        finally:
           # TODO delete temporary directory
           pass
    elif args.ANNOTATE and not args.ANALYSE:
        annotate(biotool, args)
    else:
        try:
           # TODO create temporary directory to work in
            analyse(biotool, args)
        finally:
           gen_tool = args.ORI_DESC
           # TODO delete temporary directory
           pass
        # The existing_tool need to be changed to what will be generated by analyse().
        annotate(biotool, args, gen_tool)

if __name__ == "__main__":
    run()
