#!/usr/bin/env cwl-runner

$namespaces: {edam: https://edamontology.org/, s: http://schema.org/}
baseCommand: COMMAND
class: CommandLineTool
cwlVersion: v1.0
doc: |+
  MacSyFinder is a program to model and detect macromolecular systems, genetic pathways... in protein datasets. In prokaryotes, these systems have often evolutionarily conserved properties: they are made of conserved components, and are encoded in compact loci (conserved genetic architecture). The user models these systems with MacSyFinder to reflect these conserved features, and to allow their efficient detection.

  External links:
  Tool homepage: https://github.com/gem-pasteur/macsyfinder
  bio.tools entry: MacSyFinder

id: MacSyFinder
inputs:
  INPUT1:
    format: http://edamontology.org/format_3464
    inputBinding: {prefix: --INPUT1}
    label: Report
    type: File
label: MacSyFinder is a program to model and detect macromolecular systems, genetic
  pathways.
s:about: 'MacSyFinder is a program to model and detect macromolecular systems, genetic
  pathways... in protein datasets. In prokaryotes, these systems have often evolutionarily
  conserved properties: they are made of conserved components, and are encoded in
  compact loci (conserved genetic architecture). The user models these systems with
  MacSyFinder to reflect these conserved features, and to allow their efficient detection.'
s:keywords: [edam:topic_0085]
s:name: MacSyFinder
s:programmingLanguage: [Python]
s:publication:
- {id: http://dx.doi.org/doi:10.1371/journal.pone.0110726}
s:url: https://github.com/gem-pasteur/macsyfinder
