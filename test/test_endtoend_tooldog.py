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
from glob import glob

# External libraries
import requests_mock
from nose_parameterized import parameterized

# Class and Objects
from tooldog import main

###########  Constant(s)  ###########

###########  Function(s)  ###########

def get_test_files():
    '''
    List .json files of the test directory
    '''
    test_files = []
    json_dir = os.path.dirname(__file__)
    json_list = glob(os.path.join(json_dir, '*.json'))
    for json_path in json_list:
        name = os.path.splitext(json_path)[0]
        xml_path = name + '.xml'
        test_files.append([name, json_path, xml_path])
    return test_files

###########  Class(es)  ###########

class TestToolDog(unittest.TestCase):

    @parameterized.expand(get_test_files())
    def test_from_local_to_galaxy(self, name, json_path, xml_path):
        json = main.json_from_file(json_path)
        biotool = main.json_to_biotool(json)
        tmp_file = 'tmp_test_xml.xml'
        main.write_xml(biotool,tmp_file)
        tmp_file_list = glob("tmp_*.xml")
        try:
            for temp_file in tmp_file_list:
                if len(tmp_file_list) > 1:
                    xml_path = os.path.splitext(json_path)[0] + \
                               str(tmp_file_list.index(temp_file) + 1) + '.xml' 
                self.assertTrue(filecmp.cmp(xml_path,temp_file))
        finally:
            for temp_file in tmp_file_list:
                os.remove(temp_file)

    @parameterized.expand(get_test_files())
    def test_from_biotools_to_galaxy(self, name, json_path, xml_path):
        # Open json to be the content of the requests_mock
        json_answer = main.json_from_file(json_path)
        with requests_mock.mock() as m:
            m.get('https://bio.tools/api/tool/' + name + '/version/1.0',\
                  json=json_answer)
            json = main.json_from_biotools(name, '1.0')
            biotool = main.json_to_biotool(json)
            tmp_file = 'tmp_test_xml.xml'
            main.write_xml(biotool,tmp_file)
            tmp_file_list = glob("tmp_*.xml")
            try:
                for temp_file in tmp_file_list:
                    if len(tmp_file_list) > 1:
                        xml_path = os.path.splitext(json_path)[0] + \
                                   str(tmp_file_list.index(temp_file) + 1) + '.xml' 
                    self.assertTrue(filecmp.cmp(xml_path,temp_file))
            finally:
                for temp_file in tmp_file_list:
                    os.remove(temp_file)


###########  Main  ###########

if __name__ == "__main__":
    unittest.main()
