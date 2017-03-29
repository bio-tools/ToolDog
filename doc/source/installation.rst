.. ToolDog - Tool description generator

.. _install:

************
Installation
************

.. _dependencies:

ToolDog dependencies
====================

ToolDog is built with Python 3.6.0 and uses the following libraries:

- galaxyxml_ (>=0.3.2)
- requests (>=2.12.3)
- rdflib (>=4.2.2)
- cwlgen_

.. _galaxyxml: https://github.com/erasche/galaxyxml
.. _cwlgen: https://github.com/common-workflow-language/python-cwlgen

.. _installation:

Installation procedure
======================

Requirements
------------

Prior to Tooldog installation, you need to have the following packages installed
on your machine:

* git (as long as ToolDog is not availabe on Pipy)
* Python 3.6.0

.. Note::
    We highly recommend the use of a virtual environment with Python 3.6.0
    [More info](https://virtualenv.pypa.io/en/latest/)

Pip
---

You can use pip to install directly for the git repository::

.. code-block:: bash
    pip3 install --process-dependency-links git+https://github.com/khillion/ToolDog#egg=tooldog

Manually
--------

Clone the repository and install ToolDog with the following commands::

.. code-block:: bash
    git clone https://gitlab.pasteur.fr/kehillio/ToolDog.git
    cd ToolDog
    pip3 install --process-dependency-links .

.. _uninstallation:

Uninstallation procedure
=========================

Pip
---

You can remove ToolDog with the following command::

    pip uninstall tooldog

