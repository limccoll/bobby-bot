"""Plot the aggregated Royal Mile wheel-survey results (n = 20 tourists).

Each tourist rated five categories out of 5; scores were summed to a
maximum of 100 per category.
"""
import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).parent


def load(path=HERE / "wheel_survey_totals.csv"):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    return [r["category"] for r in rows], [int(r["score_out_of_100"]) for r in rows]


def main():
    labels, scores = load()
    angles = [2 * math.pi * i / len(labels) for i in range(len(labels))]
    ax = plt.subplot(projection="polar")
    ax.bar(angles, scores, width=2 * math.pi / len(labels) * 0.9, alpha=0.8)
    ax.set_xticks(angles)
    ax.set_xticklabels([f"{l}\n{s}" for l, s in zip(labels, scores)])
    ax.set_ylim(0, 100)
    ax.set_title("What tourists on the Royal Mile want (n = 20)")
    out = HERE.parent / "docs" / "images" / "wheel-totals-chart.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
