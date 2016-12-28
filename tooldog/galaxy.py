#!/usr/bin/env python3

## Author(s): Kenzo-Hugo Hillion
## Contact(s): kehillio@pasteur.fr
## Python version: 3.5.2+
## Creation : 12-20-2016

'''
Descrition
'''

###########  Import  ###########

# General libraries
import os
import argparse
import sys
import json
import copy

# External libraries
import requests
import galaxyxml.tool as gxt
import galaxyxml.tool.parameters as gxtp

# Class and Objects
from tooldog import model

###########  Constant(s)  ###########

###########  Class(es)  ###########

class GenerateXml:

    def __init__(self, biotool):
        '''
        biotool: [Biotool] object from model.py

        Initialize a [Tool] object from galaxyxml with the minimal informations
        from a [Biotool] object.
        '''
        # Initialize counters for inputs and outputs
        self.input_ct = 0
        self.output_ct = 0
        # Initialize tool
        #   Get the first sentence of the description only
        description = biotool.description.split('.')[0] + '.' 
        self.tool = gxt.Tool(biotool.name,biotool.tool_id,biotool.version, \
                             description, "COMMAND", version_command = \
                             "COMMAND --version")
        self.tool.help = (biotool.description + "\n\nTool Homepage: " + \
                          biotool.homepage)

    def add_edam_topic(self, topic):
        '''
        topic: [Topic] object from model.py
        Add the EDAM topic to the tool
        '''
        if not hasattr(self.tool, 'edam_topics'):
            # First time we add topics to the tool
            self.tool.edam_topics = gxtp.EdamTopics()
        self.tool.edam_topics.append(gxtp.EdamTopic(topic.get_edam_id()))

    def add_edam_operation(self, operation):
        '''
        topic: [Operation] object from model.py
        Add the EDAM operation to the tool
        '''
        if not hasattr(self.tool, 'edam_operations'):
            # First time we add operations to the tool
            self.tool.edam_operations = gxtp.EdamOperations()
        self.tool.edam_operations.append(gxtp.EdamOperation(operation.get_edam_id()))

    def add_input_file(self, input):
        '''
        input: [Input] object from model.py
        Add the input to the tool. We consider inputs present in biotool represent
        input files.
        '''
        if not hasattr(self.tool, 'inputs'):
            self.tool.inputs = gxtp.Inputs()
        # Build parameter
        self.input_ct += 1
        # Give unique name to the input
        name = 'INPUT' + str(self.input_ct)
        # Get all different format for this input
        list_formats = []
        for f in input.formats:
            list_formats.append(f.term)
        formats = ', '.join(list_formats)
        # Create the parameter
        param = gxtp.DataParam(name, label=input.data_type.term, \
                               help=input.description, format=formats)
        # Override the corresponding arguments in the command line
        param.command_line_override = '--' + name + ' $' + name
        # Appends parameter to inputs
        self.tool.inputs.append(param)

    def add_output_file(self, output):
        '''
        output: [Output] object from model.py
        Add the output to the tool.
        '''
        if not hasattr(self.tool, 'outputs'):
            self.tool.outputs = gxtp.Outputs()
        # Build parameter
        self.output_ct += 1
        # Give unique name to the output
        name = 'OUTPUT' + str(self.output_ct)
        # Get all different format for this output
        list_formats = []
        for f in output.formats:
            list_formats.append(f.term)
        formats = ', '.join(list_formats)
        # Create the parameter
        param = gxtp.OutputParameter(name, format=formats, from_work_dir=\
                                     name + '.ext')
        param.command_line_override = ''
        self.tool.outputs.append(param)

    def add_citation(self, publication):
        '''
        publication: [Publication] object from model.py
        Add publication to <citations>
        '''
        if not hasattr(self.tool, 'citations'):
            self.tool.citations = gxtp.Citations()
        # Add citation depending the type (doi, pmid...)
        if publication.doi is not None:
            self.tool.citations.append(gxtp.Citation('doi',publication.doi))
        elif publication.pmid is not None:
            self.tool.citations.append(gxtp.Citation('pmid',publication.pmid))
        elif publication.pmcid is not None:
            self.tool.citations.append(gxtp.Citation('pmcid',publication.pmcid))

    def write_xml(self,out_file=None):
        '''
        '''
        # Copy informations to avoid expension of xml in case we write several XMLs
        export_tool = copy.deepcopy(self.tool)
        # Give XML on STDout
        if out_file is None:
            print(export_tool.export().decode('utf-8'))
        else:
            f = open(out_file,'w')
            f.write(export_tool.export().decode('utf-8'))
            f.close()
