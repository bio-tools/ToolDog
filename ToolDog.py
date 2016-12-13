#! /usr/bin/env python3

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

# Class and Objects


###########  Constant(s)  ###########

###########  Function(s) and Class(es)  ###########

def json_from_biotools(tool_id,tool_version):
    '''
    Import JSON of a tool from https://bio.tools

    tool_id: [string]
    tool_version: [string]
    '''
    biotools_link = "https://bio.tools/api/tool/" + tool_id + "/version/" + tool_version
    print ("Loading " + tool_id + ' version ' + tool_version + " from https://bio.tools")
    # Access the entry with requests and get the JSON part
    http_tool = requests.get(biotools_link)
    json_tool = http_tool.json()
    return json_tool

def json_from_file(json_file):
    '''
    Import JSON of a tool from a local file

    json_file: path to the file [string]
    '''
    print ("loading tool from local JSON file: " + json_file)
    # parse file in JSON format
    with open(json_file,'r') as tool_file:
        json_tool = json.load(tool_file)
    return json_tool

###########  Main  ###########

if __name__ == "__main__":

    ## Parse arguments
    parser = argparse.ArgumentParser(description = 'Generates XML template for Galaxy ' + \
                                     'from https://bio.tools entry.')
    parser.add_argument('-i', '--id', help='ID of the tool entry on https://bio.tools', dest='ID')
    parser.add_argument('-v', '--version', help='Version of the tool entry', dest='VERSION')
    parser.add_argument('-j', '--json_file', help='Path to JSON file (Giving a JSON file skips '+ \
                        'the query from https://bio.tools', dest='JSON_FILE')
   
    try:
        # No args display help message
        if len(sys.argv) == 1:
           parser.print_help()
           sys.exit(1)
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)
 
    ## Extra tests for arguments
    '''
    Must test here whether the information is given through a JSON file or if a 
    request need to be done from bio.tools.
    '''
    if args.JSON_FILE is None:
        if ((args.ID is None) | (args.VERSION is None)):
            sys.stderr.write("ERROR: You need to specify either the ID (-i/--id) and version " + \
                             "(-v/--version) of an entry from bio.tools OR a JSON file (-j/--json_file). Exit.")
            sys.exit(1)

    ###########################################################

    ## MAIN

    # Get the JSON of the tool
    if args.JSON_FILE is None:
        json_tool = json_from_biotools(args.ID,args.VERSION)
    else:
        json_tool = json_from_file(args.JSON_FILE)

    #print (json_tool['description'])
