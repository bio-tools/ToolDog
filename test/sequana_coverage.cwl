#!/usr/bin/env cwl-runner

$namespace: {s: http://schema.org/}
baseCommand: COMMAND
class: CommandLineTool
cwlVersion: v1.0
doc: |+
  Show coverage and interval of confidence to identify under and over represented genomic regions. The tool also creates an HTML report with various images showing the coverage and GC versus coverage plots. It also provides a set of CSV files with low or high coverage regions (as compared to the average coverage).

  External links:
  Tool homepage: http://sequana.readthedocs.io
  bio.tools entry: sequana_coverage

edam:
  operations: []
  topics: [http://edamontology.org/topic_3070, http://edamontology.org/topic_3316]
id: sequana_coverage
inputs:
  INPUT1:
    format: http://edamontology.org/format_2572, http://edamontology.org/format_3003,
      http://edamontology.org/format_3475
    inputBinding: {prefix: --INPUT1}
    label: Position-specific scoring matrix
    type: File
label: Show coverage and interval of confidence to identify under and over represented
  genomic regions.
outputs:
  OUTPUT1:
    format: http://edamontology.org/format_2331
    label: Report
    outputBinding: {glob: OUTPUT1.ext}
    type: File
s:about: Show coverage and interval of confidence to identify under and over represented
  genomic regions. The tool also creates an HTML report with various images showing
  the coverage and GC versus coverage plots. It also provides a set of CSV files with
  low or high coverage regions (as compared to the average coverage).
s:name: sequana_coverage
s:programmingLanguage: [Javascript, Python]
s:url: http://sequana.readthedocs.io
