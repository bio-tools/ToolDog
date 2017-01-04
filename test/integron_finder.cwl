id: integron_finder
label: A tool to detect Integron in DNA sequences.
baseCommand: COMMAND
class: CommandLineTool
doc: "A tool to detect Integron in DNA sequences\n\nTool Homepage: https://github.com/gem-pasteur/Integron_Finder"
inputs:
  INPUT1:
    type: File
    label: DNA sequence (raw)
    format: http://edamontology.org/format_1929
    inputBinding:
      prefix: --INPUT1
outputs:
  OUTPUT1:
    type: File
    label: Sequence record
    format: http://edamontology.org/format_1936
    outputBinding:
      glob: OUTPUT1.ext
  OUTPUT2:
    type: File
    label: Feature table
    format: http://edamontology.org/format_3475
    outputBinding:
      glob: OUTPUT2.ext
