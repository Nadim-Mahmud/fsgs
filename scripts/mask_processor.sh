#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
DATASET="${REPO_ROOT}/data/cameleon_masked"
INPUT_DIR="${DATASET}/original_masks"
OUTPUT_DIR="${DATASET}/projected_masks"
MODEL_DIR="${DATASET}/cameleon/distorted/sparse/0"

# Use the same reconstruction and undistortion options as the training images.
# Mask filenames and original dimensions must match the reconstruction inputs.
if [[ ! -d "${MODEL_DIR}" ]]; then
    echo "Missing distorted reconstruction: ${MODEL_DIR}" >&2
    exit 1
fi

mkdir -p "${OUTPUT_DIR}"
shopt -s nullglob
mask_sets=("${INPUT_DIR}"/*/)
if (( ${#mask_sets[@]} == 0 )); then
    echo "No mask sets found under ${INPUT_DIR}" >&2
    exit 1
fi

for mask_dir in "${mask_sets[@]}"; do
    set_name="$(basename -- "${mask_dir}")"
    echo "Undistorting ${set_name}"
    colmap image_undistorter \
        --image_path "${mask_dir}" \
        --input_path "${MODEL_DIR}" \
        --output_path "${OUTPUT_DIR}/${set_name}" \
        --output_type COLMAP \
        --max_image_size -1
done
