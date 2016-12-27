# ToolDog

[![build status](https://gitlab.pasteur.fr/kehillio/ToolDog/badges/master/build.svg)](https://gitlab.pasteur.fr/kehillio/ToolDog/commits/master)
[![coverage report](https://gitlab.pasteur.fr/kehillio/ToolDog/badges/master/coverage.svg)](https://gitlab.pasteur.fr/kehillio/ToolDog/commits/master)

ToolDog (TOOL DescriptiOn Generator) aims to generate XML template for Galaxy or CWL from the description of tools from [Bio.tools](https://bio.tools).

### Full documentation: [here]()

### License

------------------------

# Quick-start guide

## Installation

### Pip

```bash
pip install --no-cache-dir --process-dependency-links git+https://gitlab.pasteur.fr/kehillio/ToolDog.git#egg=tooldog
```

### Manually

Clone the repository and install ToolDog:

```bash
git clone https://gitlab.pasteur.fr/kehillio/ToolDog.git
cd ToolDog
pip install --no-cache-dir --process-dependency-links .
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
