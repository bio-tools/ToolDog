#!/usr/bin/env cwl-runner

cwlVersion: v1.0
id: MacSyFinder
label: MacSyFinder is a program to model and detect macromolecular systems, genetic
  pathways.
inputs:
  INPUT1:
    label: Report
    format: http://edamontology.org/format_3464
    type: File
    inputBinding:
      prefix: --INPUT1
baseCommand: COMMAND
doc: "MacSyFinder is a program to model and detect macromolecular systems, genetic\
  \ pathways... in protein datasets. In prokaryotes, these systems have often evolutionarily\
  \ conserved properties: they are made of conserved components, and are encoded in\
  \ compact loci (conserved genetic architecture). The user models these systems with\
  \ MacSyFinder to reflect these conserved features, and to allow their efficient\
  \ detection.\n\nTool Homepage: https://github.com/gem-pasteur/macsyfinder"
class: CommandLineTool
