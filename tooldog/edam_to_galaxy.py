#!/usr/bin/env python3

## Author(s): Kenzo-Hugo Hillion
## Contact(s): kehillio@pasteur.fr
## Python version: 3.6.0
## Creation : 12-20-2016

"""
Gather different information from a Galaxy server (by default https://usegalaxy.org)
and EDAM ontology (by default from http://edamontology.org/EDAM.owl)
"""

###########  Import  ###########

# General libraries
import os
import json
import logging

# External libraries
import requests
import rdflib

###########  Constant(s)  ###########

LOCAL_DATA = os.path.dirname(__file__) + "/data"

###########  Logger  ###########

LOGGER = logging.getLogger(__name__)

###########  Class(es)  ###########

class GalaxyInfo(object):
    """
    Class to gather different information about a Galaxy instance.

    By default, if the galaxy_url is None, information is loaded from local files
    located in the `data/` folder corresponding to https://usegalaxy.org.
    """

    def __init__(self, galaxy_url):
        """
        :param galaxy_url: URL of the Galaxy instance.
        :type galaxy_url: STRING

        :class:`tooldog.edam_to_galaxy.GalaxyInfo` object is initialized with several
        information from the given Galaxy instance. It contains:

        :param self.version: version of the Galaxy instance.
        :type self.version: STRING
        :param self.edam_formats: mapping edam_format to LIST of extension of datatypes.
        :type self.edam_formats: DICT
        :param self.edam_data: mapping edam_data to LIST of extension of datatypes.
        :type self.edam_data: DICT
        :param self.hierarchy: class_to_classes part of the /api/mapping.json which maps
        the parental classes of each classes.
        :type self.hierarchy: DICT
        :param self.class_names: ext_to_class_name part of the /api/mapping.json which
        maps the extension of a datatype to its class in Galaxy.
        :type self.class_names: DICT
        """
        if galaxy_url is None:
            self.galaxy_url = "https://usegalaxy.org"
            LOGGER.info("Loading Galaxy info (https://usegalaxy.org) from " + LOCAL_DATA)
            with open(LOCAL_DATA + "/edam_formats.json") as json_file:
                api_edam_formats = json.load(json_file)
            with open(LOCAL_DATA + "/edam_data.json") as json_file:
                api_edam_data = json.load(json_file)
            with open(LOCAL_DATA + "/mapping.json") as json_file:
                mapping = json.load(json_file)
            with open(LOCAL_DATA + "/version.json") as json_file:
                version = json.load(json_file)
        else:
            self.galaxy_url = galaxy_url
            LOGGER.info("Loading galaxy info from " + galaxy_url +"/api")
            api_edam_formats = requests.get(galaxy_url + "/api/datatypes/edam_formats").json()
            api_edam_data = requests.get(galaxy_url + "/api/datatypes/edam_data").json()
            mapping = requests.get(galaxy_url + "/api/datatypes/mapping").json()
            version = requests.get(galaxy_url + "/api/version").json()
        # Get version of Galaxy instance
        self.version = version['version_major']
        # Reverse EDAMs dictionnaries
        def rev_dict(dictionnary):
            """
            Reverse dictionnary key -> value to value -> LIST of key
            """
            new_dict = {}
            for key, value in dictionnary.items():
                if not value in new_dict:
                    new_dict[value] = []
                new_dict[value].append(key)
            return new_dict
        self.edam_formats = rev_dict(api_edam_formats)
        self.edam_data = rev_dict(api_edam_data)
        # Store hierarchy from mapping and class names
        self.hierarchy = mapping["class_to_classes"]
        self.class_names = mapping["ext_to_class_name"]

    def select_root(self, datatypes):
        """
        Select the root datatype from all given datatypes.

        :param datatypes: list of different datatypes.
        :type datatypes: list of STRING
        :return: root datatype.
        :rtype: STRING
        """
        # Build class to ext dictionnary
        class_to_ext = {}
        for key, value in self.class_names.items():
            if value not in class_to_ext:
                class_to_ext[value] = []
            class_to_ext[value].append(key)
        # Create subdict of hierarchy
        sub_dict = {}
        for datatype in datatypes:
            if datatype in self.class_names:
                sub_dict[self.class_names[datatype]] = \
                  self.hierarchy[self.class_names[datatype]]
            else:
                LOGGER.warning(datatype + " was not found in the ext to class mapping. skipped")
        # Remove class that inherit from both Binary and Text
        datatype_to_remove = []
        for key, value in sub_dict.items():
            binary = 'galaxy.datatypes.binary.Binary' in value
            text = 'galaxy.datatypes.data.Text' in value
            if binary and text:
                datatype_to_remove.append(key)
        for key in datatype_to_remove:
            del sub_dict[key]
        LOGGER.debug(sub_dict)
        # Find root
        selected_class = None
        root_dist = 100 # Set up huge root distance for comparison
        for key, value in sub_dict.items():
            for key, value in sub_dict.items():
                if len(value) < root_dist:
                    root_dist = len(value)
                    selected_class = key
        if selected_class is None:
            LOGGER.warning("No best datatype found, return first datatype of the list")
            return datatypes[0]
        return class_to_ext[selected_class][0]


