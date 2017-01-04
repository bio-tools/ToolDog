id: MacSyFinder
label: MacSyFinder is a program to model and detect macromolecular systems, genetic
  pathways.
baseCommand: COMMAND
class: CommandLineTool
doc: "MacSyFinder is a program to model and detect macromolecular systems, genetic\
  \ pathways... in protein datasets. In prokaryotes, these systems have often evolutionarily\
  \ conserved properties: they are made of conserved components, and are encoded in\
  \ compact loci (conserved genetic architecture). The user models these systems with\
  \ MacSyFinder to reflect these conserved features, and to allow their efficient\
  \ detection.\n\nTool Homepage: https://github.com/gem-pasteur/macsyfinder"
inputs:
  INPUT1:
    type: File
    label: Report
    format: http://edamontology.org/format_3464
    inputBinding:
      prefix: --INPUT1
