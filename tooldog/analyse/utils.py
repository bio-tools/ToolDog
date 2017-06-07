def cd(path, cmd):
    return "bash -c 'cd " + path + " && " + cmd + "'"


def pip(v, cmd):
    return "pip" + str(v) + " " + cmd


def execute(ctx, cmd, verbose=True):
    result = ''
    exe = ctx.exec(cmd)
    for line in exe:
        if verbose: print(line)
        result += line.decode("utf-8")[:-1]
    return result


def gen_cmd(tool_name, gen_format):
    return tool_name + " " + ("--generate_cwl_tool" if gen_format == 'cwl' else "--generate_galaxy_xml")


def get_workdir(unzip_output):
    import re
    m = re.search("creating: (.*?)\\n", unzip_output, re.M)
    return "/" + m.group(1).strip()


def tool_filename(tool_name, gen_format):
    return tool_name + "." + ("cwl" if gen_format == 'cwl' else "xml")


def write_to_file(filename, data='', mode='w'):
    f = open(filename, mode)
    f.write(data)
    f.close()