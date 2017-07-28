#!/usr/bin/env python3

import logging
import os
from .container import Container
from .utils import *
from tooldog import TMP_DIR

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

    def __init__(self, gen_format, source_code):
        """
        :param gen_format: tool description language (Galaxy XML or CWL)
        :type gen_format: STRING
        """
        self.gen_format = gen_format  # To be used as an option when running Docker
        self.source_code = source_code

    def analyse(self):
        """
        Run source code analysis
        """

        try:
            LOGGER.info("Trying to analyse code as python2")
            return self._analyse(2)
        except DockerException:
            LOGGER.warn("Trying to analyse code as python2")
            LOGGER.info("Trying to analyse code as python3")
            return self._analyse(3)
        except Exception:
            LOGGER.warn("Unknown Docker client error: Docker is not installed/started or unable to use network due to the network restrictions.")
            LOGGER.info("Skipping analysis...")
            return None

    def _analyse(self, version):
        python_path = "/usr/local/lib/python3.5/dist-packages/" if version == 3 else \
            "/usr/local/lib/python2.7/dist-packages/"

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

            execute(c,
                    cd(workdir, pip(version, "install .")))
            execute(c,
                    cd(workdir, pip(version, "install git+https://github.com/erasche/argparse2tool")))

            output = execute(c, cd(workdir, gen_cmd(toolname, self.gen_format)))

        if if_installed(toolname, output):
            output_path = os.path.join(TMP_DIR, tool_filename(toolname, self.gen_format))

            write_to_file(output_path, output, 'w')

            return output_path
        else:
            raise DockerException("Tool was not installed properly")


