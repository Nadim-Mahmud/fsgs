#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

# Evaluate all completed dropout models against the original cameleon images.
# Each model receives test renders, results.json, and per_view.json.
cd "${REPO_ROOT}"
rendered_models=()
for ((percent = 5; percent <= 100; percent += 5)); do
    model_dir="${REPO_ROOT}/output/cameleon_rand_drop/drop_${percent}"
    if [[ ! -f "${model_dir}/cfg_args" || ! -f "${model_dir}/point_cloud/iteration_30000/point_cloud.ply" ]]; then
        echo "Skipping drop_${percent}: no completed iteration 30000 model"
        continue
    fi

    echo "Evaluating ${percent}% dropout against original images"
    python "${REPO_ROOT}/render.py" \
        -s "${REPO_ROOT}/data/cameleon" \
        -i "${REPO_ROOT}/data/cameleon/images" \
        -m "${model_dir}" \
        --eval --iteration 30000 --skip_train
    rendered_models+=("${model_dir}")
done

if (( ${#rendered_models[@]} > 0 )); then
    echo "All renders complete. Calculating PSNR, SSIM, and LPIPS."
    python "${REPO_ROOT}/metrics.py" -m "${rendered_models[@]}"
fi
