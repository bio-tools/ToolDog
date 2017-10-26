#!/usr/bin/env python3

'''
Unit tests for ToolDog
'''

#  Import  ------------------------------

# General libraries
import os
import json
import filecmp
import unittest

# External libraries
import requests_mock

# Class and Objects
from tooldog import main, biotool_model
from tooldog.annotate import galaxy, cwl, edam_to_galaxy

#  Constant(s)  ------------------------------

# Declare one ontology for all the test
EDAM_TOPIC = {'uri':'http://edamontology.org/topic_0091',
              'term':'bioinformatics'}
EDAM_OPE = {'uri':'http://edamontology.org/operation_2429',
             'term':'mapping'}
EDAM_DATA = {'uri':'http://edamontology.org/data_0924',
             'term':'sequence_trace'}
EDAM_FORMAT = {'uri':'http://edamontology.org/format_1930',
               'term':'fastq'}

#  Function(s)  ------------------------------

#  Class(es)  ------------------------------

class TestBiotool(unittest.TestCase):

    def setUp(self):
        self.biotool = biotool_model.Biotool('name', 'an_id', 'a_version', 'a description '+\
                                       'with spaces.', 'http://urltohomepage.com')

    def test_init(self):
        self.assertEqual(self.biotool.name, 'name')
        self.assertEqual(self.biotool.tool_id, 'an_id')
        self.assertEqual(self.biotool.version, 'a_version')
        self.assertEqual(self.biotool.description, 'a description with spaces.')
        self.assertEqual(self.biotool.homepage, 'http://urltohomepage.com')
        self.assertListEqual(self.biotool.functions, [])
        self.assertListEqual(self.biotool.topics, [])
        #self.assertIsNone(self.biotool.informations)

    def test_set_informations(self):
        tool_credits = [{'comment':'a_comment', 'email':'an_email',\
                    'gridId':'a_grid_id', 'name':'a_name',\
                    'typeEntity':'a_type_entity', 'typeRole':'a_type_role',\
                    'url':'a_url', 'orcidId':'an_orcid_id'}]
        contacts = [{'email':'an_email', 'name':'a_name'}]
        pubs = [{'doi':'a_doi', 'pmid':'a_pm_id', 'pmcid':'a_pmc_id', 'type':'a_type'}]
        docs = [{'url':'an_url', 'type':'a_type', 'comment':'a_comment'}]
        language = ['Python']
        link = [{'url': 'a_url', 'type': 'Repository', 'comment': 'a comment'}]
        download = [{'url': 'a_url', 'type': 'Source code', 'comment': 'a comment'}]
        self.biotool.set_informations(tool_credits, contacts, pubs, docs, language, link, download)
        # Check credits params
        self.assertEqual(self.biotool.informations.tool_credits[0].comment, 'a_comment')
        self.assertEqual(self.biotool.informations.tool_credits[0].email, 'an_email')
        self.assertEqual(self.biotool.informations.tool_credits[0].grid_id, 'a_grid_id')
        self.assertEqual(self.biotool.informations.tool_credits[0].name, 'a_name')
        self.assertEqual(self.biotool.informations.tool_credits[0].type_entity, 'a_type_entity')
        self.assertEqual(self.biotool.informations.tool_credits[0].type_role, 'a_type_role')
        self.assertEqual(self.biotool.informations.tool_credits[0].url, 'a_url')
        self.assertEqual(self.biotool.informations.tool_credits[0].orcid_id, 'an_orcid_id')
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
        # Check language params
        self.assertEqual(self.biotool.informations.language[0], 'Python')
        # Check links
        self.assertEqual(self.biotool.informations.links[0].url, 'a_url')
        self.assertEqual(self.biotool.informations.links[0].type, 'Repository')
        self.assertEqual(self.biotool.informations.links[0].comment, 'a comment')
        self.assertEqual(self.biotool.informations.links[1].url, 'a_url')
        self.assertEqual(self.biotool.informations.links[1].type, 'Source code')
        self.assertEqual(self.biotool.informations.links[1].comment, 'a comment')

    def test_add_functions(self):
        function = [{'operation':[EDAM_OPE],
                     'input':[{'data':EDAM_DATA, 'format':[EDAM_FORMAT]}],
                     'output':[{'data':EDAM_DATA, 'format':[EDAM_FORMAT]}]}]
        self.biotool.add_functions(function)
        # Check function
        self.assertEqual(self.biotool.functions[0].operations[0].uri, EDAM_OPE['uri'])
        self.assertEqual(self.biotool.functions[0].operations[0].term, EDAM_OPE['term'])
        # Check inputs
        self.assertEqual(self.biotool.functions[0].inputs[0].data_type.uri,\
                         EDAM_DATA['uri'])
        self.assertEqual(self.biotool.functions[0].inputs[0].data_type.term, \
                         EDAM_DATA['term'])
        self.assertEqual(self.biotool.functions[0].inputs[0].formats[0].uri,\
                         EDAM_FORMAT['uri'])
        self.assertEqual(self.biotool.functions[0].inputs[0].formats[0].term, \
                         EDAM_FORMAT['term'])
        self.assertIsNone(self.biotool.functions[0].inputs[0].description)
        # Check outputs
        self.assertEqual(self.biotool.functions[0].outputs[0].data_type.uri, \
                         EDAM_DATA['uri'])
        self.assertEqual(self.biotool.functions[0].outputs[0].data_type.term, \
                         EDAM_DATA['term'])
        self.assertEqual(self.biotool.functions[0].outputs[0].formats[0].uri, \
                         EDAM_FORMAT['uri'])
        self.assertEqual(self.biotool.functions[0].outputs[0].formats[0].term, \
                         EDAM_FORMAT['term'])
        self.assertIsNone(self.biotool.functions[0].outputs[0].description)

    def test_add_topics(self):
        topics = [EDAM_TOPIC]
        self.biotool.add_topics(topics)
        self.assertEqual(self.biotool.topics[0].uri, EDAM_TOPIC['uri'])
        self.assertEqual(self.biotool.topics[0].term, EDAM_TOPIC['term'])


