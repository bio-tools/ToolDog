id: AlienTrimmer
label: Trimming and Clipping FASTQ-formatted read files.
baseCommand: COMMAND
class: CommandLineTool
doc: "Trimming and Clipping FASTQ-formatted read files\n\nTool Homepage: https://research.pasteur.fr/en/software/alientrimmer/"
inputs:
  INPUT1:
    type: File
    label: DNA sequence (raw)
    format: http://edamontology.org/format_1930
    inputBinding:
      prefix: --INPUT1
  INPUT2:
    type: File
    label: DNA sequence (raw)
    format: http://edamontology.org/format_1929
    inputBinding:
      prefix: --INPUT2
outputs:
  OUTPUT1:
    type: File
    label: DNA sequence (raw)
    format: http://edamontology.org/format_1930
    outputBinding:
      glob: OUTPUT1.ext
