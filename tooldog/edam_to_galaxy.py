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
import logging

# External libraries
import galaxyxml.tool as gxt
import galaxyxml.tool.parameters as gxtp
import requests

# Class and Objects
from ontospy import Ontospy

###########  Constant(s)  ###########

LOCAL_DATA = os.path.dirname(__file__) + "/data"

###########  Logger  ###########

LOGGER = logging.getLogger(__name__)

###########  Class(es)  ###########

class GalaxyInfo(object):
    '''
    Class to gather different information about a Galaxy instance.

    By default, if the galaxy_url is None, information is loaded from local files
    located in the `data/` folder.
    '''

    def __init__(self, galaxy_url):
        '''
        :param galaxy_url: URL of the galaxy instance.
        :type galaxy_url: STRING

        :class:`tooldog.galaxy.GalaxyInfo` object is initialized with two empty
        dictionnaries:

        * datatypes_from_formats: unique datatype for one given edam_format.
        * datatypes_from_data: unique datatype for one given edam_data.

        Dictionnaries are then filled in with :meth:`tooldog.galaxy.GalaxyInfo.load_info`.
        '''
        self.galaxy_url = galaxy_url
        if self.galaxy_url is None:
            LOGGER.info("Loading galaxy info from " + LOCAL_DATA)
            with open(LOCAL_DATA + "/edam_formats.json") as json_file:
                api_edam_formats = json.load(json_file)
            with open(LOCAL_DATA + "/edam_data.json") as json_file:
                api_edam_data = json.load(json_file)
            with open(LOCAL_DATA + "/mapping.json") as json_file:
                mapping = json.load(json_file)
        else:
            LOGGER.info("Loading galaxy info from " + galaxy_url +"/api/datatypes")
            api_edam_formats = requests.get(galaxy_url + "/api/datatypes/edam_formats").json()
            api_edam_data = requests.get(galaxy_url + "/api/datatypes/edam_data").json()
            mapping = requests.get(galaxy_url + "/api/datatypes/mapping").json()
        # Reverse EDAMs dictionnaries
        def rev_dict(dictionnary):
            new_dict = {}
            for key, value in dictionnary.items():
                if not value in new_dict:
                    new_dict[value] = []
                new_dict[value].append(key)
            return new_dict
        self.edam_formats = rev_dict(api_edam_formats)
        self.edam_data = rev_dict(api_edam_data)
        # Store hierarchy from mapping and class names
        self.hierarchy = mapping["class_to_direct_parents"]
        self.class_names = mapping["ext_to_class_name"]

    def select_best(self, datatypes):
        '''
        Select the last common datatype to all given datatypes.

        :param datatypes: list of different datatypes.
        :type datatypes: list of STRING
        :return: last common datatype.
        :rtype: STRING
        '''
        return "MULTI MAPPING"


class EdamInfo(object):
    '''
    Contains the given EDAM ontology.

    It is also possible to generate several dictionnaries to help interrogating the ontology
    for a faster access.
    '''

    def __init__(self, edam_file):
        '''
        :param edam_file: path to EDAM.owl file
        :type edam_file: STRING
        '''
        if edam_file is None:
            LOGGER.info("Loading EDAM info from " + LOCAL_DATA + "/EDAM_dev.owl")
            self.edam_ontology = Ontospy(uri_or_path=LOCAL_DATA + "/EDAM_dev.owl")
        else:
            pass

    def generate_hierarchy(self):
        '''
        Generates two dictionnaries of the EDAM hierarchy (format and data) with the following
        structure:

        DICT[edam_uri] -> LIST of edam_uri from parents
        '''
        self.edam_format_hierarchy = {}
        self.edam_data_hierarchy = {}
        for edam in self.edam_ontology.classes:
            uri = str(edam.uri).split('/')[-1]
            if 'format_' in uri:
                self.edam_format_hierarchy[uri] = []
                for parent in edam.parents():
                    p_uri = str(parent.uri).split('/')[-1]
                    self.edam_format_hierarchy[uri].append(p_uri)
            elif 'data_' in uri:
                self.edam_data_hierarchy[uri] = []
                for parent in edam.parents():
                    p_uri = str(parent.uri).split('/')[-1]
                    self.edam_data_hierarchy[uri].append(p_uri)
            else:
                pass