class EdamInfo(object):
    """
    Contains the given EDAM ontology.

    It is also possible to generate several dictionnaries to help interrogating the ontology
    for a faster access.
    """

    def __init__(self, edam_url):
        """
        :param edam_url: path to EDAM.owl file
        :type edam_url: STRING

        All the EDAM ontology will be contained in a dictionnary (self.edam_ontology).
        """
        if edam_url is None:
            LOGGER.info("Loading EDAM info from http://edamontology.org/EDAM.owl")
            self.edam_ontology = rdflib.Graph()
            self.edam_ontology.parse("http://edamontology.org/EDAM.owl")
            # Get version of EDAM ontology
            version_query = """SELECT ?version WHERE {
                                     <http://edamontology.org> doap:Version ?version}"""
            for row in self.edam_ontology.query(version_query):
                self.version = row[0]
                break
        else:
            pass

    def generate_hierarchy(self):
        """
        Generates two dictionnaries of the EDAM hierarchy (format and data) with the following
        structure:

        DICT[edam_uri] -> LIST of edam_uri from parents

        The dictionnary can be accessed via self.edam_format_hierarchy
        """

        def make_hierarchy(query):
            """
            Build hierarchy for a given query.

            :return: generated hierarchy
            :rtype: DICT
            """
            hierarchy = {}
            for row in self.edam_ontology.query(query):
                uri = row[0].split('/')[-1]
                p_uri = row[1].split('/')[-1]
                if uri not in hierarchy:
                    hierarchy[uri] = []
                hierarchy[uri].append(p_uri)
            return hierarchy

        formats_query = """SELECT ?format ?superformat WHERE {
                                    ?format rdfs:subClassOf ?superformat .
                                    ?superformat oboInOwl:inSubset 
                                   <http://purl.obolibrary.org/obo/edam#formats>
                                    }"""
        data_query = """SELECT ?data ?superdata WHERE {
                                 ?data rdfs:subClassOf ?superdata .
                                 ?superdata oboInOwl:inSubset 
                                <http://purl.obolibrary.org/obo/edam#data>
                                 }"""
        self.edam_format_hierarchy = make_hierarchy(formats_query)
        self.edam_data_hierarchy = make_hierarchy(data_query)
        # TO BE DELETED, JUST TO BYPASS EDAM ISSUE
        del self.edam_data_hierarchy['operation_3458']

