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
import galaxyxml.tool as gxt
import galaxyxml.tool.parameters as gxtp

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
        for c in contacts:
            self.informations.contacts.append(Contact(c))
        for c in credits:
            self.informations.documentations.append(Credit(c))
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

    def generate_xml(self):
        '''
        Generate XML file using galaxyxml (reference) from Biotool object    
    
        biotool: Biotool [OBJECT]
        '''
        # Initialize XML
        tool = gxt.Tool(biotool.name,biotool.tool_id,biotool.version,biotool.description,\
                        "COMMAND", version_command="COMMAND --version")

        # Write the ontology for functions and topics
        edam_topics = gxtp.EdamTopics()
        for t in self.topics:
            edam_topics.append(gxtp.EdamTopic(t.get_edam_id()))
        tool.edam_topics = edam_topics
        edam_operations = gxtp.EdamOperations()
        for f in self.functions:
            for o in f.operations:
                edam_operations.append(gxtp.EdamOperation(o.get_edam_id()))
        tool.edam_operations = edam_operations

        # Write Inputs based on the description        
        tool.inputs = self.functions[0].generate_inputs_xml()

        # Write Help part of the XML
        tool.help = (biotool.description + '\n' + biotool.homepage)

        # Write XML in current directory (id.xml)
        outfile = open(self.tool_id + '.xml','w')
        outfile.write(tool.export().decode('utf-8'))
        outfile.close()


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

    def generate_inputs_xml(self):
        '''
        Build XML from inputs with the Galaxy syntax from Function object
        '''
        inputs = gxtp.Inputs()
        cpt = 1
        for i in self.inputs:
            inputs.append(i.generate_xml(cpt))
            cpt += 1
        return inputs

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

    def generate_xml(self,cpt):
        '''
        Build XML from Input object with the Galaxy syntax.

        cpt: counter to give different ID to inputs (e.g. INPUT1, INPUT2...) [INT]
        '''
        name = 'INPUT' + str(cpt)
        param = gxtp.DataParam(name, label=self.data_type.term, \
                               help=self.description, format=self.formats[0].term)
        param.command_line_override = '--' + name + ' $' + name
        return param


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



###########  Function(s)  ###########

def json_from_biotools(tool_id,tool_version):
    '''
    Import JSON of a tool from https://bio.tools

    tool_id: [STRING]
    tool_version: [STRING]
    '''
    biotools_link = "https://bio.tools/api/tool/" + tool_id + "/version/" + tool_version
    # print ("Loading " + tool_id + ' version ' + tool_version + " from https://bio.tools")
    # Access the entry with requests and get the JSON part
    http_tool = requests.get(biotools_link)
    json_tool = http_tool.json()
    return json_tool

def json_from_file(json_file):
    '''
    Import JSON of a tool from a local file

    json_file: path to the file [STRING]
    '''
    # print ("Loading tool from local JSON file: " + json_file)
    # parse file in JSON format
    with open(json_file,'r') as tool_file:
        json_tool = json.load(tool_file)
    tool_file.close()
    return json_tool


def json_to_biotool(json):
    '''
    Takes JSON file from bio.tools and loads it content to Biotool object

    json: json file from bio.tools [DICT]

    RETURN: Biotool [OBJECT]
    '''
    # Initialize Biotool object with basic parameters
    biotool = Biotool(json['name'],json['id'],json['version'],json['description'],json['homepage'])
    # Add informations
    biotool.set_informations(json['credit'],json['contact'],json['publication'],json['documentation'])
    # Add Function(s)
    biotool.add_functions(json['function'])
    # Add Topics(s)  
    biotool.add_topics(json['topic'])
    return biotool

###########  Main  ###########

if __name__ == "__main__":

    ## Parse arguments
    parser = argparse.ArgumentParser(description = 'Generates XML template for Galaxy ')
    subparsers = parser.add_subparsers(dest='COMMAND', help='COMMAND')
    subparsers.required = True

    # Parser for online tool entry
    parser_onl = subparsers.add_parser('online', help='import tool from https://bio.tools')
    parser_onl.add_argument('-i', '--id', help='ID of the tool entry on https://bio.tools',\
                            dest='ID', required=True)
    parser_onl.add_argument('-v', '--version', help='Version of the tool entry', \
                            dest='VERSION', required=True)

    # Parser for local import
    parser_loc = subparsers.add_parser('local', help='import tool from local JSON file')
    parser_loc.add_argument('-j', '--json_file', help='Path to JSON file (Giving a JSON ' + \
                            'file skips the query from https://bio.tools', dest='JSON_FILE', \
                            required=True)
  
    try:
        args = parser.parse_args()
    except SystemExit:
        if len(sys.argv) == 1:
            parser.print_help()
        elif sys.argv[1] == 'online':
            parser_onl.print_help()
        elif sys.argv[1] == 'local':
            parser_loc.print_help()
        else:
            parser.print_help()
        sys.exit(1)

    ## Extra tests for arguments

    ###########################################################

    ## MAIN

    # Get JSON of the tool
    if args.COMMAND == 'online':
        json_tool = json_from_biotools(args.ID,args.VERSION)
    elif args.COMMAND == 'local':
        json_tool = json_from_file(args.JSON_FILE)

    # Load Biotool object
    biotool = json_to_biotool(json_tool)

    # Write corresponding XML
    biotool.generate_xml()
