.. ToolDog - Tool description generator

.. _changelog:

**********
Changelogs
**********

Summary of developments of ToolDog software.

v0.3
====

v0.3.1
------

* DOI are not fetched when only PMID or PMCID is given on bio.tools through this `API`_
* Addition of ``--inout_biotools`` to also write inputs and outputs from https://bio.tools in the tool description
* Namespaces have been added to cwlgen library so more information can be written in the CWL tool description
* Better errors and warnings handling for code analysis part
* ToolDog is not asking for ``id/version`` anymore but only ``id`` instead

.. _API: https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/

v0.3.0
------

* Addition of source code analysis feature:

  * use argparse2tool in a docker container
  * only cover python tools using argparse

* Both part of ToolDog can be run independently:

  * `tooldog --analyse tool_id/version`
  * `tooldog --annotate tool_id/version`

* Options are available to specify language of the tool manually, as well as a path to access source code locally

v0.2
====

v0.2.2
------

* Add import feature from cwlgen to the workflow

v0.2.1
------

* Modify architecture of ToolDog
* add `--analyse` (feature not available yet) and `--annotate` arguments

v0.2.0
------

This is the first release of Tooldog:

* Import bio.tools description from online or local JSON file
* Generation of Galaxy XML:

  * Generates skeleton from bio.tools description (metadata)
  * Possibility to add EDAM annotation and citations to existing Galaxy XML

* Generation CWL tool:

  * Generates skeleton from bio.tools description (metadata)
