.. ToolDog - Tool description generator

.. _install:

************
Installation
************

Requirements
============

ToolDog is built with Python 3.6.0 and uses the following Python libraries:

- galaxyxml_ (>=0.4.3)
- cwlgen_ (>=0.2.2)
- requests (>=2.13.0)
- rdflib (>=4.2.2)
- docker (==0.2.1)

.. _galaxyxml: https://github.com/erasche/galaxyxml
.. _cwlgen: https://github.com/common-workflow-language/python-cwlgen

Docker is also required in order to perform the code analysis part of the code.

.. Note::
    We highly recommend the use of a virtual environment with Python 3.6.0
    using `virtualenv`_ or `conda`_.

.. _virtualenv: https://virtualenv.pypa.io/en/latest/
.. _conda: http://docs.readthedocs.io/en/latest/conda.html

.. _installation:

Installation procedure
======================

Pip
---

You can use pip to install ToolDog of the latest stable version:

.. code-block:: bash

    pip3 install tooldog

Manually
--------

.. Note::
    This is particularly useful when you wish to install a version under development from
    any branches of the Github repository.

Clone the repository and install ToolDog with the following commands:

.. code-block:: bash

    git clone https://github.com/bio-tools/ToolDog.git
    cd ToolDog
    pip3 install .

.. _uninstallation:

Uninstallation procedure
=========================

Pip
---

You can remove ToolDog with the following command:

.. code-block:: bash

    pip3 uninstall tooldog

.. Note::
    This will not uninstall dependencies. To do so you can make use of the pip-autoremove
    tool `pip-autoremove`_.

.. _pip-autoremove: https://github.com/invl/pip-autoremove 
