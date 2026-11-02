#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"
shopt -s nullglob

# Use cameleon's cameras with each masked-image set.
for mask_dir in "${REPO_ROOT}"/data/cameleon_masked/masked_256_256/view*/images; do
    set_name="$(basename -- "$(dirname -- "${mask_dir}")")"
    echo "Training ${set_name}"
    python "${REPO_ROOT}/train.py" \
        -s "${REPO_ROOT}/data/cameleon_masked/cameleon" \
        -i "${mask_dir}" \
        -m "${REPO_ROOT}/output/cameleon_masked/${set_name}" \
        --iteration_report_suffix with_mask \
        "$@"
done
