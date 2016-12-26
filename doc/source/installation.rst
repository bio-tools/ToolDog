.. ToolDog - Tool description generator

.. _install:

************
Installation
************

.. _dependencies:

ToolDog dependencies
====================

ToolDog is built with Python 3.5 and uses the following libraries:

- galaxyxml_ (>=0.2.3)
- requests (>=2.12.3)

.. _galaxyxml: https://github.com/erasche/galaxyxml

.. _installation:

Installation procedure
======================

Conda
-----

Pip
---

You can use pip to install directly for the git repository::

    pip install --no-cache-dir --process-dependency-links git+https://gitlab.pasteur.fr/kehillio/ToolDog.git#egg=tooldog

Manually
--------

Clone the repository and install ToolDog with the following commands::

    git clone https://gitlab.pasteur.fr/kehillio/ToolDog.git
    cd ToolDog
    pip install --no-cache-dir --process-dependency-links .

.. _uninstallation:

Uninstallation procedure
=========================

Conda
-----

Pip
---

You can remove ToolDog with the following command::

    pip uninstall tooldog

