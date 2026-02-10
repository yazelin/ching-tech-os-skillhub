#!/usr/bin/env sh
# Simple wrapper: md2doc-evolution <input.md> -o <output.docx>
if [ "$#" -lt 2 ]; then
  echo "Usage: $0 input.md output.docx"
  exit 2
fi
INPUT="$1"
OUTPUT="$2"
md2doc-evolution "$INPUT" -o "$OUTPUT"
