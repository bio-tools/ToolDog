#!/usr/bin/env cwl-runner

cwlVersion: v1.0
id: SARTools
label: SARTools is a R package dedicated to the differential analysis of RNA-seq data.
baseCommand: COMMAND
doc: "SARTools is a R package dedicated to the differential analysis of RNA-seq data.\
  \ It provides tools to generate descriptive and diagnostic graphs, to run the differential\
  \ analysis with one of the well known DESeq2 or edgeR packages and to export the\
  \ results into easily readable tab-delimited files. It also facilitates the generation\
  \ of a HTML report which displays all the figures produced, explains the statistical\
  \ methods and gives the results of the differential analysis.\n\nTool Homepage:\
  \ https://github.com/PF2-pasteur-fr/SARTools"
class: CommandLineTool
inputs:
  INPUT1:
    label: Gene expression data
    format: http://edamontology.org/format_3475
    type: File
    inputBinding:
      prefix: --INPUT1
outputs:
  OUTPUT1:
    label: Plot
    format: ''
    type: File
    outputBinding:
      glob: OUTPUT1.ext
  OUTPUT2:
    label: Experiment report
    format: http://edamontology.org/format_2331
    type: File
    outputBinding:
      glob: OUTPUT2.ext
  OUTPUT3:
    label: Experiment report
    format: http://edamontology.org/format_3475
    type: File
    outputBinding:
      glob: OUTPUT3.ext
s:name: SARTools
s:about: SARTools is a R package dedicated to the differential analysis of RNA-seq
  data. It provides tools to generate descriptive and diagnostic graphs, to run the
  differential analysis with one of the well known DESeq2 or edgeR packages and to
  export the results into easily readable tab-delimited files. It also facilitates
  the generation of a HTML report which displays all the figures produced, explains
  the statistical methods and gives the results of the differential analysis.
s:url: https://github.com/PF2-pasteur-fr/SARTools
s:programmingLanguage:
- R
s:publication: []
$namespace:
  s: http://schema.org/
