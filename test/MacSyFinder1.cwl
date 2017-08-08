#!/usr/bin/env cwl-runner

cwlVersion: v1.0
id: MacSyFinder
label: MacSyFinder is a program to model and detect macromolecular systems, genetic
  pathways.
baseCommand: COMMAND
doc: "MacSyFinder is a program to model and detect macromolecular systems, genetic\
  \ pathways... in protein datasets. In prokaryotes, these systems have often evolutionarily\
  \ conserved properties: they are made of conserved components, and are encoded in\
  \ compact loci (conserved genetic architecture). The user models these systems with\
  \ MacSyFinder to reflect these conserved features, and to allow their efficient\
  \ detection.\n\nExternal links:\nTool homepage: https://github.com/gem-pasteur/macsyfinder\n\
  bio.tools_ entry: MacSyFinder\n\n"
class: CommandLineTool
inputs:
  INPUT1:
    label: Protein sequence record
    format: http://edamontology.org/format_2200, http://edamontology.org/format_1929
    type: File
    inputBinding:
      prefix: --INPUT1
  INPUT2:
    label: Sequence-profile alignment
    format: http://edamontology.org/format_3329
    type: File
    inputBinding:
      prefix: --INPUT2
  INPUT3:
    label: Resource metadata
    format: http://edamontology.org/format_2332
    type: File
    inputBinding:
      prefix: --INPUT3
outputs:
  OUTPUT1:
    label: Report
    format: http://edamontology.org/format_3475
    type: File
    outputBinding:
      glob: OUTPUT1.ext
  OUTPUT2:
    label: Report
    format: http://edamontology.org/format_3475
    type: File
    outputBinding:
      glob: OUTPUT2.ext
  OUTPUT3:
    label: Report
    format: http://edamontology.org/format_3475
    type: File
    outputBinding:
      glob: OUTPUT3.ext
  OUTPUT4:
    label: Report
    format: http://edamontology.org/format_3464
    type: File
    outputBinding:
      glob: OUTPUT4.ext
s:name: MacSyFinder
s:about: 'MacSyFinder is a program to model and detect macromolecular systems, genetic
  pathways... in protein datasets. In prokaryotes, these systems have often evolutionarily
  conserved properties: they are made of conserved components, and are encoded in
  compact loci (conserved genetic architecture). The user models these systems with
  MacSyFinder to reflect these conserved features, and to allow their efficient detection.'
s:url: https://github.com/gem-pasteur/macsyfinder
s:programmingLanguage:
- Python
s:publication:
- id: http://dx.doi.org/doi:10.1371/journal.pone.0110726
$namespace:
  s: http://schema.org/
