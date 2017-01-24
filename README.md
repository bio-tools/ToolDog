# ToolDog

[![Build Status](https://travis-ci.org/khillion/ToolDog.svg?branch=master)](https://travis-ci.org/khillion/ToolDog)
[![codecov](https://codecov.io/gh/khillion/ToolDog/branch/master/graph/badge.svg)](https://codecov.io/gh/khillion/ToolDog)
[![Documentation Status](https://readthedocs.org/projects/tooldog/badge/?version=latest)](http://tooldog.readthedocs.io/en/latest/?badge=latest)
[![Python 3](https://img.shields.io/badge/python-3.6.0-blue.svg)](https://www.python.org/downloads/release/python-360/)

ToolDog (TOOL DescriptiOn Generator) aims to generate XML template for Galaxy or CWL from
the description of tools from [Bio.tools](https://bio.tools).

------------------------

# Quick-start guide

## Installation

You can install ToolDog using pip with the following command:

```bash
pip install --no-cache-dir --process-dependency-links git+https://github.com/khillion/ToolDog.git#egg=tooldog
```

## How it works ?

ToolDog supports importation either from [bio.tools](https://bio.tools) or from a local file (downloaded from [bio.tools](https://bio.tools) in JSON format). It can generate XML for Galaxy and CWL (not available yet).

```bash
usage: tooldog [-h] [-g/--galaxy] [-c/--cwl] [-f OUTFILE] biotool_entry
```

To import from [bio.tools](https://bio.tools), specify the `biotool_entry` with the following format: `id/version`:

```bash
tooldog --galaxy SARTools/1.4.0 > sartools.xml
```

You can also use local file by giving its name directly:

```bash
tooldog --galaxy sartools.json > sartools.xml
```

## References
