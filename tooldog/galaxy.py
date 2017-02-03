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


class GenerateXml(object):
    '''
    Class to support generation of XML from :class:`tooldog.model.Biotool` object.
    '''

    def __init__(self, biotool, galaxy_url=None):
        '''
        Initialize a [Tool] object from galaxyxml with the minimal information
        (a name, an id, a version, a description, the command, the command version
        and a help).

        :param biotool: Biotool object of an entry from https://bio.tools.
        :type biotool: :class:`tooldog.model.Biotool`
        '''
        # Initialize GalaxyInfo
        self.galaxy_info = GalaxyInfo(galaxy_url=galaxy_url)
        self.galaxy_info.load_info()
        # Initialize counters for inputs and outputs
        self.input_ct = 0
        self.output_ct = 0
        # Initialize tool
        #   Get the first sentence of the description only
        description = biotool.description.split('.')[0] + '.'
        self.tool = gxt.Tool(biotool.name, biotool.tool_id, biotool.version, \
                             description, "COMMAND", version_command=\
                             "COMMAND --version")
        self.tool.help = (biotool.description + "\n\nTool Homepage: " + \
                          biotool.homepage)

    def add_edam_topic(self, topic):
        '''
        Add the EDAM topic to the tool (XML: edam_topics).

        :param topic: Topic object.
        :type topic: :class:`tooldog.model.Topic`
        '''
        if not hasattr(self.tool, 'edam_topics'):
            # First time we add topics to the tool
            self.tool.edam_topics = gxtp.EdamTopics()
        self.tool.edam_topics.append(gxtp.EdamTopic(topic.get_edam_id()))

    def add_edam_operation(self, operation):
        '''
        Add the EDAM operation to the tool (XML: edam_operations).

        :param topic: Operation object.
        :type topic: :class:`tooldog.model.Operation`
        '''
        if not hasattr(self.tool, 'edam_operations'):
            # First time we add operations to the tool
            self.tool.edam_operations = gxtp.EdamOperations()
        self.tool.edam_operations.append(gxtp.EdamOperation(operation.get_edam_id()))

    def add_input_file(self, input_obj):
        '''
        Add an input to the tool (XML: <inputs>).

        :param input_obj: Input object.
        :type input_obj: :class:`tooldog.model.Input`
        '''
        if not hasattr(self.tool, 'inputs'):
            self.tool.inputs = gxtp.Inputs()
        # Build parameter
        self.input_ct += 1
        # Give unique name to the input
        name = 'INPUT' + str(self.input_ct)
        # Get all different format for this input
        list_formats = []
        for format_obj in input_obj.formats:
            list_formats.append(self.galaxy_info.get_datatype(format_obj.uri,\
                                                              input_obj.data_type.uri))
        formats = ', '.join(list_formats)
        # Create the parameter
        param = gxtp.DataParam(name, label=input_obj.data_type.term, \
                               help=input_obj.description, format=formats)
        # Override the corresponding arguments in the command line
        param.command_line_override = '--' + name + ' $' + name
        # Appends parameter to inputs
        self.tool.inputs.append(param)

    def add_output_file(self, output):
        '''
        Add an output to the tool (XML: <outputs>).
 
        :param output: Output object.
        :type output: :class:`tooldog.model.Output`
        '''
        if not hasattr(self.tool, 'outputs'):
            self.tool.outputs = gxtp.Outputs()
        # Build parameter
        self.output_ct += 1
        # Give unique name to the output
        name = 'OUTPUT' + str(self.output_ct)
        # Get all different format for this output
        list_formats = []
        for format_obj in output.formats:
            list_formats.append(self.galaxy_info.get_datatype(format_obj.uri))
        formats = ', '.join(list_formats)
        # Create the parameter
        param = gxtp.OutputParameter(name, format=formats, from_work_dir=\
                                     name + '.ext')
        param.command_line_override = ''
        self.tool.outputs.append(param)

    def add_citation(self, publication):
        '''
        Add publication(s) to the tool (XML: <citations>).

        :param publication: Publication object.
        :type publication: :class:`tooldog.model.Publication`
        '''
        if not hasattr(self.tool, 'citations'):
            self.tool.citations = gxtp.Citations()
        # Add citation depending the type (doi, pmid...)
        if publication.doi is not None:
            self.tool.citations.append(gxtp.Citation('doi', publication.doi))
        elif publication.pmid is not None:
            self.tool.citations.append(gxtp.Citation('pmid', publication.pmid))
        elif publication.pmcid is not None:
            self.tool.citations.append(gxtp.Citation('pmcid', publication.pmcid))

    def write_xml(self, out_file=None, index=None):
        '''
        Write CWL to STDOUT or out_file(s).

        :param out_file: path to output file.
        :type out_file: STRING
        :param index: Index in case more than one function is described.
        :type index: INT
        '''
        # Copy informations to avoid expension of xml in case we write several XMLs
        export_tool = copy.deepcopy(self.tool)
        # Give XML on STDout
        if out_file is None:
            if index is not None:
                print('########## XML number ' + str(index) + ' ##########')
            print(export_tool.export().decode('utf-8'))
        else:
            # Format name for output file(s)
            if index is not None:
                out_file = os.path.splitext(out_file)[0] + str(index) + '.xml'
            else:
                out_file = os.path.splitext(out_file)[0] + '.xml'
            file_w = open(out_file, 'w')
            file_w.write(export_tool.export().decode('utf-8'))
            file_w.close()
