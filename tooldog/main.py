#!/usr/bin/env python3

## Author(s): Kenzo-Hugo Hillion
## Contact(s): kehillio@pasteur.fr
## Python version: 3.5.2+
## Creation : 12-13-2016

'''
Descrition
'''

###########  Import  ###########

# General libraries
import os
import argparse
import sys
import json
import logging
from logging.handlers import RotatingFileHandler

# External libraries
import requests

# Class and Objects
from tooldog import model
from tooldog import galaxy

###########  Logger  ###########

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# Define the format
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
# Logger for all logs
file_handler = RotatingFileHandler('tooldog_activity.log', mode='a', maxBytes=1000000,\
                                   backupCount=1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
# Logger for Errors, warnings on stderr
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

###########  Function(s)  ###########

def json_from_biotools(tool_id,tool_version):
    '''
    Import JSON of a tool from https://bio.tools

    tool_id: [STRING]
    tool_version: [STRING]

    RETURN: [DICT]
    '''
    logger.debug("Loading tool entry from https://bio.tools: " + tool_id + '/' + tool_version)
    biotools_link = "https://bio.tools/api/tool/" + tool_id + "/version/" + tool_version
    # Access the entry with requests and get the JSON part
    http_tool = requests.get(biotools_link)
    json_tool = http_tool.json()
    if (len(json_tool.keys()) == 1):
        # The content of JSON only contains one element which is the results we obtain 
        # on bio.tools when an entry does not exist.
        logger.error('Entry not found on https://bio.tools.com. Exit.')
        sys.exit(1)
    return json_tool

def json_from_file(json_file):
    '''
    Import JSON of a tool from a local file

    json_file: path to the file [STRING]

    RETURN: [DICT]
    '''
    logger.debug("Loading tool entry from local file: " + json_file)
    # parse file in JSON format
    with open(json_file,'r') as tool_file:
        json_tool = json.load(tool_file)
    tool_file.close()
    return json_tool

def json_to_biotool(json):
    '''
    Takes JSON file from bio.tools and loads it content to Biotool object

    json: json file from bio.tools [DICT]

    RETURN: Biotool [OBJECT]
    '''
    # Initialize Biotool object with basic parameters
    biotool = model.Biotool(json['name'],json['id'],json['version'],json['description'],json['homepage'])
    # Add informations
    biotool.set_informations(json['credit'],json['contact'],json['publication'],json['documentation'])
    # Add Function(s)
    biotool.add_functions(json['function'])
    # Add Topics(s)  
    biotool.add_topics(json['topic'])
    return biotool

def write_xml(biotool,outfile=None):
    '''
    This function uses GenerateXml class (galaxy.py) to write XML using galaxyxml

    biotool: [Biotool] object from model.py
    outfile: output file to write the XML [String]
    '''
    logger.debug("Writing XML file...")
    biotool_xml = galaxy.GenerateXml(biotool)
    # Add topics to the XML
    for t in biotool.topics:
        biotool_xml.add_edam_topic(t)
    # Add operations and inputs
    #for f in biotool.functions:  -> deal with all function
    # Deal with 1st function only:
    for f in biotool.functions:
        for o in f.operations:
            biotool_xml.add_edam_operation(o)
        for i in f.inputs:
            biotool_xml.add_input_file(i)
        for o in f.outputs:
            biotool_xml.add_output_file(o)
        break # Only dead with 1st function:
    for p in biotool.informations.publications:
        biotool_xml.add_citation(p)
    biotool_xml.write_xml(outfile)

###########  Main  ###########

def run():

    ## Parse arguments
    parser = argparse.ArgumentParser(description = 'Generates XML or CWL from bio.tools entry.')
    parser.add_argument('biotool_entry', help='either online (ID/VERSION, e.g. SignalP/4.1) '+\
                        'or from local file (ENTRY.json, e.g. signalp4.1.json)')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-g','--galaxy', action='store_true', help='generates XML for Galaxy.',\
                        dest='GALAXY')
    group.add_argument('-c','--cwl', action='store_true', help='generates CWL', dest='CWL')
    parser.add_argument('-f','--file', dest='OUTFILE', help='Write in the OUTFILE instead '+\
                        'of STDOUT.')
  
    try:
        args = parser.parse_args()
    except SystemExit:
        parser.print_help()
        sys.exit(1)

    ###########################################################

    ## MAIN

    # Get JSON of the tool
    if '.json' in args.biotool_entry:
        # Importation from local file
        json_tool = json_from_file(args.biotool_entry)
    elif ('/' in args.biotool_entry) and (len(args.biotool_entry.split('/')) == 2):
        # Importation from https://bio.tools
        tool_ids = args.biotool_entry.split('/')
        json_tool = json_from_biotools(tool_ids[0],tool_ids[1])
    else:
        # Wrong argument given for the entry
        logger.error('biotool_entry does not have the correct syntax. Exit')
        parser.print_help()
        sys.exit(1)

    # Load Biotool object
    biotool = json_to_biotool(json_tool)

    if args.GALAXY:
    # Write corresponding XMLs
        write_xml(biotool,args.OUTFILE)

    if args.CWL:
    # Write corresponding CWL
        logger.warning('Generation of CWL is not available yet. Coming soon...')

if __name__ == "__main__":
    run()
