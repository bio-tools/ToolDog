#!/usr/bin/env cwl-runner

$namespace: {s: http://schema.org/}
baseCommand: COMMAND
class: CommandLineTool
cwlVersion: v1.0
doc: |+
  This tool allows users to perform an automated workflow to analyze, validate and visualize large HDX-MS datasets. The input file is the output of DynamX software from Waters. Output files provide a plot of the data, the fitted model for each peptide, a plot of the calculated p -values, and a global visualization of the experiment. User could also obtain an overview of all peptides on the 3D structure.

  External links:
  Tool homepage: http://memhdx.c3bi.pasteur.fr/
  bio.tools entry: MEMHDX

edam:
  operations: []
  topics: [http://edamontology.org/topic_3520]
id: MEMHDX
inputs:
  INPUT1:
    format: http://edamontology.org/format_3475
    inputBinding: {prefix: --INPUT1}
    label: Mass spectrometry data
    type: File
label: This tool allows users to perform an automated workflow to analyze, validate
  and visualize large HDX-MS datasets.
outputs:
  OUTPUT1:
    format: ''
    label: Plot
    outputBinding: {glob: OUTPUT1.ext}
    type: File
s:about: This tool allows users to perform an automated workflow to analyze, validate
  and visualize large HDX-MS datasets. The input file is the output of DynamX software
  from Waters. Output files provide a plot of the data, the fitted model for each
  peptide, a plot of the calculated p -values, and a global visualization of the experiment.
  User could also obtain an overview of all peptides on the 3D structure.
s:name: MEMHDX
s:programmingLanguage: [R]
s:publication:
- {id: http://dx.doi.org/10.1093/bioinformatics/btw420}
s:url: http://memhdx.c3bi.pasteur.fr/
