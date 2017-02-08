#!/usr/bin/env python3

## Author(s): Kenzo-Hugo Hillion
## Contact(s): kehillio@pasteur.fr
## Python version: 3.6.0
## Creation : 12-20-2016

'''
Generation of XML for Galaxy from https://bio.tools based on the Tooldog model using
galaxyxml library.
'''

###########  Import  ###########

# General libraries
import os
import copy
import json

# External libraries
import galaxyxml.tool as gxt
import galaxyxml.tool.parameters as gxtp
import requests

# Class and Objects

###########  Constant(s)  ###########

LOCAL_DATA = os.path.dirname(__file__) + "/data"

###########  Class(es)  ###########

class GalaxyInfo(object):
    '''
    Class to gather different information about a Galaxy instance.

    By default, if the galaxy_url is None, information is loaded from local files
    located in the `data/` folder.
    '''

    def __init__(self, galaxy_url=None):
        '''
        :param galaxy_url: URL of the galaxy instance.
        :type galaxy_url: STRING

        :class:`tooldog.galaxy.GalaxyInfo` object is initialized with two empty
        dictionnaries:

        * datatypes_from_formats
        * datatypes_from_data

        Dictionnaries are then filled in with :meth:`tooldog.galaxy.GalaxyInfo.load_info`.
        '''
        self.galaxy_url = galaxy_url
        self.datatypes_from_formats = {}
        self.datatypes_from_data = {}

    def load_info(self):
        '''
        Loads information from the galaxy URL (or local file).
        '''
        # Load dictionnaries datatype -> EDAM
        if self.galaxy_url is None:
            with open(LOCAL_DATA + "/edam_formats.json") as json_file:
                edam_formats = json.load(json_file)
            json_file.close()
            with open(LOCAL_DATA + "/edam_data.json") as json_file:
                edam_data = json.load(json_file)
            json_file.close()
        else:
            edam_formats = requests.get(galaxy_url + "/api/datatypes/edam_formats").json()
            edam_data = requests.get(galaxy_url + "/api/datatypes/edam_data").json()
        # Build dictionnaries EDAM -> datatype
        # FOR THE MOMENT, KEEP ONLY ONE DATATYPE PER EDAM, ONLY LAST IS KEPT
        for datatype in edam_formats.keys():
            self.datatypes_from_formats[edam_formats[datatype]] = datatype
        for datatype in edam_data.keys():
            self.datatypes_from_data[edam_data[datatype]] = datatype

    def get_datatype(self, edam_format_uri, edam_data_uri=None):
        '''
        :return: datatype corresponding to both edam_format and edam_data
        :rtype: STRING

        Note: for the moment, return only datatype corresponding to the edam_format
        '''
        edam_format = edam_format_uri.split('/')[-1]
        if edam_format in self.datatypes_from_formats:
            return self.datatypes_from_formats[edam_format]
        return "no_mapping"
