#!/usr/bin/env cwl-runner

cwlVersion: v1.0
id: BMGE
label: Block Mapping and Gathering using Entropy.
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
baseCommand: COMMAND
doc: "Block Mapping and Gathering using Entropy\n\nTool Homepage: https://research.pasteur.fr/en/software/bmge-block-mapping-and-gathering-with-entropy/"
class: CommandLineTool
