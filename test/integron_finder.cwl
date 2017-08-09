#!/usr/bin/env cwl-runner

cwlVersion: v1.0
id: integron_finder
label: A tool to detect Integron in DNA sequences.
baseCommand: COMMAND
doc: "A tool to detect Integron in DNA sequences\n\nExternal links:\nTool homepage:\
  \ https://github.com/gem-pasteur/Integron_Finder\nbio.tools entry: integron_finder\n\
  \nedam_topic list:\n- http://edamontology.org/topic_0085\n- http://edamontology.org/topic_0798\n\
  - http://edamontology.org/topic_3047\n- http://edamontology.org/topic_0091\n- http://edamontology.org/topic_0080\n"
class: CommandLineTool
inputs:
  INPUT1:
    label: DNA sequence (raw)
    format: http://edamontology.org/format_1929
    type: File
    inputBinding:
      prefix: --INPUT1
outputs:
  OUTPUT1:
    label: Sequence record
    format: http://edamontology.org/format_1936
    type: File
    outputBinding:
      glob: OUTPUT1.ext
  OUTPUT2:
    label: Feature table
    format: http://edamontology.org/format_3475
    type: File
    outputBinding:
      glob: OUTPUT2.ext
s:name: Integron Finder
s:about: A tool to detect Integron in DNA sequences
s:url: https://github.com/gem-pasteur/Integron_Finder
s:programmingLanguage:
- Python
s:publication:
- id: http://dx.doi.org/10.1093/nar/gkw319
$namespace:
  s: http://schema.org/
