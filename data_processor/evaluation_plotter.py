import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


repo_root = Path(__file__).resolve().parents[1]
input_dir = repo_root / "output/cameleon_rand_drop"

percentages = []
psnr = []
ssim = []
lpips = []

for percent in range(5, 101, 5):
    report = input_dir / f"drop_{percent}/results.json"
    if not report.exists():
        continue

    with open(report) as file:
        results = json.load(file)["ours_30000"]

    percentages.append(percent)
    psnr.append(results["PSNR"])
    ssim.append(results["SSIM"])
    lpips.append(results["LPIPS"])

fig, axes = plt.subplots(1, 3, figsize=(24, 7))

for ax, values, label, color in zip(
    axes, [psnr, ssim, lpips],
    ["PSNR (dB) — higher is better", "SSIM — higher is better", "LPIPS — lower is better"],
    ["tab:blue", "tab:green", "tab:red"],
):
    ax.plot(percentages, values, marker="o", color=color)
    ax.set_xlabel("Pixel dropout (%)", fontsize=14)
    ax.set_ylabel(label, fontsize=14)
    ax.set_xticks(range(5, 101, 5))
    ax.tick_params(axis="x", labelrotation=45)
    ax.grid(alpha=0.3)

fig.suptitle("Evaluation results vs pixel dropout (iteration 30000)", fontsize=20)
plt.tight_layout()
plt.savefig(repo_root / "output/evaluation_plot.png", dpi=200)
plt.savefig(repo_root / "output/evaluation_plot.pdf")
plt.close()
