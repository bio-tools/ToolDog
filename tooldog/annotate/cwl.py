#!/usr/bin/env python3

"""
Generation of CWL tool from https://bio.tools based on the ToolDog model using
cwlgen library.
"""

#  Import  ------------------------------

# General libraries
import os
import logging

# External libraries
import cwlgen
from cwlgen.import_cwl import CWLToolParser

# Class and Objects

#  Constant(s)  ------------------------------

LOGGER = logging.getLogger(__name__)

#  Class(es)  ------------------------------


class CwlToolGen(object):
    """
    Class to support generation of CWL from :class:`tooldog.biotool_model.Biotool` object.
    """

    def __init__(self, biotool, existing_tool=None):
        """
        Initialize a [CommandLineTool] object from cwlgen.

        :param biotool: Biotool object of an entry from https://bio.tools.
        :type biotool: :class:`tooldog.biotool_model.Biotool`
        """
        if existing_tool:
            LOGGER.info("Loading existing CWL tool from " + existing_tool)
            ctp = CWLToolParser()
            self.tool = ctp.import_cwl(existing_tool)
            if 'None' in self.tool.doc:
                self.tool.doc = biotool.generate_cwl_doc()
        else:
            LOGGER.info("Creating new CwlToolGen object...")
            # Initialize counters for inputs and outputs
            self.input_ct = 0
            self.output_ct = 0
            # Initialize tool
            #   Get the first sentence of the description only
            description = biotool.description.split('.')[0] + '.'
            documentation = biotool.generate_cwl_doc()
            self.tool = cwlgen.CommandLineTool(tool_id=biotool.tool_id,
                                               label=description,
                                               base_command="COMMAND",
                                               doc=documentation,
                                               cwl_version='v1.0')
        self._set_meta_from_biotool(biotool)

    def add_input_file(self, input_obj):
        """
        Add an input to the CWL tool.

        :param input_obj: Input object.
        :type input_obj: :class:`tooldog.biotool_model.Input`
        """
        LOGGER.info("Adding input to CwlToolGen object...")
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
        param = cwlgen.CommandInputParameter(name, param_type='File',
                                             label=input_obj.data_type.term,
                                             param_format=formats,
                                             input_binding=param_binding)
        # Appends parameter to inputs
        self.tool.inputs.append(param)

    def add_output_file(self, output):
        """
        Add an output to the CWL tool.

        :param output: Output object.
        :type output: :class:`tooldog.biotool_model.Output`
        """
        LOGGER.info("Adding output to CwlToolGen object...")
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
        param = cwlgen.CommandOutputParameter(name, param_type='File',
                                              label=output.data_type.term,
                                              param_format=formats,
                                              output_binding=param_binding)
        self.tool.outputs.append(param)

    def _set_meta_from_biotool(self, biotool):
        """
        Add first set of metadata found on bio.tools to the description.

        :param biotool: Biotool object of an entry from https://bio.tools.
        :type biotool: :class:`tooldog.biotool_model.Biotool`
        """
        self.tool.metadata = cwlgen.Metadata()
        self.tool.metadata.name = biotool.name
        self.tool.metadata.about = biotool.description
        self.tool.metadata.url = biotool.homepage
        if biotool.informations.language:
            self.tool.metadata.programmingLanguage = biotool.informations.language

    def add_publication(self, publication):
        """
        Add publication to the tool (CWL: s:publication).

        :param publication: Publication object.
        :type publication: :class:`tooldog.biotool_model.Publication`
        """
        LOGGER.debug("Adding publication to CwlToolGen object...")
        if not hasattr(self.tool.metadata, 'publication'):
            self.tool.metadata.publication = []
        # Add citation depending the type (doi, pmid...)
        if publication.doi is not None:
            self.tool.metadata.publication.append({'id': 'http://dx.doi.org/' + publication.doi})
        # <citation> only supports doi and bibtex as a type
        elif publication.pmid is not None:
            LOGGER.warn('pmid is not supported by publication, publication skipped')
        elif publication.pmcid is not None:
            LOGGER.warn('pmcid is not supported by publication, publication skipped')

    '''
    Commented for the moment since we did not figure out the best way to integrate
    EDAM operations and topics within CWL tools. It will be added in the Documentation
    for the moment...

    def add_edam_topic(self, topic):
        """
        Add the EDAM topic to the tool (CWL: s:topic).

        :param topic: Topic object.
        :type topic: :class:`tooldog.biotool_model.Topic`
        """
        LOGGER.debug("Adding EDAM topic to CwlToolGen object...")
        LOGGER.warning("Current way of writing EDAM topic in CWL is not correct.")
        if not hasattr(self.tool.metadata, 'edam_topic'):
            self.tool.metadata.edam_topic = []
        self.tool.metadata.edam_topic.append({'url': topic.uri})

    def add_edam_operation(self, operation):
        """
        Add the EDAM operation to the tool (CWL: s:operation).

        :param operation: Operation object.
        :type operation: :class:`tooldog.biotool_model.Operation`
        """
        LOGGER.debug("Adding EDAM operation to CwlToolGen object...")
        LOGGER.warning("Current way of writing EDAM operation in CWL is not correct.")
        if not hasattr(self.tool.metadata, 'edam_operation'):
            self.tool.metadata.edam_operation = []
        self.tool.metadata.edam_operation.append({'url': operation.uri})
    '''

    def write_cwl(self, out_file=None, index=None):
        """
        Write CWL to STDOUT or out_file(s).

        :param out_file: path to output file.
        :type out_file: STRING
        :param index: Index in case more than one function is described.
        :type index: INT
        """
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
