import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import time


repo_root = Path(__file__).resolve().parents[1]
input_dir = repo_root / "output/cameleon_masked"

plt.figure(figsize=(26, 15))
colors = plt.get_cmap("tab10")

for index, mask_value in enumerate(["0.025", "0.05", "0.1"]):
    model_dir = input_dir / f"view2image_training_1201_{mask_value}"
    report = model_dir / "iteration_report_with_mask.csv"
    if not report.exists():
        continue

    iterations = []
    counts = []
    with open(report) as file:
        for row in csv.DictReader(file):
            iterations.append(int(row["iteration"]))
            counts.append(int(row["total_points"]))

    final_time = float(row["training_time_s"])
    label = f"Mask {mask_value} — {counts[-1]:,} Gaussians — {final_time / 60:.1f} min"

    results_path = model_dir / "results.json"
    if results_path.exists():
        with open(results_path) as file:
            results = json.load(file)["ours_30000"]

        if "FPS" in results:
            label += f" — {results['FPS']:.1f} FPS"
    
    plt.plot(iterations, counts, label=label, color=colors(index))


timestamp = time.time()

plt.title("Gaussian count during masked-image training", fontsize=24)
plt.xlabel("Iteration", fontsize=18)
plt.ylabel("Number of Gaussians", fontsize=18)
plt.legend(title="Mask / final count / training time / render FPS", bbox_to_anchor=(1.01, 1), loc="upper left")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(repo_root / f"output/gs_count_masked_{int(timestamp)}.png", dpi=200)
plt.savefig(repo_root / f"output/gs_count_masked_{int(timestamp)}.pdf")
plt.close()
