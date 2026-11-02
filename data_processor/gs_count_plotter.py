import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import time


repo_root = Path(__file__).resolve().parents[1]
input_dir = repo_root / "output/cameleon_rand_drop"

plt.figure(figsize=(26, 15))
colors = plt.get_cmap("tab20")

for index, percent in enumerate(range(5, 101, 5)):
    report = input_dir / f"drop_{percent}/iteration_report.csv"
    if not report.exists():
        continue

    iterations = []
    counts = []
    with open(report) as file:
        for row in csv.DictReader(file):
            iterations.append(int(row["iteration"]))
            counts.append(int(row["total_points"]))

    final_time = float(row["training_time_s"])
    label = f"{percent}% — {counts[-1]:,} Gaussians — {final_time / 60:.1f} min"

    results_path = input_dir / f"drop_{percent}/results.json"
    if results_path.exists():
        with open(results_path) as file:
            results = json.load(file)["ours_30000"]

        if "FPS" in results:
            label += f" — {results['FPS']:.1f} FPS"
    
    plt.plot(iterations, counts, label=label, color=colors(index))


timestamp = time.time()

plt.title("Gaussian count during training", fontsize=24)
plt.xlabel("Iteration", fontsize=18)
plt.ylabel("Number of Gaussians", fontsize=18)
plt.legend(title="Pixel dropout / final count / training time / render FPS", bbox_to_anchor=(1.01, 1), loc="upper left")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(repo_root / f"output/gs_count_plot_{int(timestamp)}.png", dpi=200)
plt.savefig(repo_root / f"output/gs_count_plot_{int(timestamp)}.pdf")
plt.close()
