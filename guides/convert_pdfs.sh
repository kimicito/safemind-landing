#!/bin/bash
# Convert all guides to PDF

cd /root/.openclaw/workspace/safemind/guides
mkdir -p ../pdfs

for lang in ru en es; do
  for role in marketing hr teacher legal finance transport procurement economist; do
    input="${lang}_${role}.md"
    output="../pdfs/safemind_survival_guide_${lang}_${role}.pdf"
    if [ -f "$input" ]; then
      pandoc "$input" -o "$output" --pdf-engine=xelatex -V geometry:margin=1.5cm -V fontsize=11pt -V mainfont="DejaVu Serif" 2>/dev/null || \
      pandoc "$input" -o "$output" --pdf-engine=pdflatex -V geometry:margin=1.5cm 2>/dev/null || \
      echo "Failed: $input"
      echo "Created: $output"
    fi
  done
done

echo "Done!"
ls -la ../pdfs/
