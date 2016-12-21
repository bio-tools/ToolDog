#!/usr/bin/env python3

## Author(s): Kenzo-Hugo Hillion
## Contact(s): kehillio@pasteur.fr
## Python version: 3.5.2+
## Creation : 12-19-2016

'''
Descrition
'''

###########  Import  ###########

# General libraries
import os
import argparse
import sys
import filecmp
import unittest

# External libraries

# Class and Objects
from tooldog import main, model, galaxy

###########  Constant(s)  ###########

# Declare one ontology for all the test
EDAM = {'uri':'http://edamontology.org/topic_0091',
        'term':'bioinformatics'}

###########  Function(s)  ###########

###########  Class(es)  ###########

class TestBiotool(unittest.TestCase):

    def setUp(self):
        self.biotool = model.Biotool('name','an_id','a_version','a description '+\
                                       'with spaces.', 'http://urltohomepage.com')

    def test_init(self):
        self.assertEqual(self.biotool.name, 'name')
        self.assertEqual(self.biotool.tool_id, 'an_id')
        self.assertEqual(self.biotool.version, 'a_version')
        self.assertEqual(self.biotool.description, 'a description with spaces.')
        self.assertEqual(self.biotool.homepage, 'http://urltohomepage.com')
        self.assertListEqual(self.biotool.functions, [])
        self.assertListEqual(self.biotool.topics, [])
        self.assertIsNone(self.biotool.informations)

    def test_set_informations(self):
        credits = [{'comment':'a_comment', 'email':'an_email',\
                    'gridId':'a_grid_id', 'name':'a_name',\
                    'typeEntity':'a_type_entity', 'typeRole':'a_type_role',\
                    'url':'a_url', 'orcidId':'an_orcid_id'}]
        contacts = [{'email':'an_email', 'name':'a_name'}]
        pubs = [{'doi':'a_doi', 'pmid':'a_pm_id', 'pmcid':'a_pmc_id', 'type':'a_type'}]
        docs = [{'url':'an_url', 'type':'a_type', 'comment':'a_comment'}]
        self.biotool.set_informations(credits,contacts,pubs,docs)
        # Check credits params
        self.assertEqual(self.biotool.informations.credits[0].comment, 'a_comment')
        self.assertEqual(self.biotool.informations.credits[0].email, 'an_email')
        self.assertEqual(self.biotool.informations.credits[0].grid_id, 'a_grid_id')
        self.assertEqual(self.biotool.informations.credits[0].name, 'a_name')
        self.assertEqual(self.biotool.informations.credits[0].type_entity, 'a_type_entity')
        self.assertEqual(self.biotool.informations.credits[0].type_role, 'a_type_role')
        self.assertEqual(self.biotool.informations.credits[0].url, 'a_url')
        self.assertEqual(self.biotool.informations.credits[0].orcid_id, 'an_orcid_id')
        # Check contacts params
        self.assertEqual(self.biotool.informations.contacts[0].email, 'an_email')
        self.assertEqual(self.biotool.informations.contacts[0].name, 'a_name')
        # Check publications params
        self.assertEqual(self.biotool.informations.publications[0].doi, 'a_doi')
        self.assertEqual(self.biotool.informations.publications[0].pmid, 'a_pm_id')
        self.assertEqual(self.biotool.informations.publications[0].pmcid, 'a_pmc_id')
        self.assertEqual(self.biotool.informations.publications[0].type, 'a_type')
        # Check documentations params
        self.assertEqual(self.biotool.informations.documentations[0].url, 'an_url')
        self.assertEqual(self.biotool.informations.documentations[0].type, 'a_type')
        self.assertEqual(self.biotool.informations.documentations[0].comment, 'a_comment')

    def test_add_functions(self):
        function = [{'operation':[EDAM],
                     'input':[{'data':EDAM, 'format':[EDAM]}],
                     'output':[{'data':EDAM, 'format':[EDAM]}]}]
        self.biotool.add_functions(function)
        # Check function
        self.assertEqual(self.biotool.functions[0].operations[0].uri, EDAM['uri'])
        self.assertEqual(self.biotool.functions[0].operations[0].term, EDAM['term'])
        # Check inputs
        self.assertEqual(self.biotool.functions[0].inputs[0].data_type.uri,\
                         EDAM['uri'])
        self.assertEqual(self.biotool.functions[0].inputs[0].data_type.term, \
                         EDAM['term'])
        self.assertEqual(self.biotool.functions[0].inputs[0].formats[0].uri,\
                         EDAM['uri'])
        self.assertEqual(self.biotool.functions[0].inputs[0].formats[0].term, \
                         EDAM['term'])
        self.assertIsNone(self.biotool.functions[0].inputs[0].description)
        # Check outputs
        self.assertEqual(self.biotool.functions[0].outputs[0].data_type.uri, \
                         EDAM['uri'])
        self.assertEqual(self.biotool.functions[0].outputs[0].data_type.term, \
                         EDAM['term'])
        self.assertEqual(self.biotool.functions[0].outputs[0].formats[0].uri, \
                         EDAM['uri'])
        self.assertEqual(self.biotool.functions[0].outputs[0].formats[0].term, \
                         EDAM['term'])
        self.assertIsNone(self.biotool.functions[0].outputs[0].description)

    def test_add_topics(self):
        topics =[EDAM]
        self.biotool.add_topics(topics)
        self.assertEqual(self.biotool.topics[0].uri, EDAM['uri'])
        self.assertEqual(self.biotool.topics[0].term, EDAM['term'])