class TestInformations(unittest.TestCase):

    def test_init(self):
        info = biotool_model.Informations()
        self.assertListEqual(info.publications, [])
        self.assertListEqual(info.documentations, [])
        self.assertListEqual(info.contacts, [])
        self.assertListEqual(info.tool_credits, [])


class TestCredit(unittest.TestCase):

    def test_init(self):
        dict_credit = {'comment':'a_comment', 'email':'an_email', 'gridId':'a_grid_id',\
                       'name':'a_name', 'typeEntity':'a_type_entity', 'typeRole':'a_type_role', \
                       'url':'an_url', 'orcidId':'an_orcid_id'}
        credit = biotool_model.Credit(dict_credit)
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
        publication = biotool_model.Publication(dict_publi)
        self.assertEqual(publication.doi, dict_publi['doi'])
        self.assertEqual(publication.pmid, dict_publi['pmid'])
        self.assertEqual(publication.pmcid, dict_publi['pmcid'])
        self.assertEqual(publication.type, dict_publi['type'])


class TestDocumentation(unittest.TestCase):

    def test_init(self):
        dict_doc = {'url':'one_url', 'type':'one_type', 'comment':'one comment with spaces.'}
        documentation = biotool_model.Documentation(dict_doc)
        self.assertEqual(documentation.url, dict_doc['url'])
        self.assertEqual(documentation.type, dict_doc['type'])
        self.assertEqual(documentation.comment, dict_doc['comment'])


class TestContact(unittest.TestCase):

    def test_init(self):
        dict_contact = {'email':'an_email', 'name':'a_name'}
        contact = biotool_model.Contact(dict_contact)
        self.assertEqual(contact.email, dict_contact['email'])
        self.assertEqual(contact.name, dict_contact['name'])


