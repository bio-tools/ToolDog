# Set of util functions for work with ToolDog container

import sys
import logging

LOGGER = logging.getLogger(__name__)

def cd(path, cmd):
    return "bash -c 'cd " + path + " && " + cmd + "'"


def pip(v, cmd):
    return "pip" + str(v) + " " + cmd


def execute(ctx, cmd):
    result = ''
    exe = ctx.exec(cmd)
    for line in exe:
        output = line.decode("utf-8").rstrip()
        LOGGER.info(output)
        result += output
    return result


def gen_cmd(tool_name, gen_format):
    return tool_name + " " + ("--generate_cwl_tool" if gen_format == 'cwl' else "--generate_galaxy_xml")


def get_workdir(unzip_output):
    import re
    m = re.search("creating: (.*?)\\n", unzip_output, re.M)
    return "/" + m.group(1).strip()


def if_installed(toolname, output):
    substr = toolname + ": command not found"
    if output.find(substr) == -1:
        return True
    else:
        return False


def tool_filename(tool_name, gen_format):
    return tool_name + "." + ("cwl" if gen_format == 'cwl' else "xml")


def write_to_file(filename=None, data='', mode='w'):
    if filename:
        f = open(filename, mode)
        f.write(data)
        f.close()
    else:
        sys.stdout.write(data)


class DockerException(Exception):
    pass
