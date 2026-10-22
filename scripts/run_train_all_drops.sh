#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

# Use cameleon's reconstruction with each dropped-image folder as loss targets.
# Save each run separately and train sequentially from 5% through 100%.
# Additional train.py options can be supplied, e.g. --iterations 7000 --eval.
cd "${REPO_ROOT}"
for ((percent = 5; percent <= 100; percent += 5)); do
    images_dir="${REPO_ROOT}/data/cameleon_rand_drop/drop_${percent}"
    if [[ ! -d "${images_dir}" ]]; then
        echo "Missing image folder: ${images_dir}" >&2
        exit 1
    fi
done

for ((percent = 5; percent <= 100; percent += 5)); do
    echo "Training cameleon with ${percent}% pixel dropping"
    python "${REPO_ROOT}/train.py" \
        -s "${REPO_ROOT}/data/cameleon" \
        -i "${REPO_ROOT}/data/cameleon_rand_drop/drop_${percent}" \
        -m "${REPO_ROOT}/output/cameleon_rand_drop/drop_${percent}" \
        "$@"
done
