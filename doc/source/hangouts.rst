.. ToolDog - Tool description generator

.. _hangouts:

************
Hangouts
************

24–28 April 2017, Paris
=======================

The meeting was to set up the collaboration between ELIXIR France (Hervé Menager, Kenzo-Hugo Hillion) and ELIXIR Estonia (Hedi Peterson, Ivan Kuzmin) nodes on the development of the workbench integration enabler.

Currently the tool generates Galaxy XML or CWL directly from the bio.tools tool description file in JSON as shown in the following figure.

|current_design|

After discussing the design of the tool an idea for a new architecture has emerged. ToolDog will not simply be monodirectional, but instead would allow to go from any given tool descriptor to another one as illustrated in the next figure.

|proposed_design|

Therefore, work is going to be first focused on both galaxyxml and cwlgen libraries to cover all different fields from corresponding tool descriptors. Then this libraries need to allow accurate import of existing files into the corresponding model. After that the new model for ToolDog can be built.

.. |current_design| image:: _static/images/current_design.svg
    :alt: The UMl-like figure of the current design.
.. TODO: Write descriptive alt-text in HUTN

.. |proposed_design| image:: _static/images/proposed_design.svg
    :alt: The UMl-like figure of the proposed design.
.. TODO: Write descriptive alt-text in HUTN