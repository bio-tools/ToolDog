#!/usr/bin/env cwl-runner

cwlVersion: v1.0
id: BMGE
label: Block Mapping and Gathering using Entropy.
baseCommand: COMMAND
class: CommandLineTool
doc: "Block Mapping and Gathering using Entropy\n\nTool Homepage: https://research.pasteur.fr/en/software/bmge-block-mapping-and-gathering-with-entropy/"
inputs:
  INPUT1:
    type: File
    label: Sequence alignment
    format: http://edamontology.org/format_1998, http://edamontology.org/format_1984
    inputBinding:
      prefix: --INPUT1
outputs:
  OUTPUT1:
    type: File
    label: Sequence alignment
    format: http://edamontology.org/format_1973, http://edamontology.org/format_1998,
      http://edamontology.org/format_1984
    outputBinding:
      glob: OUTPUT1.ext
  OUTPUT2:
    type: File
    label: Report
    format: http://edamontology.org/format_2331
    outputBinding:
      glob: OUTPUT2.ext
