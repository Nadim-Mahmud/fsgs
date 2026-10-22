#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

# Train all Tanks and Temples and Deep Blending scenes in tandt_db_30.
# Save each scene under output/tandt_db_30/<dataset>/<scene>.
# Additional train.py options can be supplied, e.g. --iterations 7000 --eval.
cd "${REPO_ROOT}"
for scene in tandt/train tandt/truck db/drjohnson db/playroom; do
    echo "Training ${scene}"
    python "${REPO_ROOT}/train.py" \
        -s "${REPO_ROOT}/data/tandt_db_30/${scene}" \
        -m "${REPO_ROOT}/output/tandt_db_30/${scene}" \
        "$@"
done
