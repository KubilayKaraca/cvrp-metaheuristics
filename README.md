<!-- Origin: written by Claude (AI). See ai_usage.md, Section 5. -->
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

## Benchmarks (CVRPLIB Set A) – parser check

The four benchmark instances and their best-known solutions are in `instances/`
(`A-n32-k5`, `A-n45-k6`, `A-n60-k9`, `A-n80-k10`, each as `.vrp` and `.sol`).

- `src/cvrplib.py` reads `.vrp` and `.sol` files and builds the distance matrix:
  CVRPLIB instances (`EUC_2D`) use Euclidean distances rounded to the nearest integer;
  our MediDrone instance (`EUC_2D_BOSPHORUS`) uses real-valued Euclidean distances
  + 150 between the European (x < 500) and Asian (x ≥ 500) sides.
- `src/evaluation.py` computes the cost of a route and of a solution.

Run the checks (works from any folder):

```bash
python scripts/test_cvrplib.py
```

For each benchmark it checks n, Q, K, the depot demand, the distance matrix (zero diagonal,
symmetric) and the best-known solution (K routes, capacity, every customer exactly once), and
compares our cost with the `.sol` file (784, 944, 1354, 1763). It also checks the MediDrone
instance (n = 100, Q = 100, K = 18, Bosphorus penalty). Expected last line:
`Tüm benchmark ve MediDrone kontrolleri başarıyla geçti.`

## Project layout

```
team.json            team members and student IDs (seed source)
src/                 Python source code
  cvrplib.py         CVRPLIB/TSPLIB reader (.vrp, .sol) and distance matrix
  evaluation.py      route cost and total cost of a solution
  distances.py       MediDrone distance (Euclidean + Bosphorus penalty)
instances/           CVRPLIB benchmarks (.vrp, .sol) and our MediDrone instance
figures/             plots
report/m1/           Milestone 1 report (LaTeX)
scripts/             build scripts and tests (test_cvrplib.py)
ai_usage.md          log of AI-tool usage (for Appendix B)
```

Planned next: feasibility checker, Clarke–Wright, Tabu Search, GA with Split,
experiment scripts.
