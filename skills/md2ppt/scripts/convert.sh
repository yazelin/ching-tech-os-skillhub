#!/usr/bin/env sh
# Simple wrapper: md2ppt-evolution <input.md> -o <output.pptx>
if [ "$#" -lt 2 ]; then
  echo "Usage: $0 input.md output.pptx"
  exit 2
fi
INPUT="$1"
OUTPUT="$2"
md2ppt-evolution "$INPUT" -o "$OUTPUT"
