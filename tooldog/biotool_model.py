#!/usr/bin/env python3

'''
Model used to process information contained in JSON from https://bio.tools description.

The content of a description on https://bio.tools is contained in a JSON file and this
model aims to store the different information.
'''

#  Class(es)  ------------------------------


class Biotool(object):
    '''
    This class correspond to an entry from https://bio.tools.
    '''

    def __init__(self, name, tool_id, version, description, homepage):
        '''
        :param name: Name of the tool.
        :type name: STRING
        :param tool_id: ID of the tool entry.
        :type tool_id: STRING
        :param version: Version of the tool entry.
        :type version: STRING
        :param description: Description of the tool entry.
        :type description: STRING
        :param homepage: URL to homepage.
        :type homepage: STRING

        :class:`tooldog.model.Biotool` object is also initialized with two empty
        list of objects:

        * functions: list of :class:`tooldog.model.Function`
        * topics: list of :class:`tooldog.model.Topic`

        More information (:class:`tooldog.model.Informations` object) can be specified
        using :meth:`tooldog.model.Biotool.set_informations`.
        '''
        self.name = name
        self.tool_id = tool_id
        self.version = version
        self.description = description
        self.homepage = homepage
        self.functions = []  # List of Function objects
        self.topics = []    # List of Topic objects
        self.informations = None  # Informations object

    def generate_galaxy_help(self):
        """
        Generate a help message from the different informations found on the tool.

        :return: a help message
        :rtype: STRING
        """
        help_message = "\n\nWhat it is ?\n" + "============\n\n"
        help_message += self.description + "\n\n"
        help_message += "External links:\n" + "===============\n\n"
        help_message += "- Tool homepage_\n"
        help_message += "- bio.tools_ entry\n\n"
        help_message += ".. _homepage: " + self.homepage + "\n"
        help_message += ".. _bio.tools: https://bio.tools/tool/" + self.tool_id
        return help_message
        

    def set_informations(self, tool_credits, contacts, publications, docs,
                         language, links, download):
        '''
        Add an :class:`tooldog.model.Informations` object to the Biotool.

        :param tool_credits: list of different tool_credits.
        :type tool_credits: LIST of DICT
        :param contacts: list of different contacts.
        :type contacts: LIST of DICT
        :param publications: list of different IDs for publications.
        :type publications: LIST of DICT
        :param doc: list of different documentations.
        :type doc: LIST of DICT
        '''
        self.informations = Informations()
        for cred in tool_credits:
            self.informations.tool_credits.append(Credit(cred))
        for cont in contacts:
            self.informations.contacts.append(Contact(cont))
        for pub in publications:
            self.informations.publications.append(Publication(pub))
        for doc in docs:
            self.informations.documentations.append(Documentation(doc))
        self.informations.language = language
        for link in links:
            self.informations.links.append(Link(link))
        for link in download:
            self.informations.links.append(Link(link))

    def add_functions(self, functions):
        '''
        Add :class:`tooldog.model.Function` objects to the list of functions of the
        Biotool object.

        :param functions: list of functions description from https://bio.tools.
        :type functions: LIST of DICT
        '''
        for fct in functions:
            # Create Function object
            function = Function(fct['operation'])
            function.add_inputs(fct['input'])
            function.add_outputs(fct['output'])
            # Append object to the biotool
            self.functions.append(function)

    def add_topics(self, topics):
        '''
        Add :class:`tooldog.model.Topic` objects to the list of topics of the
        Biotool object.

        :param topics: list of topics description from https://bio.tools.
        :type topics: LIST of DICT
        '''
        for topic in topics:
            self.topics.append(Topic(topic))


class Informations(object):
    '''
    Class to describe different information concerning a bio.tool entry.
    '''

    def __init__(self):
        '''
        :class:`tooldog.model.Informations` object is initialized with four empty
        list of objects:

        * publications: list of :class:`tooldog.model.Publication`
        * documentations: list of :class:`tooldog.model.Documentation`
        * contacts: list of :class:`tooldog.model.Contact`
        * tool_credits: list of :class:`tooldog.model.Credit`
        * language: list of coding language
        * link: list of :class:`tooldog.model.Link`
        '''
        self.publications = []
        self.documentations = []
        self.contacts = []
        self.tool_credits = []
        self.language = []
        self.links = []


class Link(object):
    '''
    Class to store download and links content.
    '''

    def __init__(self, link):
        '''
        :param link: links or download content of the JSON from http://bio.tools.
        :type link: DICT
        '''
        self.url = link['url']
        self.type = link['type']
        self.comment = link['comment']


class Credit(object):
    '''
    Class to store a credit information.
    '''

    def __init__(self, credit):
        '''
        :param credit: credit part of the JSON from http://bio.tools.
        :type credit: DICT
        '''
        self.comment = credit['comment']  # [STRING]
        self.email = credit['email']  # [STRING]
        self.grid_id = credit['gridId']  # [STRING]
        self.name = credit['name']  # [STRING]
        self.type_entity = credit['typeEntity']  # [STRING]
        self.type_role = credit['typeRole']  # [STRING]
        self.url = credit['url']  # [STRING]
        self.orcid_id = credit['orcidId']  # [STRING]


