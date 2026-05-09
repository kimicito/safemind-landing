#!/bin/bash
# Convert combined guides to DOCX

COMMON="/root/.openclaw/workspace/safemind/free_guides/ru_common_pages.md"
OUTDIR="/root/.openclaw/workspace/safemind/free_docx"
mkdir -p "$OUTDIR"

for role in marketing hr teacher legal finance transport procurement economist; do
  PAGE3="/root/.openclaw/workspace/safemind/free_guides/ru_${role}_page3.md"
  OUTPUT="$OUTDIR/safemind_free_guide_ru_${role}.docx"
  
  pandoc "$COMMON" "$PAGE3" -o "$OUTPUT" 2>/dev/null || echo "Failed: $role"
  echo "Created: $OUTPUT"
done

echo "Done!"
ls -la "$OUTDIR"
