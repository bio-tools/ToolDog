id: SARTools
label: SARTools is a R package dedicated to the differential analysis of RNA-seq data.
baseCommand: COMMAND
class: CommandLineTool
doc: "SARTools is a R package dedicated to the differential analysis of RNA-seq data.\
  \ It provides tools to generate descriptive and diagnostic graphs, to run the differential\
  \ analysis with one of the well known DESeq2 or edgeR packages and to export the\
  \ results into easily readable tab-delimited files. It also facilitates the generation\
  \ of a HTML report which displays all the figures produced, explains the statistical\
  \ methods and gives the results of the differential analysis.\n\nTool Homepage:\
  \ https://github.com/PF2-pasteur-fr/SARTools"
inputs:
  INPUT1:
    type: File
    label: Gene expression data
    format: http://edamontology.org/format_3475
    inputBinding:
      prefix: --INPUT1
outputs:
  OUTPUT1:
    type: File
    label: Plot
    outputBinding:
      glob: OUTPUT1.ext
  OUTPUT2:
    type: File
    label: Experiment report
    format: http://edamontology.org/format_2331
    outputBinding:
      glob: OUTPUT2.ext
  OUTPUT3:
    type: File
    label: Experiment report
    format: http://edamontology.org/format_3475
    outputBinding:
      glob: OUTPUT3.ext