class TestFunction(unittest.TestCase):

    def setUp(self):
        self.function = biotool_model.Function([EDAM_TOPIC])

    def test_init(self):
        self.assertEqual(self.function.operations[0].uri, EDAM_TOPIC['uri'])
        self.assertEqual(self.function.operations[0].term, EDAM_TOPIC['term'])
        self.assertListEqual(self.function.inputs, [])
        self.assertListEqual(self.function.outputs, [])

    def test_add_inputs(self):
        inputs = [{'data':EDAM_DATA,
                   'format': [EDAM_FORMAT]}]
        self.function.add_inputs(inputs)
        self.assertEqual(self.function.inputs[0].data_type.uri, EDAM_DATA['uri'])
        self.assertEqual(self.function.inputs[0].data_type.term, EDAM_DATA['term'])
        self.assertEqual(self.function.inputs[0].formats[0].uri, EDAM_FORMAT['uri'])
        self.assertEqual(self.function.inputs[0].formats[0].term, EDAM_FORMAT['term'])
        self.assertIsNone(self.function.inputs[0].description)

    def test_add_outputs(self):
        outputs = [{'data': EDAM_DATA,
                    'format': [EDAM_FORMAT]}]
        self.function.add_outputs(outputs)
        self.assertEqual(self.function.outputs[0].data_type.uri, EDAM_DATA['uri'])
        self.assertEqual(self.function.outputs[0].data_type.term, EDAM_DATA['term'])
        self.assertEqual(self.function.outputs[0].formats[0].uri, EDAM_FORMAT['uri'])
        self.assertEqual(self.function.outputs[0].formats[0].term, EDAM_FORMAT['term'])
        self.assertIsNone(self.function.outputs[0].description)


class TestData(unittest.TestCase):

    def test_init(self):
        data_type = EDAM_DATA
        formats = [EDAM_FORMAT]
        description = 'a description of a data with spaces.'
        data = biotool_model.Data(data_type, formats, description)
        self.assertEqual(data.data_type.uri, EDAM_DATA['uri'])
        self.assertEqual(data.data_type.term, EDAM_DATA['term'])
        self.assertEqual(data.formats[0].uri, EDAM_FORMAT['uri'])
        self.assertEqual(data.formats[0].term, EDAM_FORMAT['term'])
        self.assertEqual(data.description, description)

class TestInput(TestData):

    def test_init(self):
        TestData.test_init(self)

class TestOutput(TestData):

    def test_init(self):
        TestData.test_init(self)


class TestEdam(unittest.TestCase):

    def setUp(self):
        self.edam = biotool_model.Edam(EDAM_TOPIC)

    def test_init(self):
        self.assertEqual(self.edam.uri, EDAM_TOPIC['uri'])
        self.assertEqual(self.edam.term, EDAM_TOPIC['term'])

    def test_get_edam_id(self):
        self.assertEqual(self.edam.get_edam_id(), 'topic_0091')

class TestOperation(TestEdam):

    def test_init(self):
        TestEdam.test_init(self)

class TestDataType(TestEdam):

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
        json_path = os.path.dirname(__file__) + '/MacSyFinder.json'
        j = main.json_from_file(json_path)
        self.assertEqual(len(j.keys()), 32)
        self.assertEqual(j['version'], '1.0.2')
        self.assertEqual(j['name'], 'MacSyFinder')
        self.assertEqual(j['owner'], 'bneron')
        self.assertEqual(j['id'], 'MacSyFinder')

    #def test_json_from_biotool(self):


