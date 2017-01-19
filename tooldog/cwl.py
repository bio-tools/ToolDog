#!/usr/bin/env python3

## Author(s): Kenzo-Hugo Hillion
## Contact(s): kehillio@pasteur.fr
## Python version: 3.6.0
## Creation : 03-01-2017

'''
Generation of CWL from Biotool based on model.py
'''

###########  Import  ###########

# General libraries
import os
import copy

# External libraries
import pycwl

# Class and Objects

###########  Constant(s)  ###########

###########  Class(es)  ###########

class GenerateCwl(object):
    '''
    Class to support generation of CWL from Biotool class of model.py
    '''

    def __init__(self, biotool):
        '''
        biotool: [Biotool] object from model.py

        Initialize a [CommandLineTool] object from pycwl with the minimal informations
        from a [Biotool] object.
        '''
        # Initialize counters for inputs and outputs
        self.input_ct = 0
        self.output_ct = 0
        # Initialize tool
        #   Get the first sentence of the description only
        description = biotool.description.split('.')[0] + '.'
        documentation = (biotool.description + "\n\nTool Homepage: " + \
                         biotool.homepage)
        self.tool = pycwl.CommandLineTool(tool_id=biotool.tool_id, label=description, \
                                          base_command="COMMAND", \
                                          doc=documentation)

    def add_input_file(self, input_obj):
        '''
        input: [Input] object from model.py
        Add the input to the tool. We consider inputs present in biotool represent
        input files.
        '''
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
        param_binding = pycwl.CommandLineBinding(prefix='--' + name)
        param = pycwl.CommandInputParameter(name, param_type='File', \
                                            label=input_obj.data_type.term,\
                                            param_format=formats, \
                                            input_binding=param_binding)
        # Appends parameter to inputs
        self.tool.inputs.append(param)

    def add_output_file(self, output):
        '''
        output: [Output] object from model.py
        Add the output to the tool.
        '''
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
        param_binding = pycwl.CommandOutputBinding(glob=name + '.ext')
        param = pycwl.CommandOutputParameter(name, param_type='File', \
                                             label=output.data_type.term, \
                                             param_format=formats, \
                                             output_binding=param_binding)
        self.tool.outputs.append(param)

    def write_cwl(self, out_file=None, index=None):
        '''
        Write CWL to STDOUT or file(s)
        '''
        # Give CWL on STDout
        if out_file is None:
            if index is not None:
                print('########## CWL number ' + str(index) + ' ##########')
            print(self.tool.export())
        else:
            # Format name for output file(s)
            if index is not None:
                out_file = os.path.splitext(out_file)[0] + str(index) + '.cwl'
            else:
                out_file = os.path.splitext(out_file)[0] + '.cwl'
            self.tool.export(out_file)