class TestInformations(unittest.TestCase):

    def test_init(self):
        info = model.Informations()
        self.assertListEqual(info.publications, [])
        self.assertListEqual(info.documentations, [])
        self.assertListEqual(info.contacts, [])
        self.assertListEqual(info.credits, [])


class TestCredit(unittest.TestCase):

    def test_init(self):
        dict_credit = {'comment':'a_comment', 'email':'an_email', 'gridId':'a_grid_id',\
                       'name':'a_name', 'typeEntity':'a_type_entity', 'typeRole':'a_type_role', \
                       'url':'an_url', 'orcidId':'an_orcid_id'}
        credit = model.Credit(dict_credit)
        self.assertEqual(credit.comment, dict_credit['comment'])
        self.assertEqual(credit.email, dict_credit['email'])
        self.assertEqual(credit.grid_id, dict_credit['gridId'])
        self.assertEqual(credit.name, dict_credit['name'])
        self.assertEqual(credit.type_entity, dict_credit['typeEntity'])
        self.assertEqual(credit.type_role, dict_credit['typeRole'])
        self.assertEqual(credit.url, dict_credit['url'])
        self.assertEqual(credit.orcid_id, dict_credit['orcidId'])


class TestPublication(unittest.TestCase):

    def test_init(self):
        dict_publi = {'doi':'a_doi', 'pmid':'a_pm_id', 'pmcid':'a_pmc_id', 'type':'a_type'}
        publication = model.Publication(dict_publi)
        self.assertEqual(publication.doi,dict_publi['doi'])
        self.assertEqual(publication.pmid,dict_publi['pmid'])
        self.assertEqual(publication.pmcid,dict_publi['pmcid'])
        self.assertEqual(publication.type,dict_publi['type'])


class TestDocumentation(unittest.TestCase):

    def test_init(self):
        dict_doc = {'url':'one_url', 'type':'one_type', 'comment':'one comment with spaces.'}
        documentation = model.Documentation(dict_doc)
        self.assertEqual(documentation.url, dict_doc['url'])
        self.assertEqual(documentation.type, dict_doc['type'])
        self.assertEqual(documentation.comment, dict_doc['comment'])


class TestContact(unittest.TestCase):

    def test_init(self):
        dict_contact = {'email':'an_email', 'name':'a_name'}
        contact = model.Contact(dict_contact)
        self.assertEqual(contact.email,dict_contact['email'])
        self.assertEqual(contact.name,dict_contact['name'])


class TestFunction(unittest.TestCase):

    def setUp(self):
        self.function = model.Function([EDAM])

    def test_init(self):
        self.assertEqual(self.function.operations[0].uri, EDAM['uri'])
        self.assertEqual(self.function.operations[0].term, EDAM['term'])
        self.assertListEqual(self.function.inputs,[])
        self.assertListEqual(self.function.outputs,[])

    def test_add_inputs(self):
        inputs = [{'data':EDAM,
                   'format': [EDAM]}]
        self.function.add_inputs(inputs)
        self.assertEqual(self.function.inputs[0].data_type.uri, EDAM['uri'])
        self.assertEqual(self.function.inputs[0].data_type.term, EDAM['term'])
        self.assertEqual(self.function.inputs[0].formats[0].uri, EDAM['uri'])
        self.assertEqual(self.function.inputs[0].formats[0].term, EDAM['term'])
        self.assertIsNone(self.function.inputs[0].description)

    def test_add_outputs(self):
        outputs = [{'data': EDAM,
                   'format': [EDAM]}]
        self.function.add_outputs(outputs)
        self.assertEqual(self.function.outputs[0].data_type.uri, EDAM['uri'])
        self.assertEqual(self.function.outputs[0].data_type.term, EDAM['term'])
        self.assertEqual(self.function.outputs[0].formats[0].uri, EDAM['uri'])
        self.assertEqual(self.function.outputs[0].formats[0].term, EDAM['term'])
        self.assertIsNone(self.function.outputs[0].description)
        

class TestData(unittest.TestCase):

    def test_init(self):
        data_type = EDAM
        formats = [EDAM]
        description = 'a description of a data with spaces.'
        data = model.Data(data_type, formats, description)
        self.assertEqual(data.data_type.uri, EDAM['uri'])
        self.assertEqual(data.data_type.term, EDAM['term'])
        self.assertEqual(data.formats[0].uri, EDAM['uri'])
        self.assertEqual(data.formats[0].term, EDAM['term'])
        self.assertEqual(data.description, description)

class TestInput(TestData):

    def test_init(self):
        TestData.test_init(self)

class TestOutput(TestData):

    def test_init(self):
        TestData.test_init(self)


