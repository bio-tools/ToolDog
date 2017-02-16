#!/usr/bin/env python3

## Author(s): Kenzo-Hugo Hillion
## Contact(s): kehillio@pasteur.fr
## Python version: 3.6.0
## Creation : 03-01-2017

'''
Generation of CWL tool from https://bio.tools based on the ToolDog model using
cwlgen library.
'''

###########  Import  ###########

# General libraries
import os
import logging

# External libraries
import cwlgen

# Class and Objects

###########  Constant(s)  ###########

###########  Logger  ###########

LOGGER = logging.getLogger(__name__)

###########  Class(es)  ###########

class GenerateCwl(object):
    '''
    Class to support generation of CWL from :class:`tooldog.model.Biotool` object.
    '''

    def __init__(self, biotool):
        '''
        Initialize a [CommandLineTool] object from cwlgen with the minimal information
        (an id, a description, the command and a documentation).

        :param biotool: Biotool object of an entry from https://bio.tools.
        :type biotool: :class:`tooldog.model.Biotool`
        '''
        LOGGER.info("Creating new GenerateCwl object...")
        # Initialize counters for inputs and outputs
        self.input_ct = 0
        self.output_ct = 0
        # Initialize tool
        #   Get the first sentence of the description only
        description = biotool.description.split('.')[0] + '.'
        documentation = (biotool.description + "\n\nTool Homepage: " + \
                         biotool.homepage)
        self.tool = cwlgen.CommandLineTool(tool_id=biotool.tool_id, label=description, \
                                          base_command="COMMAND", \
                                          doc=documentation)

    def add_input_file(self, input_obj):
        '''
        Add an input to the CWL tool.

        :param input_obj: Input object.
        :type input_obj: :class:`tooldog.model.Input`
        '''
        LOGGER.info("Adding input to GenerateCwl object...")
        # Build parameter
        self.input_ct += 1
        # Give unique name to the input
        name = 'INPUT' + str(self.input_ct)
        # Get all different formats for this input
        list_formats = []
        for format_obj in input_obj.formats:
            list_formats.append(format_obj.uri)
        formats = ', '.join(list_formats)
        # Create the parameter
        param_binding = cwlgen.CommandLineBinding(prefix='--' + name)
        param = cwlgen.CommandInputParameter(name, param_type='File', \
                                            label=input_obj.data_type.term,\
                                            param_format=formats, \
                                            input_binding=param_binding)
        # Appends parameter to inputs
        self.tool.inputs.append(param)

    def add_output_file(self, output):
        '''
        Add an output to the CWL tool.

        :param output: Output object.
        :type output: :class:`tooldog.model.Output`
        '''
        LOGGER.info("Adding output to GenerateCwl object...")
        # Build parameter
        self.output_ct += 1
        # Give unique name to the output
        name = 'OUTPUT' + str(self.output_ct)
        # Get all different format for this output
        list_formats = []
        for format_obj in output.formats:
            list_formats.append(format_obj.uri)
        formats = ', '.join(list_formats)
        # Create the parameter
        param_binding = cwlgen.CommandOutputBinding(glob=name + '.ext')
        param = cwlgen.CommandOutputParameter(name, param_type='File', \
                                             label=output.data_type.term, \
                                             param_format=formats, \
                                             output_binding=param_binding)
        self.tool.outputs.append(param)

    def write_cwl(self, out_file=None, index=None):
        '''
        Write CWL to STDOUT or out_file(s).

        :param out_file: path to output file.
        :type out_file: STRING
        :param index: Index in case more than one function is described.
        :type index: INT
        '''
        # Give CWL on STDout
        if out_file is None:
            if index is not None:
                print('########## CWL number ' + str(index) + ' ##########')
            LOGGER.info("Writing CWL file to STDOUT...")
            print(self.tool.export())
        else:
            # Format name for output file(s)
            if index is not None:
                out_file = os.path.splitext(out_file)[0] + str(index) + '.cwl'
            else:
                out_file = os.path.splitext(out_file)[0] + '.cwl'
            LOGGER.info("Writing CWL file to " + out_file)
            self.tool.export(out_file)