class EdamToGalaxy(object):
    '''
    Class to make the link between edam ontologies (edam_format and edam_data) and galaxy
    datatypes. 
    '''

    def __init__(self, galaxy_url=None, edam_file=None, mapping_from_local=None):
        '''
        :param galaxy_url: URL of the galaxy instance.
        :type galaxy_url: STRING
        :param edam_file: path to EDAM.owl file
        :type edam_file: STRING
        :param mapping_from_local: path to personnalized EDAM mapping to Galaxy.
        :type mapping_from_local: STRING
        '''
        if mapping_from_local is None:
            mapping_from_local = LOCAL_DATA + "/edam_to_galaxy.json"
        # Generates or Loads ?
        if os.path.isfile(mapping_from_local):
            self.load_local_mapping(mapping_from_local)
        else:
            # No local file exists, needs to generate it (takes a little bit of time)
            self.edam = EdamInfo(edam_file)
            self.edam.generate_hierarchy()
            self.galaxy = GalaxyInfo(galaxy_url)
            self.generate_mapping()
            self.export_info(mapping_from_local)

    def generate_mapping(self):
        '''
        Generates mapping between edam_format and edam_data to Galaxy datatypes
        based on the information of the Galaxy instance (main by default) and the
        EDAM ontology.

        Every edam_format and edam_data will be given a datatype.
        '''
        LOGGER.info("Generating new EDAM mapping to Galaxy datatypes file...")

        def find_datatype(edam, edam_hierarchy, galaxy_mapping):
            if not edam in galaxy_mapping:
                LOGGER.info("No datatype found for " + edam)
                if len(edam_hierarchy[edam]) > 1:
                    LOGGER.warning(edam + " inherits from more than one EDAM. " +\
                                   "Only first EDAM parent of the list is treated: " + \
                                   edam_hierarchy[edam][0])
                elif len(edam_hierarchy[edam]) == 0:
                    LOGGER.warning("No parental EDAM found. " + edam + " is skipped.")
                    return "NO mapping"
                datatype = find_datatype(edam_hierarchy[edam][0], edam_hierarchy, \
                                         galaxy_mapping)
            elif len(galaxy_mapping[edam]) == 1:
                LOGGER.info("Exactly one datatype found for " + edam)
                datatype = galaxy_mapping[edam][0]
            elif len(galaxy_mapping[edam]) > 1:
                LOGGER.info("More than one datatypes found for " + edam)
                datatype = self.galaxy.select_best(galaxy_mapping[edam])
            return datatype

        def maps_datatype(edam_hierarchy, galaxy_mapping):
            map_to_datatype = {}
            for edam in edam_hierarchy.keys():
                map_to_datatype[edam] = find_datatype(edam, edam_hierarchy, galaxy_mapping)
            return map_to_datatype
            
        # EDAM formats
        self.format_to_datatype = maps_datatype(self.edam.edam_format_hierarchy,\
                                                self.galaxy.edam_formats)
        # EDAM data
        self.data_to_datatype = maps_datatype(self.edam.edam_data_hierarchy,\
                                              self.galaxy.edam_data)

    def load_local_mapping(self, local_file):
        '''
        Method to load (from JSON file) mapping previously generated and exported in the
        `local_file`.

        :param local_file: path to the mapping local file.
        :type local_file: STRING
        '''
        LOGGER.info("Loading EDAM mapping to Galaxy datatypes from " +\
                    local_file)
        with open(local_file, 'r') as fp:
            json_file = json.load(fp)
        self.format_to_datatype = json_file['format']
        self.data_to_datatype = json_file['data']

    def export_info(self, export_file):
        '''
        Method to export mapping of this object to a JSON file.

        :param export_file: path to the file.
        :type export_file: STRING
        '''
        LOGGER.info("Exporting new EDAM mapping to Galaxy datatypes file to " +\
                    export_file)
        with open(export_file, 'w') as fp:
            json.dump({'format':self.format_to_datatype,
                       'data': self.data_to_datatype}, fp)

    def get_datatype(self, edam_data=None, edam_format=None):
        '''
        :return: datatype corresponding to given EDAM ontologies.
        :rtype: STRING
        '''
        if not edam_format is None:
            return self.format_to_datatype[edam_format]
        elif not edam_data is None:
            return self.data_to_datatype[edam_data]
        else:
            return "no EDAM given"
