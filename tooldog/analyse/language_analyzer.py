#!/usr/bin/env python3

import logging
import os
from .container import Container
from .utils import *

LOGGER = logging.getLogger(__name__)

class LanguageAnalyzer(object):
    """
    This should be the abstract class for all analyzer
    I have to check the way to properly do that you might be able to help for that :).
    """

    def __init__(self, biotool):
        """
        :param biotool: Biotool object
        :type biotool: :class:`tooldog.biotool_model.Biotool`
        """
        self.biotool = biotool

    def analyse(self):
        """
        Run source code analysis
        """
        pass


class PythonAnalyzer(LanguageAnalyzer):
    """
    Object to specifically analyze Python source code.
    """

    def __init__(self, gen_format, source_code, source_format):
        """
        :param gen_format: tool description language (Galaxy XML or CWL)
        :type gen_format: STRING
        """
        self.gen_format = gen_format  # To be used as an option when running Docker
        self.source_code = source_code
        self.source_format = source_format

    def analyse(self):
        """
        Run source code analysis
        """

        python_path = "/usr/local/lib/python2.7/dist-packages/"

        c = Container("tooldog/analyser",
                      "tail -f /dev/null",  # run until we will stop the container
                      environment={'PYTHONPATH': python_path})

        c.put(self.source_code, "/")

        output = ''
        workdir = ''
        toolname = ''
        with c:
            workdir = get_workdir(execute(c, "unzip /tool.zip"))

            toolname = execute(c, cd(workdir, "python setup.py --name"))

            cd(workdir, pip(2, "install ."))
            cd(workdir, pip(2, "install argparse2tool"))

            output = cd(workdir, gen_cmd(toolname, self.gen_format))

        current_path = os.path.realpath(os.getcwd())
        output_path = os.path.join(current_path, "tmp", tool_filename(toolname, self.gen_format))

        write_to_file(output_path, output, 'w')


        return output_path


