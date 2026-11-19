# Origin: written by Claude (AI). See ai_usage.md, Section 5.
"""Plot the MediDrone instance (Milestone 1 figure).

Colour encodes the side of the strait (European / Asian); filled markers are
clustered customers, hollow markers are the uniformly random ones; marker area
grows with demand. Cluster labels C1..Cm sit next to the cluster centres.

Usage:  python src/plot_instance.py [instances_dir] [figures_dir]
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

EU_COLOR = "#2a78d6"     # categorical slot 1 (blue)
AS_COLOR = "#eb6834"     # categorical slot 2 (orange)
INK = "#1f1f1e"
MUTED = "#6b6a63"
GRID = "#e4e3dd"


def marker_size(q):
    return 10 + 2.2 * q          # area in pt^2, demand 1..30 -> 12..76


def plot(inst, out_stem):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    fig, ax = plt.subplots(figsize=(6.4, 6.0))

    sx = inst["strait_x"]
    ax.axvspan(-20, sx, color=EU_COLOR, alpha=0.04, lw=0)
    ax.axvspan(sx, 1020, color=AS_COLOR, alpha=0.04, lw=0)
    ax.axvline(sx, color=MUTED, lw=1.2, ls=(0, (5, 3)), zorder=1)
    ax.text(sx + 10, 800, f"Bosphorus (x = {sx})", color=MUTED, va="center",
            ha="left", rotation=90, fontsize=8)
    ax.text(15, 985, "European side (x < 500)", color=MUTED, fontsize=8, va="top")
    ax.text(985, 985, "Asian side (x ≥ 500)", color=MUTED, fontsize=8, va="top",
            ha="right")

    for c in inst["customers"]:
        color = EU_COLOR if c["side"] == "EU" else AS_COLOR
        clustered = c["cluster"] >= 0
        ax.scatter(c["x"], c["y"], s=marker_size(c["demand"]),
                   facecolor=color if clustered else "white",
                   edgecolor="white" if clustered else color,
                   linewidth=0.8 if clustered else 1.4, zorder=3)

    # cluster label next to its cluster, at the first candidate spot with no
    # customer marker underneath (above, below, left, right of the cluster)
    dx0, dy0 = inst["depot"]
    pts = [(c["x"], c["y"]) for c in inst["customers"]] + [(dx0, dy0)]
    pts += [(dx0 + o, dy0 + 40) for o in range(-120, 121, 20)]   # depot label
    pts += [(sx + 18, y) for y in range(700, 901, 20)]          # Bosphorus label
    for cl in inst["clusters"]:
        members = [c for c in inst["customers"] if c["cluster"] == cl["id"]]
        xs = sorted(c["x"] for c in members)
        mx = xs[len(xs) // 2]
        top = max(c["y"] for c in members)
        bottom = min(c["y"] for c in members)
        cy = cl["center"][1]
        candidates = [(mx, top + 40), (max(xs) + 45, cy),
                      (min(xs) - 45, cy), (mx, bottom - 40)]
        candidates = [(x, y) for x, y in candidates if 30 < x < 970 and 30 < y < 960]

        def clearance(p):
            return min(((p[0] - x) ** 2 + ((p[1] - y) * 1.4) ** 2) ** 0.5 for x, y in pts)

        lx, ly = next((p for p in candidates if clearance(p) > 42),
                      max(candidates, key=clearance))
        pts.append((lx, ly))                                      # keep labels apart
        ax.text(lx, ly, f"C{cl['id'] + 1}", ha="center", va="center", fontsize=8.5,
                color=INK, fontweight="bold", zorder=4)

    dx, dy = inst["depot"]
    ax.scatter(dx, dy, marker="*", s=260, color=INK, edgecolor="white",
               linewidth=1.0, zorder=5)
    ax.text(dx, dy + 26, "Depot (central lab)", ha="center", va="bottom",
            fontsize=8, color=INK, zorder=5,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.85))

    ax.set_xlim(-20, 1020)      # small margin so points on the border stay visible
    ax.set_ylim(-20, 1020)
    ax.set_aspect("equal")
    ax.set_xticks(range(0, 1001, 250))
    ax.set_yticks(range(0, 1001, 250))
    ax.grid(color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_color(GRID)
    ax.tick_params(colors=MUTED, length=0)
    ax.set_xlabel("x", color=MUTED)
    ax.set_ylabel("y", color=MUTED)

    eu = sum(c["side"] == "EU" for c in inst["customers"])
    ax.set_title(f"MediDrone instance (seed {inst['seed']}): n = {inst['n']}, "
                 f"Σq = {inst['total_demand']}, Q = {inst['capacity']}, "
                 f"K = {inst['vehicles']}", color=INK, fontsize=10, loc="left")

    handles = [
        Line2D([], [], marker="o", ls="", markerfacecolor=EU_COLOR, markeredgecolor=EU_COLOR,
               markersize=7, label=f"European customer ({eu})"),
        Line2D([], [], marker="o", ls="", markerfacecolor=AS_COLOR, markeredgecolor=AS_COLOR,
               markersize=7, label=f"Asian customer ({inst['n'] - eu})"),
        Line2D([], [], marker="o", ls="", markerfacecolor="white", markeredgecolor=MUTED,
               markeredgewidth=1.4, markersize=7, label="hollow = uniform random"),
        Line2D([], [], marker="*", ls="", color=INK, markersize=12, label="Depot"),
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.09), ncol=2,
              frameon=False, fontsize=8, handletextpad=0.4, columnspacing=1.6)
    fig.text(0.99, 0.005, "marker area ∝ demand", ha="right", fontsize=7, color=MUTED)

    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(f"{out_stem}.{ext}", dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    inst_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "instances")
    fig_dir = Path(sys.argv[2] if len(sys.argv) > 2 else "figures")
    fig_dir.mkdir(parents=True, exist_ok=True)
    stem = (inst_dir / "medidrone_current.txt").read_text().strip()
    inst = json.loads((inst_dir / f"{stem}.json").read_text())
    plot(inst, fig_dir / "medidrone_instance")
    print(f"written: {fig_dir / 'medidrone_instance.pdf'} (+ .png)")