class TestEdam(unittest.TestCase):

    def setUp(self):
        self.edam = model.Edam(EDAM)

    def test_init(self):
        self.assertEqual(self.edam.uri, EDAM['uri'])
        self.assertEqual(self.edam.term, EDAM['term'])

    def test_get_edam_id(self):
        self.assertEqual(self.edam.get_edam_id(), 'topic_0091')
        
class TestOperation(TestEdam):

    def test_init(self):
        TestEdam.test_init(self)

class TestData_type(TestEdam):

    def test_init(self):
        TestEdam.test_init(self)

class TestFormat(TestEdam):

    def test_init(self):
        TestEdam.test_init(self)

class TestTopic(TestEdam):

    def test_init(self):
        TestEdam.test_init(self)


class TestImportJson(unittest.TestCase):

    def test_json_from_file(self):
        j = main.json_from_file('MacSyFinder.json')
        self.assertEqual(len(j.keys()), 32)
        self.assertEqual(j['version'], '1.0.2')
        self.assertEqual(j['name'], 'MacSyFinder')
        self.assertEqual(j['owner'], 'bneron')
        self.assertEqual(j['id'], 'MacSyFinder')

    #def test_json_from_biotool(self):


class TestMainFunctions(unittest.TestCase):

    def test_json_to_biotool(self):
        j = main.json_from_file('MacSyFinder.json')
        bt = main.json_to_biotool(j)
        # Check 3/5 arguments of biotool object
        self.assertEqual(bt.name, 'MacSyFinder')
        self.assertEqual(bt.tool_id, 'MacSyFinder')
        self.assertEqual(bt.version, '1.0.2')
        # Check few arguments from Information object
        self.assertEqual(bt.informations.contacts[0].name, 'Bertrand Néron')
        self.assertEqual(bt.informations.credits[0].name, 'Institut Pasteur')
        self.assertEqual(bt.informations.documentations[0].type, \
                         'Citation instructions')
        self.assertEqual(bt.informations.publications[0].doi, \
                         'doi:10.1371/journal.pone.0110726')
        # Check few arguments from function
        self.assertEqual(bt.functions[0].operations[0].term, \
                         'Prediction and recognition (protein)')
        self.assertEqual(bt.functions[0].inputs[0].data_type.term, \
                         'Protein sequence record')
        self.assertEqual(bt.functions[0].outputs[0].data_type.term, 'Report')
        # Check few arguments from topics
        self.assertEqual(bt.topics[0].term, 'Functional genomics')

    #def test_write_xml(self):


class TestGenerateXml(unittest.TestCase):

    def setUp(self):
        # Create a biotool
        self.biotool = model.Biotool('a_name', 'an_id', 'a_version', 'a_description',\
                                     'a_homepage')
        self.genxml = galaxy.GenerateXml(self.biotool)

    def test_init(self):
        # Test counters
        self.assertEqual(self.genxml.input_ct, 0)
        self.assertEqual(self.genxml.output_ct, 0)
        # Copy tool to make it easier to read
        tool = self.genxml.tool
        # Test simple values of the tool
        self.assertEqual(tool.help, self.biotool.description + \
                         "\n\nTool Homepage: " + self.biotool.homepage)
        self.assertEqual(tool.version_command, "COMMAND --version")
        # Test <tool> of the future XML
        self.assertEqual(tool.root.attrib['id'], 'an_id')
        self.assertEqual(tool.root.attrib['name'], 'a_name')
        self.assertEqual(tool.root.attrib['version'], 'a_version')
        # Test <description> of the future XML
        self.assertEqual(tool.root.find('description').text, 'a_description')

    def test_add_edam_topic(self):
        # Create a Topic object
        topic = model.Topic(EDAM)
        self.genxml.add_edam_topic(topic)
        # Test
        self.assertEqual(self.genxml.tool.edam_topics.children[0].node.text, 'topic_0091')

    def test_add_edam_operation(self):
        # Create a Operation object (Warning: EDAM is a topic)
        operation = model.Operation(EDAM)
        self.genxml.add_edam_operation(operation)
        # Test
        self.assertEqual(self.genxml.tool.edam_operations.children[0].node.text, 'topic_0091')

    def test_add_input_file(self):
        # Create a Input object (Warning both Type and Format will be a topic)
        input = model.Input(EDAM,[EDAM])
        self.genxml.add_input_file(input)
        # Copy object to test (easier to read)
        input_attrib = self.genxml.tool.inputs.children[0].node.attrib
        self.assertEqual(input_attrib['help'], '(INPUT1)')
        self.assertEqual(input_attrib['name'], 'INPUT1')
        self.assertEqual(input_attrib['format'], EDAM['term'])
        self.assertEqual(input_attrib['label'], EDAM['term'])
        self.assertEqual(input_attrib['type'], 'data')

    def test_write_xml(self):
        tmp_file = 'tmp_test_write_xml'
        self.genxml.write_xml(tmp_file)
        self.assertTrue(filecmp.cmp('test_write_xml.xml',tmp_file))
        os.remove(tmp_file)


###########  Main  ###########

if __name__ == "__main__":
    unittest.main()