class EdamToGalaxy(object):
    """
    Class to make the link between EDAM ontology terms (edam_format and edam_data) and Galaxy
    datatypes.
    """

    def __init__(self, galaxy_url=None, edam_url=None, mapping_json=None):
        """
        :param galaxy_url: URL of the galaxy instance.
        :type galaxy_url: STRING
        :param edam_url: path to EDAM.owl file (URL or local path).
        :type edam_url: STRING
        :param mapping_json: path to personnalized EDAM mapping to Galaxy.
        :type mapping_json: STRING
        """
        if mapping_json is None:
            if galaxy_url or edam_url:
                mapping_json = 'edam_to_galaxy.json'
            else:
                mapping_json = LOCAL_DATA + "/edam_to_galaxy.json"
        # Generates or Loads ?
        if os.path.isfile(mapping_json):
            self.load_local_mapping(mapping_json)
        else:
            # No local file exists, needs to generate it (takes a little bit of time)
            self.edam = EdamInfo(edam_url)
            self.edam_version = self.edam.version
            self.edam.generate_hierarchy()
            self.galaxy = GalaxyInfo(galaxy_url)
            self.galaxy_url = self.galaxy.galaxy_url
            self.galaxy_version = self.galaxy.version
            self.generate_mapping()
            self.export_info(mapping_json)

    def generate_mapping(self):
        """
        Generates mapping between edam_format and edam_data to Galaxy datatypes
        based on the information of the Galaxy instance and the EDAM ontology.

        Every edam_format and edam_data will be given a datatype.
        """
        LOGGER.info("Generating new EDAM mapping to Galaxy datatypes file...")

        def find_datatype(edam, edam_hierarchy, galaxy_mapping):
            """
            Find the best datatype for a given EDAM term.
            :param edam: EDAM term.
            :type edam: STRING
            :param edam_hierarchy: edam_hierarchy from :class:`tooldog.edam_to_galaxy.EdamInfo`
            :type edam_hierarchy: DICT
            :param galaxy_mapping: mapping from :class:`tooldog.edam_to_galaxy.GalaxyInfo`
            :type galaxy_mapping: DICT

            The function then create two dictionnaries: self.format_to_datatype and
            self.data_to_datatype that represents a unique datatype for each EDAM term.
            """
            if not edam in galaxy_mapping:
                LOGGER.debug("No datatype found for " + edam + ". Looking at parental terms.")
                if len(edam_hierarchy[edam]) > 1:
                    LOGGER.debug(edam + " inherits from more than one EDAM. " +\
                                 "Only first EDAM parent of the list is treated: " + \
                                 edam_hierarchy[edam][0])
                elif len(edam_hierarchy[edam]) == 0:
                    LOGGER.debug("No parental EDAM found. " + edam + " is skipped.")
                    return "NO mapping"
                datatype = find_datatype(edam_hierarchy[edam][0], edam_hierarchy, \
                                         galaxy_mapping)
            elif len(galaxy_mapping[edam]) == 1:
                LOGGER.debug("Exactly one datatype found for " + edam + ": " + \
                             galaxy_mapping[edam][0])
                datatype = galaxy_mapping[edam][0]
            elif len(galaxy_mapping[edam]) > 1:
                LOGGER.debug("More than one datatypes found for " + edam)
                datatype = self.galaxy.select_root(galaxy_mapping[edam])
            return datatype

        def maps_datatype(edam_hierarchy, galaxy_mapping):
            """
            Maps all edam terms to a Galaxy datatype.
            :param edam_hierarchy: edam_hierarchy from :class:`tooldog.edam_to_galaxy.EdamInfo`
            :type edam_hierarchy: DICT
            :param galaxy_mapping: mapping from :class:`tooldog.edam_to_galaxy.GalaxyInfo`
            :type galaxy_mapping: DICT
            :return: mapping EDAM term to Galaxy datatype (unique mapping).
            :rtype: DICT
            """
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
        """
        Method to load (from JSON file) mapping previously generated and exported in the
        `local_file`.

        :param local_file: path to the mapping local file.
        :type local_file: STRING
        """
        LOGGER.info("Loading EDAM mapping to Galaxy datatypes from " +\
                    local_file)
        with open(local_file, 'r') as file_path:
            json_file = json.load(file_path)
        self.format_to_datatype = json_file['format']
        self.data_to_datatype = json_file['data']
        self.galaxy_url = json_file['galaxy_url']
        self.galaxy_version = json_file['galaxy_version']
        self.edam_version = json_file['edam_version']

    def export_info(self, export_file):
        """
        Method to export mapping of this object to a JSON file.

        :param export_file: path to the file.
        :type export_file: STRING
        """
        LOGGER.info("Exporting new EDAM mapping to Galaxy datatypes file to ./" +\
                    export_file)
        with open(export_file, 'w') as file_path:
            json.dump({'format':self.format_to_datatype,
                       'data': self.data_to_datatype,
                       'edam_version': self.edam_version,
                       'galaxy_url': self.galaxy_url,
                       'galaxy_version': self.galaxy_version}, file_path)

    def get_datatype(self, edam_data=None, edam_format=None):
        """
        Get datatype from EDAM terms.
        :param edam_data: EDAM data term.
        :type edam_data: STRING
        :param edam_format: EDAM format term.
        :type edam_format: STRING
        :return: datatype corresponding to given EDAM ontologies.
        :rtype: STRING
        """
        if not edam_format is None:
            return self.format_to_datatype[edam_format]
        elif not edam_data is None:
            return self.data_to_datatype[edam_data]
        else:
            return "no EDAM given"
