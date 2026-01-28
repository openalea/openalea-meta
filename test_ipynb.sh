#!/usr/bin/env bash
#set -euo pipefail
export QT_QPA_PLATFORM=offscreen
DIRS=(
  mtg/example
  oawidgets/doc/examples
  rsml/example
  PyRATP/example
  caribu/doc/notebook
  astk/doc/notebooks
  adel/doc/example/notebook
  spice/doc/examples/plantgl-rad-scene
  hydroroot/example
  phenomenal/doc/examples
  hydroshoot/example/potted_grapevine
  WheatFspm/example/Notebooks
)

for dir in "${DIRS[@]}"; do
  echo "▶ Running notebooks in $dir"

  if [ -d "$dir" ]; then
    (
      cd "$dir"
      echo "***** $dir ******"
      pytest --nbmake *.ipynb
    )
  else
    echo "⚠ Directory not found: $dir"
  fi
done
