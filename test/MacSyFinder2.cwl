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
  \ detection.\n\nTool Homepage: https://github.com/gem-pasteur/macsyfinder"
class: CommandLineTool
inputs:
  INPUT1:
    label: Report
    format: http://edamontology.org/format_3464
    type: File
    inputBinding:
      prefix: --INPUT1
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
s:edam_topic:
- url: http://edamontology.org/topic_0085
s:edam_operation:
- url: http://edamontology.org/operation_3023
- url: http://edamontology.org/operation_0337
$namespace:
  s: http://schema.org/
