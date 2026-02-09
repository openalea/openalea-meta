#!/usr/bin/env bash
#set -euo pipefail
export QT_QPA_PLATFORM=offscreen
DIRS=(
  plantgl/test
  lpy/test
  core/test
  oawidgets/test
  mtg/test
  scipack/test
  oalab/test
  grapheditor/test
  visualea/test
  weberpenn/test
  rsml/test
  PyRatp/test
  caribu/test
  astk/test
  adel/test
  spice/test
  hydroroot/test
  phenomenal/test
  hydroshoot/test
  WheatFspm/test
)

for dir in "${DIRS[@]}"; do
  echo "▶ Running notebooks in $dir"

  if [ -d "$dir" ]; then
    (
      cd "$dir"
      echo "***** $dir ******"
      pytest test*.py
    )
  else
    echo "⚠ Directory not found: $dir"
  fi
done
