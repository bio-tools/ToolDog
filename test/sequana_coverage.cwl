#!/usr/bin/env cwl-runner

cwlVersion: v1.0
id: sequana_coverage
label: Show coverage and interval of confidence to identify under and over represented
  genomic regions.
baseCommand: COMMAND
class: CommandLineTool
doc: "Show coverage and interval of confidence to identify under and over represented\
  \ genomic regions. The tool also creates an HTML report with various images showing\
  \ the coverage and GC versus coverage plots. It also provides a set of CSV files\
  \ with low or high coverage regions (as compared to the average coverage).\n\nTool\
  \ Homepage: http://sequana.readthedocs.io"
inputs:
  INPUT1:
    type: File
    label: Position-specific scoring matrix
    format: http://edamontology.org/format_2572, http://edamontology.org/format_3003,
      http://edamontology.org/format_3475
    inputBinding:
      prefix: --INPUT1
outputs:
  OUTPUT1:
    type: File
    label: Report
    format: http://edamontology.org/format_2331
    outputBinding:
      glob: OUTPUT1.ext
