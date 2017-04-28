.. ToolDog - Tool description generator

.. _how_to_use:

********************
How to use ToolDog ?
********************

ToolDog can either generates a template from a bio.tools entry for Galaxy or CWL but
also annotates exiting tool descriptors with missing metadata.
ToolDog supports generation of XML files for Galaxy (`-g/--galaxy`) or CWL (`-c/--cwl`).

.. Note::
   If you find a bug, have any questions or suggestions, please `create an issue`_ on
   GitHub or contact us on `Gitter`_.

.. _create an issue: https://github.com/bio-tools/ToolDog/issues
.. _Gitter: https://gitter.im/ToolDog/Lobby

.. _online_import:

Import from https://bio.tools entry
===================================

You can generate a XML for Galaxy from an online bio.tools description using the following command:

.. code-block:: bash

    tooldog --galaxy id/version > outfile.xml

.. _local_import:

Import from JSON local file
===========================

To generate XML from a local file, use the following command:

.. code-block:: bash

    tooldog --galaxy file.json > outfile.xml


Annotation of existing files
============================

You can also use ToolDog to add missing metadata from your tool descriptor if the tool
is registered on https://bio.tools:

.. code-block:: bash

    tooldog --galaxy id/version --existing_xml your_xml.xml > annotated_xml.xml

.. Note::
    For the moment, only annotation of Galaxy XML is supported.
