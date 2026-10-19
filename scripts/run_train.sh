#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

# Train on the undistorted cameleon dataset; save results under output/cameleon.
# Additional train.py options can be supplied, e.g. --iterations 7000 --eval.
cd "${REPO_ROOT}"
exec python "${REPO_ROOT}/train.py" \
    -s "${REPO_ROOT}/data/cameleon_random" \
    -m "${REPO_ROOT}/output/cameleon_random_50" \
    "$@"