class TestMainFunctions(unittest.TestCase):

    def test_json_to_biotool(self):
        json_path = os.path.dirname(__file__) + '/MacSyFinder.json'
        j = main.json_from_file(json_path)
        biot = main.json_to_biotool(j)
        # Check 3/5 arguments of biotool object
        self.assertEqual(biot.name, 'MacSyFinder')
        self.assertEqual(biot.tool_id, 'MacSyFinder')
        self.assertEqual(biot.version, '1.0.2')
        # Check few arguments from Information object
        self.assertEqual(biot.informations.contacts[0].name, 'Bertrand Néron')
        self.assertEqual(biot.informations.tool_credits[0].name, 'Institut Pasteur')
        self.assertEqual(biot.informations.documentations[0].type, \
                         'Citation instructions')
        self.assertEqual(biot.informations.publications[0].doi, \
                         'doi:10.1371/journal.pone.0110726')
        # Check few arguments from function
        self.assertEqual(biot.functions[0].operations[0].term, \
                         'Prediction and recognition (protein)')
        self.assertEqual(biot.functions[0].inputs[0].data_type.term, \
                         'Protein sequence record')
        self.assertEqual(biot.functions[0].outputs[0].data_type.term, 'Report')
        # Check few arguments from topics
        self.assertEqual(biot.topics[0].term, 'Functional genomics')


class TestGalaxyToolGen(unittest.TestCase):

    def setUp(self):
        # Create a biotool
        self.biotool = biotool_model.Biotool('a_name', 'an_id', 'a_version', 'a_description.',\
                                     'a_homepage')
        self.genxml = galaxy.GalaxyToolGen(self.biotool)

    def test_init(self):
        # Test counters
        self.assertEqual(self.genxml.input_ct, 0)
        self.assertEqual(self.genxml.output_ct, 0)
        # Copy tool to make it easier to read
        tool = self.genxml.tool
        # Test simple values of the tool
        self.assertEqual(tool.version_command, "COMMAND --version")
        # Test <tool> of the future XML
        self.assertEqual(tool.root.attrib['id'], 'an_id')
        self.assertEqual(tool.root.attrib['name'], 'a_name')
        self.assertEqual(tool.root.attrib['version'], 'a_version')
        # Test <description> of the future XML
        self.assertEqual(tool.root.find('description').text, 'a_description.')

    def test_init_existing(self):
        genxml = galaxy.GalaxyToolGen(self.biotool,
                                    existing_tool=os.path.dirname(__file__) +
                                                  '/test_write_xml.xml')
        self.assertEqual(genxml.tool.version_command, 'COMMAND --version')
        self.assertEqual(genxml.tool.command, 'COMMAND')
        self.assertEqual(genxml.tool.root.attrib['id'], 'an_id')
        self.assertEqual(genxml.tool.root.attrib['name'], 'a_name')
        self.assertEqual(genxml.tool.root.attrib['version'], 'a_version')

    def test_add_edam_topic(self):
        # Create a Topic object
        topic = biotool_model.Topic(EDAM_TOPIC)
        self.genxml.add_edam_topic(topic)
        # Test
        self.assertEqual(self.genxml.tool.edam_topics.children[0].node.text, 'topic_0091')

    def test_add_edam_operation(self):
        # Create a Operation object (Warning: EDAM_TOPIC is a topic)
        operation = biotool_model.Operation(EDAM_OPE)
        self.genxml.add_edam_operation(operation)
        # Test
        self.assertEqual(self.genxml.tool.edam_operations.children[0].node.text, 'operation_2429')

    def test_add_input_file(self):
        # Create a Input object (Warning both Type and Format will be a topic)
        an_input = biotool_model.Input(EDAM_DATA, [EDAM_FORMAT])
        self.genxml.add_input_file(an_input)
        # Copy object to test (easier to read)
        input_attrib = self.genxml.tool.inputs.children[0].node.attrib
        self.assertEqual(input_attrib['name'], 'INPUT1')
        self.assertEqual(input_attrib['format'], 'fastq')
        self.assertEqual(input_attrib['label'], EDAM_DATA['term'])
        self.assertEqual(input_attrib['type'], 'data')

    def test_add_output_file(self):
        # Create a Output object (Warning both Type and Format will be a topic)
        output = biotool_model.Output(EDAM_DATA, [EDAM_FORMAT])
        self.genxml.add_output_file(output)
        # Copy object to test
        output_attrib = self.genxml.tool.outputs.children[0].node.attrib
        self.assertEqual(output_attrib['name'], 'OUTPUT1')
        self.assertEqual(output_attrib['format'], 'fastq')
        self.assertEqual(output_attrib['from_work_dir'], 'OUTPUT1.fastq')

    def test_add_citation(self):
        # Create a Publication object
        dict_pub = {'doi':'doi:123', 'pmid':'', 'pmcid':'', 'type':'a_type'}
        publication = biotool_model.Publication(dict_pub)
        self.genxml.add_citation(publication)
        # Test
        self.assertEqual(self.genxml.tool.citations.children[0].node.text, 'doi:123')
        self.assertEqual(self.genxml.tool.citations.children[0].node.attrib['type'], 'doi')

    def test_write_xml(self):
        tmp_file = 'tmp_test_write_xml.xml'
        self.genxml.write_xml(tmp_file)
        expected_xml = os.path.dirname(__file__) + '/test_write_xml.xml'
        try:
            self.assertTrue(filecmp.cmp(expected_xml, tmp_file))
        finally:
            os.remove(tmp_file)


