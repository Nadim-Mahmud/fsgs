#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

# Evaluate the cameleon_256_256 model against its own 256x256 source images.
# The model receives test renders, results.json, and per_view.json.
cd "${REPO_ROOT}"
model_dir="${REPO_ROOT}/output/cameleon_256_256"
if [[ ! -f "${model_dir}/cfg_args" || ! -f "${model_dir}/point_cloud/iteration_30000/point_cloud.ply" ]]; then
    echo "No completed iteration 30000 model in ${model_dir}"
    exit 1
fi

echo "Evaluating cameleon_256_256"
python "${REPO_ROOT}/render.py" \
    -s "${REPO_ROOT}/data/cameleon_masked/cameleon" \
    -i "${REPO_ROOT}/data/cameleon_masked/cameleon/images" \
    -m "${model_dir}" \
    --eval --iteration 30000 --skip_train

echo "Render complete. Calculating PSNR, SSIM, and LPIPS."
python "${REPO_ROOT}/metrics.py" -m "${model_dir}"
