# Origin: written by Claude (AI). See ai_usage.md, Section 5.
"""Numerical check of the triangle inequality on the MediDrone instance (Task 1.4).

Checks two versions of the distance:
  (a) the rule as written: depot (x = 500) belongs to the Asian side
  (b) a "neutral depot" variant: no penalty on any depot edge
      -> expected to violate the triangle inequality (counter-example in M1)
Results are printed and saved to <instance>_metric.json.
"""
import json
import sys
from pathlib import Path

import numpy as np

from distances import distance_matrix, max_triangle_violation, PENALTY, STRAIT_X

if __name__ == "__main__":
    inst_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "instances")
    stem = (inst_dir / "medidrone_current.txt").read_text().strip()
    inst = json.loads((inst_dir / f"{stem}.json").read_text())

    coords = [inst["depot"]] + [[c["x"], c["y"]] for c in inst["customers"]]
    d = distance_matrix(coords)
    worst, count = max_triangle_violation(d)

    # neutral depot: remove the penalty from every depot edge
    d_neutral = d.copy()
    xy = np.asarray(coords, float)
    euclid_from_depot = np.sqrt(((xy - xy[0]) ** 2).sum(axis=1))
    d_neutral[0, :] = euclid_from_depot
    d_neutral[:, 0] = euclid_from_depot
    worst_n, count_n = max_triangle_violation(d_neutral)

    triples = d.shape[0] ** 3
    result = {
        "triples_checked": triples,
        "rule_as_written": {"max_violation": worst, "violating_triples": count},
        "neutral_depot": {"max_violation": worst_n, "violating_triples": count_n},
        "edges_crossing_from_depot": int((xy[1:, 0] < STRAIT_X).sum()),
    }
    (inst_dir / f"{stem}_metric.json").write_text(json.dumps(result, indent=1))
    print(f"checked {triples:,} triples")
    print(f"rule as written : max(d_ik - d_ij - d_jk) = {worst:.6f}, violations = {count}")
    print(f"neutral depot   : max(d_ik - d_ij - d_jk) = {worst_n:.6f}, violations = {count_n}")
