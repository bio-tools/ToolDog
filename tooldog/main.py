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

# External libraries
import requests
import galaxyxml.tool as gxt
import galaxyxml.tool.parameters as gxtp

# Class and Objects
from tooldog import model
from tooldog import galaxy

###########  Constant(s)  ###########

###########  Class(es)  ###########

###########  Function(s)  ###########

def json_from_biotools(tool_id,tool_version):
    '''
    Import JSON of a tool from https://bio.tools

    tool_id: [STRING]
    tool_version: [STRING]
    '''
    biotools_link = "https://bio.tools/api/tool/" + tool_id + "/version/" + tool_version
    # print ("Loading " + tool_id + ' version ' + tool_version + " from https://bio.tools")
    # Access the entry with requests and get the JSON part
    http_tool = requests.get(biotools_link)
    json_tool = http_tool.json()
    return json_tool

def json_from_file(json_file):
    '''
    Import JSON of a tool from a local file

    json_file: path to the file [STRING]
    '''
    # print ("Loading tool from local JSON file: " + json_file)
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

###########  Main  ###########

def run():

    ## Parse arguments
    parser = argparse.ArgumentParser(description = 'Generates XML template for Galaxy ')
    subparsers = parser.add_subparsers(dest='COMMAND', help='COMMAND')
    subparsers.required = True

    # Parser for online tool entry
    parser_onl = subparsers.add_parser('online', help='import tool from https://bio.tools')
    parser_onl.add_argument('-i', '--id', help='ID of the tool entry on https://bio.tools',\
                            dest='ID', required=True)
    parser_onl.add_argument('-v', '--version', help='Version of the tool entry', \
                            dest='VERSION', required=True)

    # Parser for local import
    parser_loc = subparsers.add_parser('local', help='import tool from local JSON file')
    parser_loc.add_argument('-j', '--json_file', help='Path to JSON file (Giving a JSON ' + \
                            'file skips the query from https://bio.tools', dest='JSON_FILE', \
                            required=True)
  
    try:
        args = parser.parse_args()
    except SystemExit:
        if len(sys.argv) == 1:
            parser.print_help()
        elif sys.argv[1] == 'online':
            parser_onl.print_help()
        elif sys.argv[1] == 'local':
            parser_loc.print_help()
        else:
            parser.print_help()
        sys.exit(1)

    ## Extra tests for arguments

    ###########################################################

    ## MAIN

    # Get JSON of the tool
    if args.COMMAND == 'online':
        json_tool = json_from_biotools(args.ID,args.VERSION)
    elif args.COMMAND == 'local':
        json_tool = json_from_file(args.JSON_FILE)

    # Load Biotool object
    biotool = json_to_biotool(json_tool)

    # Write corresponding XMLs (write function later)
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
        break # Only dead with 1st function:
    biotool_xml.write_xml()

if __name__ == "__main__":
    run()
