#!/usr/bin/env cwl-runner

cwlVersion: v1.0
id: integron_finder
label: A tool to detect Integron in DNA sequences.
baseCommand: COMMAND
doc: "A tool to detect Integron in DNA sequences\n\nTool Homepage: https://github.com/gem-pasteur/Integron_Finder"
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
s:edam_topic:
- url: http://edamontology.org/topic_0085
- url: http://edamontology.org/topic_0798
- url: http://edamontology.org/topic_3047
- url: http://edamontology.org/topic_0091
- url: http://edamontology.org/topic_0080
$namespace:
  s: http://schema.org/
