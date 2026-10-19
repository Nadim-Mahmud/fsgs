#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

# Train on cameleon with the live SIBR viewer accessible through Docker.
# Dataset, output, and viewer connection defaults are supplied below.
# Additional train.py options can be supplied, e.g. --iterations 7000 --eval.
cd "${REPO_ROOT}"
exec python "${REPO_ROOT}/train.py" \
    -s "${REPO_ROOT}/data/cameleon" \
    -m "${REPO_ROOT}/output/cameleon" \
    --ip 0.0.0.0 \
    --port 6009 \
    "$@"
