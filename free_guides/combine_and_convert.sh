#!/bin/bash
# Combine common pages + unique page 3 for each role, convert to PDF

COMMON="/root/.openclaw/workspace/safemind/free_guides/ru_common_pages.md"
OUTDIR="/root/.openclaw/workspace/safemind/free_pdfs"
mkdir -p "$OUTDIR"

for role in marketing hr teacher legal finance transport procurement economist; do
  PAGE3="/root/.openclaw/workspace/safemind/free_guides/ru_${role}_page3.md"
  OUTPUT="$OUTDIR/safemind_free_guide_ru_${role}.pdf"
  
  # Combine with pandoc
  pandoc "$COMMON" "$PAGE3" -o "$OUTPUT" --pdf-engine=xelatex \
    -V geometry:margin=1.5cm -V fontsize=11pt -V mainfont="DejaVu Serif" \
    -V colorlinks=true 2>/dev/null || \
  pandoc "$COMMON" "$PAGE3" -o "$OUTPUT" --pdf-engine=pdflatex \
    -V geometry:margin=1.5cm 2>/dev/null || \
  echo "Failed: $role"
  
  echo "Created: $OUTPUT"
done

echo "Done!"
ls -la "$OUTDIR"
