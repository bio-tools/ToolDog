#!/usr/bin/env cwl-runner

$namespace: {s: http://schema.org/}
baseCommand: COMMAND
class: CommandLineTool
cwlVersion: v1.0
doc: |
  A tool to detect Integron in DNA sequences

  External links:
  Tool homepage: https://github.com/gem-pasteur/Integron_Finder
  bio.tools entry: integron_finder

  edam_topic list:
  - http://edamontology.org/topic_0085
  - http://edamontology.org/topic_0798
  - http://edamontology.org/topic_3047
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_0080
id: integron_finder
inputs:
  INPUT1:
    format: http://edamontology.org/format_1929
    inputBinding: {prefix: --INPUT1}
    label: DNA sequence (raw)
    type: File
label: A tool to detect Integron in DNA sequences.
outputs:
  OUTPUT1:
    format: http://edamontology.org/format_1936
    label: Sequence record
    outputBinding: {glob: OUTPUT1.ext}
    type: File
  OUTPUT2:
    format: http://edamontology.org/format_3475
    label: Feature table
    outputBinding: {glob: OUTPUT2.ext}
    type: File
s:about: A tool to detect Integron in DNA sequences
s:name: Integron Finder
s:programmingLanguage: [Python]
s:publication:
- {id: http://dx.doi.org/10.1093/nar/gkw319}
s:url: https://github.com/gem-pasteur/Integron_Finder
