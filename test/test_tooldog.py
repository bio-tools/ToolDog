#! /usr/bin/env python3

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
import unittest

# External libraries
import tooldog

# Class and Objects


###########  Constant(s)  ###########

###########  Function(s)  ###########

###########  Class(es)  ###########

class TestBiotool(unittest.TestCase):

    def setUp(self):
        self.biotool = tooldog.Biotool('name','an_id','a_version','a description '+\
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

    #def test_set_infromations(self):

    def test_add_functions(self):
        edam = {'uri':'one_uri', 'term':'one_term'}
        function = [{'operation':[edam],
                     'input':[{'data':edam, 'format':[edam]}],
                     'output':[{'data':edam, 'format':[edam]}]}]
        self.biotool.add_functions(function)
        # Check function
        self.assertEqual(self.biotool.functions[0].operations[0].uri,'one_uri')
        self.assertEqual(self.biotool.functions[0].operations[0].term,'one_term')
        # Check inputs
        self.assertEqual(self.biotool.functions[0].inputs[0].data_type.uri,\
                         'one_uri')
        self.assertEqual(self.biotool.functions[0].inputs[0].data_type.term, \
                         'one_term')
        self.assertEqual(self.biotool.functions[0].inputs[0].formats[0].uri,\
                         'one_uri')
        self.assertEqual(self.biotool.functions[0].inputs[0].formats[0].term, \
                         'one_term')
        self.assertIsNone(self.biotool.functions[0].inputs[0].description)
        # Check outputs
        self.assertEqual(self.biotool.functions[0].outputs[0].data_type.uri, \
                         'one_uri')
        self.assertEqual(self.biotool.functions[0].outputs[0].data_type.term, \
                         'one_term')
        self.assertEqual(self.biotool.functions[0].outputs[0].formats[0].uri, \
                         'one_uri')
        self.assertEqual(self.biotool.functions[0].outputs[0].formats[0].term, \
                         'one_term')
        self.assertIsNone(self.biotool.functions[0].outputs[0].description)

    def test_add_topics(self):
        edam = {'uri':'one_uri', 'term':'one_term'}
        topics =[edam]
        self.biotool.add_topics(topics)
        self.assertEqual(self.biotool.topics[0].uri, 'one_uri')
        self.assertEqual(self.biotool.topics[0].term, 'one_term')

    #def test_generate_xml(self):


class TestInformations(unittest.TestCase):

    def test_init(self):
        info = tooldog.Informations()
        self.assertListEqual(info.publications, [])
        self.assertListEqual(info.documentations, [])
        self.assertListEqual(info.contacts, [])
        self.assertListEqual(info.credits, [])


class TestCredit(unittest.TestCase):

    def test_init(self):
        dict_credit = {'comment':'a_comment', 'email':'an_email', 'gridId':'a_grid_id',\
                       'name':'a_name', 'typeEntity':'a_type_entity', 'typeRole':'a_type_role', \
                       'url':'an_url', 'orcidId':'an_orcid_id'}
        credit = tooldog.Credit(dict_credit)
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
        publication = tooldog.Publication(dict_publi)
        self.assertEqual(publication.doi,dict_publi['doi'])
        self.assertEqual(publication.pmid,dict_publi['pmid'])
        self.assertEqual(publication.pmcid,dict_publi['pmcid'])
        self.assertEqual(publication.type,dict_publi['type'])


class TestDocumentation(unittest.TestCase):

    def test_init(self):
        dict_doc = {'url':'one_url', 'type':'one_type', 'comment':'one comment with spaces.'}
        documentation = tooldog.Documentation(dict_doc)
        self.assertEqual(documentation.url, dict_doc['url'])
        self.assertEqual(documentation.type, dict_doc['type'])
        self.assertEqual(documentation.comment, dict_doc['comment'])


class TestContact(unittest.TestCase):

    def test_init(self):
        dict_contact = {'email':'an_email', 'name':'a_name'}
        contact = tooldog.Contact(dict_contact)
        self.assertEqual(contact.email,dict_contact['email'])
        self.assertEqual(contact.name,dict_contact['name'])


class TestFunction(unittest.TestCase):

    def setUp(self):
        self.edams = [{'uri':'first_uri', 'term':'first_term'}, \
                 {'uri':'second_uri', 'term':'second_term'}]
        self.function = tooldog.Function(self.edams)

    def test_init(self):
        self.assertEqual(self.function.operations[0].uri,self.edams[0]['uri'])
        self.assertEqual(self.function.operations[0].term,self.edams[0]['term'])
        self.assertEqual(self.function.operations[1].uri,self.edams[1]['uri'])
        self.assertEqual(self.function.operations[1].term,self.edams[1]['term'])
        self.assertListEqual(self.function.inputs,[])
        self.assertListEqual(self.function.outputs,[])

    def test_add_inputs(self):
        inputs = [{'data':self.edams[0],
                   'format': self.edams}]
        self.function.add_inputs(inputs)
        self.assertEqual(self.function.inputs[0].data_type.uri, 'first_uri')
        self.assertEqual(self.function.inputs[0].data_type.term, 'first_term')
        self.assertEqual(self.function.inputs[0].formats[0].uri, 'first_uri')
        self.assertEqual(self.function.inputs[0].formats[0].term, 'first_term')
        self.assertEqual(self.function.inputs[0].formats[1].uri, 'second_uri')
        self.assertEqual(self.function.inputs[0].formats[1].term, 'second_term')
        self.assertIsNone(self.function.inputs[0].description)
        

class TestData(unittest.TestCase):

    def test_init(self):
        data_type = {'uri':'uri_data', 'term':'term_data'}
        formats = [{'uri':'first_uri', 'term':'first_term'}, \
                 {'uri':'second_uri', 'term':'second_term'}]
        description = 'a description of a data with spaces.'
        data = tooldog.Data(data_type, formats, description)
        self.assertEqual(data.data_type.uri, data_type['uri'])
        self.assertEqual(data.data_type.term, data_type['term'])
        self.assertEqual(data.formats[0].uri, formats[0]['uri'])
        self.assertEqual(data.formats[0].term, formats[0]['term'])
        self.assertEqual(data.formats[1].uri, formats[1]['uri'])
        self.assertEqual(data.formats[1].term, formats[1]['term'])
        self.assertEqual(data.description, description)

class TestInput(TestData):

    def test_init(self):
        TestData.test_init(self)

class TestOutput(TestData):

    def test_init(self):
        TestData.test_init(self)


class TestEdam(unittest.TestCase):

    def test_init(self):
        dict_edam = {'uri':'one_uri', 'term':'one_term'}
        edam = tooldog.Edam(dict_edam)
        self.assertEqual(edam.uri, dict_edam['uri'])
        self.assertEqual(edam.term, dict_edam['term'])
        
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


        
        



###########  Main  ###########

if __name__ == "__main__":
    unittest.main()
