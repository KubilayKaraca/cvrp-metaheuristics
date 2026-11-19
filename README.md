# medidrone-cvrp

CMP3005 Term Project – Capacitated Vehicle Routing Problem (CVRP) for MediDrone Istanbul:
Clarke–Wright savings, Genetic Algorithm (giant tour + Split) and Tabu Search, evaluated on
CVRPLIB benchmarks and on our own team instance.

## Requirements

- Python 3.10+ with `numpy` and `matplotlib` (`pip install -r requirements.txt`)
- A LaTeX distribution with `latexmk` (only needed to build the PDF report)

## Milestone 1 – rebuild everything with one command

1. Put the real names and student IDs in `team.json` and set `"placeholder": false`.
2. Run:

```bash
bash scripts/build_m1.sh
```

This runs, in order:

| Step | Script | Output |
|---|---|---|
| Team seed | `src/team_seed.py` | printed seed calculation |
| Instance generation | `src/generate_medidrone.py` | `instances/medidrone_s<seed>.vrp` (+ `.json`) |
| Triangle-inequality check | `src/check_metric.py` | `instances/medidrone_s<seed>_metric.json` |
| Instance map | `src/plot_instance.py` | `figures/medidrone_instance.pdf/.png` |
| Report numbers | `src/m1_values.py` | `report/m1/values.tex` |
| Report | `report/m1/m1.tex` | `report/m1/m1.pdf` |

Seed rule: `seed_mode` in `team.json` is `last4_number` (1234 → 1234, default) or
`last4_digits` (1234 → 1+2+3+4).

## Project layout

```
team.json            team members and student IDs (seed source)
src/                 Python source code
  distances.py       MediDrone distance (Euclidean + Bosphorus penalty)
instances/           generated / downloaded instances (.vrp)
figures/             plots
report/m1/           Milestone 1 report (LaTeX)
scripts/             build scripts
ai_usage.md          log of AI-tool usage (for Appendix B)
```

Planned next: CVRPLIB parser, feasibility checker, Clarke–Wright, Tabu Search, GA with Split,
experiment scripts.
