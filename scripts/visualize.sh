#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

# Render the latest saved cameleon model using its saved training configuration.
# Images are written to output/cameleon/train/ours_<iteration>/renders/.
# Extra render.py options can be supplied, e.g. --iteration 7000.
cd "${REPO_ROOT}"
exec python "${REPO_ROOT}/render.py" \
    -s "${REPO_ROOT}/data/cameleon" \
    -m "${REPO_ROOT}/output/cameleon" \
    "$@"