class Publication(object):
    '''
    Class to store one publication information.
    '''

    def __init__(self, publication):
        '''
        :param publication: publication part of the JSON from http://bio.tools.
        :type publication: DICT
        '''
        self.doi = publication['doi']  # [STRING]
        self.pmid = publication['pmid']  # [STRING]
        self.pmcid = publication['pmcid']  # [STRING]
        self.type = publication['type']  # [STRING]


class Documentation(object):
    '''
    Class to store one documentation information.
    '''

    def __init__(self, documentation):
        '''
        :param documentation: documentation part of the JSON from http://bio.tools.
        :type documentation: DICT
        '''
        self.url = documentation['url']  # [STRING]
        self.type = documentation['type']  # [STRING]
        self.comment = documentation['comment']  # [STRING]


class Contact(object):
    '''
    Class to store one contact information.
    '''

    def __init__(self, contact):
        '''
        :param contact: contact part of the JSON from http://bio.tools.
        :type contact: DICT
        '''
        self.email = contact['email']  # [STRING]
        self.name = contact['name']  # [STRING]
        # self.role = contact['contactRole']
        # self.tel = contact['contactTel']
        # self.url = contact['contactURL']


class Function(object):
    '''
    Correspond to one function of the entry with the corresponding inputs and outputs.
    '''

    def __init__(self, edams):
        '''
        :param edams: EDAM ontology for operation(s) with uri and term.
        :type edams: LIST of DICT
        :class:`tooldog.model.Function` object is initialized with two empty
        list of objects:

        * inputs: list of :class:`tooldog.model.Input`
        * outputs: list of :class:`tooldog.model.Output`
        '''
        self.operations = []
        for edam in edams:
            self.operations.append(Operation(edam))
        self.inputs = []
        self.outputs = []

    def add_inputs(self, inputs):
        '''
        Add inputs to the :class:`tooldog.model.Function` object.

        :param inputs: inputs part of one function from http://bio.tools.
        :type inputs: LIST of DICT
        '''
        for inp in inputs:
            # Create Input object and appends to the list
            self.inputs.append(Input(inp['data'], inp['format']))

    def add_outputs(self, outputs):
        '''
        Add outputs to the :class:`tooldog.model.Function` object.

        :param outputs: inputs part of one function from http://bio.tools.
        :type outputs: LIST of DICT
        '''
        for outp in outputs:
            # Create Output object and appends to the list
            self.outputs.append(Output(outp['data'], outp['format']))


class Data(object):
    '''
    Data described by EDAM ontology.
    '''

    def __init__(self, data_type, formats, description=None):
        '''
        :param data_type: EDAM ontology for the data type with uri and term.
        :type data_type: DICT
        :param formats: EDAM ontology for data formats with uri and term.
        :type formats: LIST of DICT
        :param description: description of the data (DEPRECATED)
        :type description: STRING
        '''
        self.data_type = DataType(data_type)
        self.formats = []
        for frmt in formats:
            self.formats.append(Format(frmt))
        self.description = description


class Input(Data):
    '''
    Input of a described function.
    '''

    def __init__(self, data_type, formats, description=None):
        '''
        :param data_type: EDAM ontology for the data type with uri and term.
        :type data_type: DICT
        :param formats: EDAM ontology for data formats with uri and term.
        :type formats: LIST of DICT
        :param description: description of the data (DEPRECATED)
        :type description: STRING
        '''
        Data.__init__(self, data_type, formats, description)


class Output(Data):
    '''
    Output of a described function.
    '''

    def __init__(self, data_type, formats, description=None):
        '''
        :param data_type: EDAM ontology for the data type with uri and term.
        :type data_type: DICT
        :param formats: EDAM ontology for data formats with uri and term.
        :type formats: LIST of DICT
        :param description: description of the data (DEPRECATED)
        :type description: STRING
        '''
        Data.__init__(self, data_type, formats, description)


class Edam(object):
    '''
    Edam annotation with the uri and its corresponding term.
    '''

    def __init__(self, edam):
        '''
        :param edam: EDAM ontology with uri and term.
        :type edam: DICT
        '''
        self.uri = edam['uri']
        self.term = edam['term']

    def get_edam_id(self):
        '''
        Get the EDAM id from the uri.

        :return: EDAM id from the uri.
        :rtype: STRING
        '''
        return self.uri.split('/')[-1]


class Operation(Edam):
    '''
    EDAM operation associated to a function.
    '''

    def __init__(self, edam):
        '''
        :param edam: EDAM ontology with uri and term.
        :type edam: DICT
        '''
        Edam.__init__(self, edam)


class DataType(Edam):
    '''
    EDAM data associated to either input or output.
    '''

    def __init__(self, edam):
        '''
        :param edam: EDAM ontology with uri and term.
        :type edam: DICT
        '''
        Edam.__init__(self, edam)


class Format(Edam):
    '''
    EDAM format associated to either input or output.
    '''

    def __init__(self, edam):
        '''
        :param edam: EDAM ontology with uri and term.
        :type edam: DICT
        '''
        Edam.__init__(self, edam)


class Topic(Edam):
    '''
    EDAM topic associated to the entry.
    '''

    def __init__(self, edam):
        '''
        :param edam: EDAM ontology with uri and term.
        :type edam: DICT
        '''
        Edam.__init__(self, edam)
