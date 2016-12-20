.. ToolDog - Tool description generator

.. _how_to_use:

***************
How to use it ?
***************

We assume here that the program is :ref:`installed <install>`.

Importation of an entry can be perfomed either from :ref:`online <online_import>` entry or :ref:`local <local_import>` file::

    tooldog -h

ToolDog supports generation of XML files for Galaxy (`-g/--galaxy`) or CWL (`-c/--cwl`, not available yet).

.. _online_import:

From https://bio.tools entry
============================

You can generate a XML for Galaxy from an online bio.tools description using the following command::

    tooldog --galaxy id/version > outfile.xml

.. _local_import:

From JSON local file
====================

To generate XML from a local file, use the following command::

    tooldog --galaxy file.json > outfile.xml
