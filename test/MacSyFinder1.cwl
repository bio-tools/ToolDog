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
    label: Protein sequence record
    format: http://edamontology.org/format_2200, http://edamontology.org/format_1929
    inputBinding:
      prefix: --INPUT1
  INPUT2:
    type: File
    label: Sequence-profile alignment
    format: http://edamontology.org/format_3329
    inputBinding:
      prefix: --INPUT2
  INPUT3:
    type: File
    label: Resource metadata
    format: http://edamontology.org/format_2332
    inputBinding:
      prefix: --INPUT3
outputs:
  OUTPUT1:
    type: File
    label: Report
    format: http://edamontology.org/format_3475
    outputBinding:
      glob: OUTPUT1.ext
  OUTPUT2:
    type: File
    label: Report
    format: http://edamontology.org/format_3475
    outputBinding:
      glob: OUTPUT2.ext
  OUTPUT3:
    type: File
    label: Report
    format: http://edamontology.org/format_3475
    outputBinding:
      glob: OUTPUT3.ext
  OUTPUT4:
    type: File
    label: Report
    format: http://edamontology.org/format_3464
    outputBinding:
      glob: OUTPUT4.ext
