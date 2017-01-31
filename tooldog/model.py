#!/usr/bin/env python3

## Author(s): Kenzo-Hugo Hillion
## Contact(s): kehillio@pasteur.fr
## Python version: 3.6.0
## Creation : 12-13-2016

'''
Model used to process information contained in JSON from https//bio.tools description.
'''

###########  Class(es)  ###########

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

        Functions (:class:`tooldog.model.Function` objects) 
        and topics (:class:`tooldog.model.Topic` objects)
        are stored in lists which are initialized empty.

        More information (:class:`tooldog.model.Informations` object) can be specified
        using :meth:`tooldog.model.Biotool.set_informations`.
        '''
        self.name = name
        self.tool_id = tool_id
        self.version = version
        self.description = description
        self.homepage = homepage
        self.functions = [] # List of Function objects
        self.topics = []    # List of Topic objects
        self.informations = None # Informations object

    def set_informations(self, tool_credits, contacts, publications, docs):
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
    Class to describe different informations concerning a bio.tool entry
    '''

    def __init__(self):
        self.publications = [] # List of Publication objects
        self.documentations = [] # List of Documentation objects
        self.contacts = [] # List of Contact objects
        self.tool_credits = [] # List of Credit objects


class Credit(object):
    '''
    Class to store a credit information
    '''

    def __init__(self, credit):
        self.comment = credit['comment'] # [STRING]
        self.email = credit['email'] # [STRING]
        self.grid_id = credit['gridId'] # [STRING]
        self.name = credit['name'] # [STRING]
        self.type_entity = credit['typeEntity'] # [STRING]
        self.type_role = credit['typeRole'] # [STRING]
        self.url = credit['url'] # [STRING]
        self.orcid_id = credit['orcidId'] # [STRING]


class Publication(object):
    '''
    Store publication information
    '''

    def __init__(self, publication):
        self.doi = publication['doi'] # [STRING]
        self.pmid = publication['pmid'] # [STRING]
        self.pmcid = publication['pmcid'] # [STRING]
        self.type = publication['type'] # [STRING]


class Documentation(object):
    '''
    Store documentation information
    '''

    def __init__(self, documentation):
        self.url = documentation['url'] # [STRING]
        self.type = documentation['type'] # [STRING]
        self.comment = documentation['comment'] # [STRING]


class Contact(object):
    '''
    Store contact information
    '''

    def __init__(self, contact):
        self.email = contact['email'] # [STRING]
        self.name = contact['name'] # [STRING]
        # self.role = contact['contactRole']
        # self.tel = contact['contactTel']
        # self.url = contact['contactURL']


class Function(object):
    '''
    Correspond to one function of the entry with the corresponding inputs and outputs
    '''

    def __init__(self, edams):
        '''
        edams: [LIST] of [DICT] of EDAM ontology for operation(s) with uri and term
        '''
        self.operations = [] # List of Operation objects
        for edam in edams:
            self.operations.append(Operation(edam))
        self.inputs = [] # List of Inputs objects
        self.outputs = [] # List of Outputs objects

    def add_inputs(self, inputs):
        '''
        inputs: [LIST] of [DICT] inputs
        '''
        for inp in inputs:
            # Create Input object and appends to the list
            self.inputs.append(Input(inp['data'], inp['format']))

    def add_outputs(self, outputs):
        '''
        outputs: [LIST] of [DICT] outputs
        '''
        for outp in outputs:
            # Create Output object and appends to the list
            self.outputs.append(Output(outp['data'], outp['format']))


class Data(object):
    '''
    Data described by EDAM ontology that can be input or output
    '''

    def __init__(self, data_type, formats, description=None):
        '''
        data_type: [DICT] of EDAM ontology for data types with uri and term
        formats: [LIST] of [DICT] of EDAM ontology for data formats with uri and term
        description: [STRING]
        '''
        self.data_type = DataType(data_type) # Data_type object
        self.formats = [] # List of Format objects
        for frmt in formats:
            self.formats.append(Format(frmt))
        self.description = description

class Input(Data):
    '''
    Input of a described function
    '''

    def __init__(self, data_type, formats, description=None):
        '''
        data_type: [DICT] of EDAM ontology for data types with uri and term
        formats: [LIST] of [DICT] of EDAM ontology for data formats with uri and term
        description: [STRING]
        '''
        Data.__init__(self, data_type, formats, description)


class Output(Data):
    '''
    Output of a described function
    '''

    def __init__(self, data_type, formats, description=None):
        '''
        data_type: [DICT] of EDAM ontology for data types with uri and term
        formats: [LIST] of [DICT] of EDAM ontology for data formats with uri and term
        description: [STRING]
        '''
        Data.__init__(self, data_type, formats, description)


class Edam(object):
    '''
    Edam annotation with the uri and its corresponding term
    '''

    def __init__(self, edam):
        '''
        edam: [DICT] of EDAM ontology with uri and term
        '''
        self.uri = edam['uri']
        self.term = edam['term']

    def get_edam_id(self):
        '''
        Get the EDAM id from the url
        '''
        return self.uri.split('/')[-1]

class Operation(Edam):
    '''
    EDAM operation associated to a function
    '''

    def __init__(self, edam):
        '''
        edam: [DICT] of EDAM ontology for operations with uri and term
        '''
        Edam.__init__(self, edam)

class DataType(Edam):
    '''
    EDAM data_type associated to either input or output
    '''

    def __init__(self, edam):
        '''
        edam: [DICT] of EDAM ontology for data type with uri and term
        '''
        Edam.__init__(self, edam)

class Format(Edam):
    '''
    EDAM format associated to either input or output
    '''

    def __init__(self, edam):
        '''
        edam: [DICT] of EDAM ontology for formats with uri and term
        '''
        Edam.__init__(self, edam)

class Topic(Edam):
    '''
    EDAM topic associated to the entry
    '''

    def __init__(self, edam):
        '''
        edam: [DICT] of EDAM ontology for topics with uri and term
        '''
        Edam.__init__(self, edam)
