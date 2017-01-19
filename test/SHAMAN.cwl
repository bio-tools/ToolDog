#!/usr/bin/env cwl-runner

cwlVersion: v1.0
id: SHAMAN
label: SHAMAN is a SHiny application for Metagenomic ANalysis including the normalization,
  the differential analysis and mutiple visualization.
baseCommand: COMMAND
class: CommandLineTool
doc: "SHAMAN is a SHiny application for Metagenomic ANalysis including the normalization,\
  \ the differential analysis and mutiple visualization.\n\nSHAMAN is based on DESeq2\
  \ R package [Anders and Huber 2010] for the analysis of metagenomic data, as suggested\
  \ in [McMurdie and Holmes 2014, Jonsson2016] . SHAMAN robustly identifies the differential\
  \ abundant genera with the Generalized Linear Model implemented in DESeq2 [Love\
  \ 2014] . Resulting p-values are adjusted according to the Benjamini and Hochberg\
  \ procedure [Benjamini and Hochberg 1995]. The PCOA is performed with the ade4 R\
  \ package and plots are generated with ggplot2 or D3.js packages. SHAMAN is compatible\
  \ with standard formats for metagenomic analysis.\n\nTool Homepage: http://shaman.c3bi.pasteur.fr/"
inputs:
  INPUT1:
    type: File
    label: Report
    format: http://edamontology.org/format_3475
    inputBinding:
      prefix: --INPUT1
outputs:
  OUTPUT1:
    type: File
    label: Plot
    outputBinding:
      glob: OUTPUT1.ext
