# ToolDog

[![Build Status](https://travis-ci.org/bio-tools/ToolDog.svg?branch=master)](https://travis-ci.org/bio-tools/ToolDog)
[![codecov](https://codecov.io/gh/bio-tools/ToolDog/branch/master/graph/badge.svg)](https://codecov.io/gh/bio-tools/ToolDog)
[![Documentation Status](https://readthedocs.org/projects/tooldog/badge/?version=latest)](http://tooldog.readthedocs.io/en/latest/?badge=latest)
[![Python 3](https://img.shields.io/badge/python-3.6.0-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Gitter Chat](http://img.shields.io/badge/chat-online-brightgreen.svg)](https://gitter.im/ToolDog/Lobby)
[![PyPI version](https://badge.fury.io/py/tooldog.svg)](https://badge.fury.io/py/tooldog)

ToolDog (TOOL DescriptiOn Generator) aims to generate XML template for Galaxy or CWL from
the description of tools from [Bio.tools](https://bio.tools).

------------------------

# Quick-start guide

## Installation

#### Requirements

You can then install ToolDog using pip with the following command:

```bash
pip3 install tooldog
```

## How does it work ?

ToolDog supports import either from [bio.tools](https://bio.tools) or from a local
file (downloaded from [bio.tools](https://bio.tools) in JSON format). It can generates XML
for Galaxy and CWL tool but also annotates existing ones (only support XML so far...).

```bash
usage: tooldog [-h] [-g/--galaxy] [-c/--cwl] [-f OUTFILE] biotool_entry
```

To import from [bio.tools](https://bio.tools), specify the `biotool_entry` with the following format: `id/version`:

```bash
tooldog --galaxy SARTools/1.4.0 > sartools.xml
```

You can also use local file downloaded from [bio.tools](https://bio.tools) API
by giving its name directly:

```bash
tooldog --galaxy sartools.json > sartools.xml
```

More information about ToolDog usage [here](http://tooldog.readthedocs.io/en/latest/how_to_use.html).

## References

Hervé Ménager, Matúš Kalaš, Kristoffer Rapacki and Jon Ison. Using registries to integrate
bioinformatics tools and services into workbench environments. International Journal on
Software Tools for Technology Transfer (2016) doi: [10.1007/s10009-015-0392-z](http://link.springer.com/article/10.1007/s10009-015-0392-z)
