#!/usr/bin/env cwl-runner

cwlVersion: v1.0
id: sequana_coverage
label: Show coverage and interval of confidence to identify under and over represented
  genomic regions.
baseCommand: COMMAND
doc: "Show coverage and interval of confidence to identify under and over represented\
  \ genomic regions. The tool also creates an HTML report with various images showing\
  \ the coverage and GC versus coverage plots. It also provides a set of CSV files\
  \ with low or high coverage regions (as compared to the average coverage).\n\nTool\
  \ Homepage: http://sequana.readthedocs.io"
class: CommandLineTool
inputs:
  INPUT1:
    label: Position-specific scoring matrix
    format: http://edamontology.org/format_2572, http://edamontology.org/format_3003,
      http://edamontology.org/format_3475
    type: File
    inputBinding:
      prefix: --INPUT1
outputs:
  OUTPUT1:
    label: Report
    format: http://edamontology.org/format_2331
    type: File
    outputBinding:
      glob: OUTPUT1.ext
s:name: sequana_coverage
s:about: Show coverage and interval of confidence to identify under and over represented
  genomic regions. The tool also creates an HTML report with various images showing
  the coverage and GC versus coverage plots. It also provides a set of CSV files with
  low or high coverage regions (as compared to the average coverage).
s:url: http://sequana.readthedocs.io
s:programmingLanguage:
- Javascript
- Python
$namespace:
  s: http://schema.org/