class TestGalaxyInfo(unittest.TestCase):

    def setUp(self):
        # Create two GalaxyInfo objects
        self.gi = edam_to_galaxy.GalaxyInfo(None)
        with requests_mock.mock() as m:
            edam_format_answer = main.json_from_file(edam_to_galaxy.LOCAL_DATA + \
                                                     '/edam_formats.json') 
            m.get('http://supergalaxy.com/api/datatypes/edam_formats', \
                  json=edam_format_answer)
            edam_data_answer = main.json_from_file(edam_to_galaxy.LOCAL_DATA + \
                                                   '/edam_data.json') 
            m.get('http://supergalaxy.com/api/datatypes/edam_data', \
                  json=edam_data_answer)
            mapping_answer = main.json_from_file(edam_to_galaxy.LOCAL_DATA + \
                                                 '/mapping.json')
            m.get('http://supergalaxy.com/api/datatypes/mapping', \
                  json=mapping_answer)
            version_answer = main.json_from_file(edam_to_galaxy.LOCAL_DATA + \
                                                 '/version.json')
            m.get('http://supergalaxy.com/api/version', \
                  json=version_answer)
            self.gi_url = edam_to_galaxy.GalaxyInfo('http://supergalaxy.com')

    def test_init(self):
        # Tests URLs
        self.assertEqual(self.gi.galaxy_url, 'https://usegalaxy.org')
        self.assertEqual(self.gi_url.galaxy_url, 'http://supergalaxy.com')
        # Tests one EDAM format
        self.assertEqual(self.gi.edam_formats['format_3579'][0], 'jpg')
        self.assertEqual(self.gi_url.edam_formats['format_3579'][0], 'jpg')
        # Tests one EDAM data
        self.assertEqual(self.gi.edam_data['data_0848'][0], 'twobit')
        self.assertEqual(self.gi_url.edam_data['data_0848'][0], 'twobit')
        # Tests class names
        self.assertEqual(self.gi.class_names['fasta'], 'galaxy.datatypes.sequence.Fasta')
        self.assertEqual(self.gi_url.class_names['fasta'], 'galaxy.datatypes.sequence.Fasta')

    def test_select_root(self):
        datatypes = ['fastq','fastq.bz2']
        for gi in [self.gi, self.gi_url]:
            root = gi.select_root(datatypes)
            self.assertEqual(root, 'fastq')


class TestEdamInfo(unittest.TestCase):

    def setUp(self):
        # Create one EdamInfo object
        self.ei = edam_to_galaxy.EdamInfo(None)

    #def test_init(self):
    #    try:
    #        self.assertEqual(len(self.ei.edam_ontology), 33192)
    #    except AssertionError:
    #        print("It is likely that EDAM has been updated.")
    #        raise

    def test_generate_hierarchy(self):
        self.ei.generate_hierarchy()
        self.assertEqual(len(self.ei.edam_data_hierarchy['data_2887']), 2)
        self.assertEqual(self.ei.edam_format_hierarchy['format_1930'][0], 'format_2182')


