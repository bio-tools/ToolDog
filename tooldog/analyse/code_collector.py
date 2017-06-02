#!/usr/bin/env python3

import logging

LOGGER = logging.getLogger(__name__)

class CodeCollector(object):
    """
    Class to download source code from a https://bio.tools entry 
    """

    def __init__(self, biotool):
        """
        :param biotool: Biotool object
        :type biotool: :class:`tooldog.biotool_model.Biotool`
        """
        self.biotool = biotool

    def _get_from_repository(self, url):
        """
        Get source code from a repository link

        :param url: url of the repository
        :type url: STRING
        """
        # Here we deal with repository, have to use regex to test the url and
        # use appropriate strategy to get the code depending the type of repository
        return None

    def _get_from_source_code(self, url):
        """
        Get source code from a source code link

        :param url: url of the source code
        :type url: STRING
        """
        return None

    def get_source(self):
        """
        Retrieve source code of the tool using links provided in https://bio.tools
        """
        links = self.biotool.informations.links
        for link in links:
            link_type = link.type.lower().translate(str.maketrans(' ','_'))
            try:
                source_code = getattr(self, '_get_from_{}'.format(link_type))(link)
            except AttributeError:
                LOGGER.warn(link_type + ' link type is not processed yet by ToolDog.')
            if source_code is not None:
                # For the moment, consider that if a source code has been found,
                # we just leave the loop.
                break
        return source_code
