#!/usr/bin/env cwl-runner

cwlVersion: v1.0
id: BMGE
label: Block Mapping and Gathering using Entropy.
baseCommand: COMMAND
doc: "Block Mapping and Gathering using Entropy\n\nTool Homepage: https://research.pasteur.fr/en/software/bmge-block-mapping-and-gathering-with-entropy/"
class: CommandLineTool
inputs:
  INPUT1:
    label: Sequence alignment
    format: http://edamontology.org/format_1998, http://edamontology.org/format_1984
    type: File
    inputBinding:
      prefix: --INPUT1
outputs:
  OUTPUT1:
    label: Sequence alignment
    format: http://edamontology.org/format_1973, http://edamontology.org/format_1998,
      http://edamontology.org/format_1984
    type: File
    outputBinding:
      glob: OUTPUT1.ext
  OUTPUT2:
    label: Report
    format: http://edamontology.org/format_2331
    type: File
    outputBinding:
      glob: OUTPUT2.ext
s:name: BMGE
s:about: Block Mapping and Gathering using Entropy
s:url: https://research.pasteur.fr/en/software/bmge-block-mapping-and-gathering-with-entropy/
s:programmingLanguage:
- Java
s:publication:
- id: http://dx.doi.org/10.1186/1471-2148-10-210
$namespace:
  s: http://schema.org/