class TestEdamToGalaxy(unittest.TestCase):

    def setUp(self):
        # Create two EdamToGalaxy objects
        self.etog = edam_to_galaxy.EdamToGalaxy()
        try:
            self.etog_url = edam_to_galaxy.EdamToGalaxy(mapping_json='tmp_mapping.json')
        finally:
            os.remove('tmp_mapping.json')

    def test_init(self):
        for etog in [self.etog, self.etog_url]:
            self.assertEqual(etog.data_to_datatype['data_3002'], 'genetrack')
            self.assertEqual(etog.format_to_datatype['format_1930'], 'fastq')
        self.assertEqual(self.etog_url.galaxy.galaxy_url, 'https://usegalaxy.org')


class TestCwlToolGen(unittest.TestCase):

    def setUp(self):
        # Create a biotool
        self.biotool = biotool_model.Biotool('a_name', 'an_id', 'a_version', 'a_description.',
                                     'a_homepage')
        self.gencwl = cwl.CwlToolGen(self.biotool)

    def test_init(self):
        # Test counters
        self.assertEqual(self.gencwl.input_ct, 0)
        self.assertEqual(self.gencwl.output_ct, 0)
        # Copy tool to make it easier to read
        tool = self.gencwl.tool
        # Test simple values of the tool
        self.assertEqual(tool.id, "an_id")
        self.assertEqual(tool.label, "a_description.")
        self.assertEqual(tool.baseCommand, "COMMAND")
        self.assertListEqual(tool.inputs, [])
        self.assertListEqual(tool.outputs, [])

    def test_init_existing(self):
        gencwl = cwl.CwlToolGen(self.biotool,
                                existing_tool=os.path.dirname(__file__) +
                                              '/test_write_cwl.cwl')
        self.assertEqual(gencwl.tool.id, 'an_id')
        self.assertEqual(gencwl.tool.label, 'a_description.')
        self.assertEqual(gencwl.tool.cwlVersion, 'v1.0')

    def test_add_input_file(self):
        # Create a Input object (Warning both Type and Format will be a topic)
        input = biotool_model.Input(EDAM_DATA, [EDAM_FORMAT])
        self.gencwl.add_input_file(input)
        # Copy object to test (easier to read)
        input_attrib = self.gencwl.tool.inputs[0]
        self.assertEqual(input_attrib.id, 'INPUT1')
        self.assertEqual(input_attrib.type, 'File')
        self.assertEqual(input_attrib.label, EDAM_DATA['term'])
        self.assertEqual(input_attrib.format, EDAM_FORMAT['uri'])
        self.assertEqual(input_attrib.inputBinding.prefix, '--INPUT1')

    def test_add_output_file(self):
        # Create a Output object (Warning both Type and Format will be a topic)
        output = biotool_model.Output(EDAM_DATA, [EDAM_FORMAT])
        self.gencwl.add_output_file(output)
        # Copy object to test
        output_attrib = self.gencwl.tool.outputs[0]
        self.assertEqual(output_attrib.id, 'OUTPUT1')
        self.assertEqual(output_attrib.type, 'File')
        self.assertEqual(output_attrib.label, EDAM_DATA['term'])
        self.assertEqual(output_attrib.format, EDAM_FORMAT['uri'])
        self.assertEqual(output_attrib.outputBinding.glob, 'OUTPUT1.ext')

    def test_write_cwl(self):
        tmp_file = 'tmp_test_write_cwl.cwl'
        self.gencwl.write_cwl(tmp_file, 1)
        expected_cwl = os.path.dirname(__file__) + '/test_write_cwl.cwl'
        try:
            self.assertTrue(filecmp.cmp(expected_cwl, 'tmp_test_write_cwl1.cwl'))
        finally:
            os.remove('tmp_test_write_cwl1.cwl')


###########  Main  ###########

if __name__ == "__main__":
    unittest.main()
