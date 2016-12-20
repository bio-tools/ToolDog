#!/usr/bin/env python3

## Author(s): Kenzo-Hugo Hillion
## Contact(s): kehillio@pasteur.fr
## Python version: 3.5.2+
## Creation : 12-13-2016

'''
Descrition
'''

###########  Import  ###########

# General libraries
import os
import argparse
import sys
import json

# External libraries
import requests

# Class and Objects

###########  Constant(s)  ###########

###########  Class(es)  ###########

class Biotool:

    def __init__(self, name, tool_id, version, description, homepage):
         '''
         name: [STRING]
         tool_id: [STRING]
         version: [STRING]
         description: [STRING]
         homepage: URL to homepage [STRING]
         '''
         self.name = name
         self.tool_id = tool_id
         self.version = version
         self.description = description
         self.homepage = homepage
         self.functions = [] # List of Function objects
         self.topics = []    # List of Topic objects
         self.informations = None # Informations object

    def set_informations(self, credits, contacts, publications, docs): 
        '''
        Add an information object to the biotool

        credits: [LIST] of [DICT] with different credits
        contacts: [LIST] of [DICT] of contacts
        publications: [LIST] of [DICT] of different IDs for publications 
        doc: [LIST] of [DICT] with different documentations
        '''
        self.informations = Informations()
        for c in credits:
            self.informations.credits.append(Credit(c))
        for c in contacts:
            self.informations.contacts.append(Contact(c))
        for p in publications:
            self.informations.publications.append(Publication(p))
        for d in docs:
            self.informations.documentations.append(Documentation(d))

    def add_functions(self, functions):
        '''
        Add functions to the list

        function: [LIST] of [DICT]
        '''
        for f in functions:
            # Create Function object
            function = Function(f['operation'])
            function.add_inputs(f['input'])
            function.add_outputs(f['output'])
            # Append object to the biotool
            self.functions.append(function)

    def add_topics(self, topics):
        '''
        Add topics to the list
        '''
        for t in topics:
            self.topics.append(Topic(t))


class Informations:

    def __init__(self):
        self.publications = [] # List of Publication objects
        self.documentations = [] # List of Documentation objects
        self.contacts = [] # List of Contact objects
        self.credits = [] # List of Credit objects


class Credit:

    def __init__(self, credit):
        self.comment = credit['comment'] # [STRING]
        self.email = credit['email'] # [STRING]
        self.grid_id = credit['gridId'] # [STRING]
        self.name = credit['name'] # [STRING]
        self.type_entity = credit['typeEntity'] # [STRING]
        self.type_role = credit['typeRole'] # [STRING]
        self.url = credit['url'] # [STRING]
        self.orcid_id = credit['orcidId'] # [STRING]


class Publication:

    def __init__(self, publication):
        self.doi = publication['doi'] # [STRING]
        self.pmid = publication['pmid'] # [STRING]
        self.pmcid = publication['pmcid'] # [STRING]
        self.type = publication['type'] # [STRING]


class Documentation:

    def __init__(self, documentation):
        self.url = documentation['url'] # [STRING]
        self.type = documentation['type'] # [STRING]
        self.comment = documentation['comment'] # [STRING]


class Contact:

    def __init__(self,contact):
        self.email = contact['email'] # [STRING]
        self.name = contact['name'] # [STRING]
        # self.role = contact['contactRole']
        # self.tel = contact['contactTel']
        # self.url = contact['contactURL']


class Function:

    def __init__(self,edams):
        '''
        edams: [LIST] of [DICT] of EDAM ontology for operation(s) with uri and term
        '''
        self.operations = [] # List of Operation objects
        for e in edams:
            self.operations.append(Operation(e))
        self.inputs = [] # List of Inputs objects
        self.outputs = [] # List of Outputs objects

    def add_inputs(self, inputs):
        '''
        inputs: [LIST] of [DICT] inputs
        '''
        for i in inputs:
            # Create Input object and appends to the list
            self.inputs.append(Input(i['data'],i['format']))

    def add_outputs(self, outputs):
        '''
        outputs: [LIST] of [DICT] outputs
        '''
        for o in outputs:
            # Create Output object and appends to the list
            self.outputs.append(Output(o['data'],o['format']))


class Data:

    def __init__(self, data_type, formats, description=None):
        '''
        data_type: [DICT] of EDAM ontology for data types with uri and term
        formats: [LIST] of [DICT] of EDAM ontology for data formats with uri and term
        description: [STRING]
        '''
        self.data_type = Data_type(data_type) # Data_type object
        self.formats = [] # List of Format objects
        for f in formats:
            self.formats.append(Format(f))
        self.description = description

class Input(Data):

    def __init__(self, data_type, formats, description=None):
        '''
        data_type: [DICT] of EDAM ontology for data types with uri and term
        formats: [LIST] of [DICT] of EDAM ontology for data formats with uri and term
        description: [STRING]
        '''
        Data.__init__(self, data_type, formats, description)


class Output(Data):

    def __init__(self, data_type, formats, description=None):
        '''
        data_type: [DICT] of EDAM ontology for data types with uri and term
        formats: [LIST] of [DICT] of EDAM ontology for data formats with uri and term
        description: [STRING]
        '''
        Data.__init__(self, data_type, formats, description)


class Edam:

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

    def __init__(self, edam):
        '''
        edam: [DICT] of EDAM ontology for operations with uri and term
        '''
        Edam.__init__(self, edam)

class Data_type(Edam):

    def __init__(self, edam):
        '''
        edam: [DICT] of EDAM ontology for data type with uri and term
        '''
        Edam.__init__(self, edam)

class Format(Edam):

    def __init__(self, edam):
        '''
        edam: [DICT] of EDAM ontology for formats with uri and term
        '''
        Edam.__init__(self, edam)

class Topic(Edam):

    def __init__(self, edam):
        '''
        edam: [DICT] of EDAM ontology for topics with uri and term
        '''
        Edam.__init__(self, edam)
