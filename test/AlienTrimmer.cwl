#!/usr/bin/env cwl-runner

cwlVersion: v1.0
id: AlienTrimmer
label: Trimming and Clipping FASTQ-formatted read files.
baseCommand: COMMAND
doc: "Trimming and Clipping FASTQ-formatted read files\n\nTool Homepage: https://research.pasteur.fr/en/software/alientrimmer/"
class: CommandLineTool
inputs:
  INPUT1:
    label: DNA sequence (raw)
    format: http://edamontology.org/format_1930
    type: File
    inputBinding:
      prefix: --INPUT1
  INPUT2:
    label: DNA sequence (raw)
    format: http://edamontology.org/format_1929
    type: File
    inputBinding:
      prefix: --INPUT2
outputs:
  OUTPUT1:
    label: DNA sequence (raw)
    format: http://edamontology.org/format_1930
    type: File
    outputBinding:
      glob: OUTPUT1.ext
s:name: AlienTrimmer
s:about: Trimming and Clipping FASTQ-formatted read files
s:url: https://research.pasteur.fr/en/software/alientrimmer/
s:programmingLanguage:
- Java
s:publication:
- id: http://dx.doi.org/10.3389/fgene.2014.00130
$namespace:
  s: http://schema.org/
