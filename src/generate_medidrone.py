# Origin: written by Claude (AI). See ai_usage.md, Section 5.
"""Generate the team-specific MediDrone CVRP instance (Task 2b).

Rules from the project text:
  * 1000 x 1000 square, depot in the centre (500, 500)
  * European side x < 500, Asian side x >= 500
  * n = 100 customers: 4-6 clusters spread over both sides + ~20% uniform random
  * demands q_i uniform integers in [1, 30], capacity Q = 100,
    K = ceil(sum q_i / Q) + 1
  * d(i, j) = Euclidean + 150 if i and j are on different sides

Reproducibility: every random number comes from random.Random(seed).random().
Python guarantees that random() gives the same sequence for the same seed in
every Python version (other helpers such as gauss/randint are not guaranteed),
so uniform, integer and normal draws are built from random() by hand.

Usage:  python src/generate_medidrone.py [team.json] [output_dir]
"""
import json
import math
import random
import sys
from pathlib import Path

from team_seed import load_team, team_seed

SIZE = 1000
DEPOT = (500, 500)
STRAIT_X = 500
PENALTY = 150
N_CUSTOMERS = 100
RANDOM_SHARE = 0.20
CAPACITY = 100
DEMAND_MIN, DEMAND_MAX = 1, 30

# cluster layout parameters (our own choices, reported in M1)
CENTER_X_RANGE = {"EU": (120, 400), "AS": (600, 880)}
CENTER_Y_RANGE = (120, 880)
MIN_CENTER_GAP = 220
SIGMA_RANGE = (35, 60)


class Rng:
    """Thin wrapper: all draws derived from random.random()."""

    def __init__(self, seed):
        self._r = random.Random(seed)

    def u(self):
        return self._r.random()                      # [0, 1)

    def uniform(self, a, b):
        return a + (b - a) * self.u()

    def randint(self, a, b):                          # inclusive
        return a + int(self.u() * (b - a + 1))

    def normal(self):                                 # Box-Muller
        u1 = 1.0 - self.u()                           # (0, 1]
        u2 = self.u()
        return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)

    def shuffle(self, items):                         # Fisher-Yates
        for i in range(len(items) - 1, 0, -1):
            j = int(self.u() * (i + 1))
            items[i], items[j] = items[j], items[i]


def side_of(x):
    return "EU" if x < STRAIT_X else "AS"


def first_fit_decreasing(demands, capacity):
    """Number of vehicles FFD needs (feasibility sanity check)."""
    loads = []
    for q in sorted(demands, reverse=True):
        for b in range(len(loads)):
            if loads[b] + q <= capacity:
                loads[b] += q
                break
        else:
            loads.append(q)
    return len(loads)


def generate(seed, n=N_CUSTOMERS):
    rng = Rng(seed)
    used = {DEPOT}

    # 1) number of clusters and their sides (alternating -> both sides covered)
    m = rng.randint(4, 6)
    first = "EU" if rng.u() < 0.5 else "AS"
    other = "AS" if first == "EU" else "EU"
    sides = [first if c % 2 == 0 else other for c in range(m)]

    # 2) cluster centres, kept at least MIN_CENTER_GAP apart (rejection sampling)
    centers = []
    for s in sides:
        for _ in range(10_000):
            cx = rng.uniform(*CENTER_X_RANGE[s])
            cy = rng.uniform(*CENTER_Y_RANGE)
            if all(math.dist((cx, cy), c) >= MIN_CENTER_GAP for c in centers):
                break
        else:
            raise RuntimeError("could not place cluster centres far enough apart")
        centers.append((cx, cy))
    sigmas = [rng.uniform(*SIGMA_RANGE) for _ in range(m)]

    # 3) customer counts: 20% random, the rest split as evenly as possible
    n_random = round(RANDOM_SHARE * n)
    n_clustered = n - n_random
    sizes = [n_clustered // m + (1 if c < n_clustered % m else 0) for c in range(m)]

    customers = []  # (x, y, cluster_id) ; cluster_id = -1 for random customers
    for c, (size, (cx, cy), sig, s) in enumerate(zip(sizes, centers, sigmas, sides)):
        placed = 0
        while placed < size:
            x = round(cx + sig * rng.normal())
            y = round(cy + sig * rng.normal())
            # keep the point inside the square, on its cluster's side, unique
            if not (0 <= x <= SIZE and 0 <= y <= SIZE):
                continue
            if side_of(x) != s or (x, y) in used:
                continue
            used.add((x, y))
            customers.append((x, y, c))
            placed += 1

    placed = 0
    while placed < n_random:
        x, y = rng.randint(0, SIZE), rng.randint(0, SIZE)
        if (x, y) in used:
            continue
        used.add((x, y))
        customers.append((x, y, -1))
        placed += 1

    # 4) shuffle so that customer numbers do not reveal the cluster structure
    rng.shuffle(customers)

    # 5) demands, capacity and fleet size
    demands = [rng.randint(DEMAND_MIN, DEMAND_MAX) for _ in customers]
    total = sum(demands)
    lower_bound = math.ceil(total / CAPACITY)
    K = lower_bound + 1

    return {
        "name": f"MediDrone-s{seed}",
        "seed": seed,
        "n": n,
        "capacity": CAPACITY,
        "vehicles": K,
        "vehicle_lower_bound": lower_bound,
        "ffd_vehicles": first_fit_decreasing(demands, CAPACITY),
        "strait_x": STRAIT_X,
        "crossing_penalty": PENALTY,
        "depot": list(DEPOT),
        "customers": [{"id": i + 1, "x": x, "y": y, "demand": q,
                       "cluster": c, "side": side_of(x)}
                      for i, ((x, y, c), q) in enumerate(zip(customers, demands))],
        "clusters": [{"id": c, "side": s, "center": [round(cx, 1), round(cy, 1)],
                      "sigma": round(sg, 1), "size": sz}
                     for c, (s, (cx, cy), sg, sz)
                     in enumerate(zip(sides, centers, sigmas, sizes))],
        "total_demand": total,
    }


def write_vrp(inst, path):
    """CVRPLIB-style file. Node 1 = depot (CVRPLIB numbering is 1-based)."""
    lines = [
        f"NAME : {inst['name']}",
        f"COMMENT : CMP3005 MediDrone team instance, seed {inst['seed']}; "
        f"d = Euclidean + {inst['crossing_penalty']} if sides differ "
        f"(EU: x < {inst['strait_x']}, AS: x >= {inst['strait_x']}); no rounding",
        "TYPE : CVRP",
        f"DIMENSION : {inst['n'] + 1}",
        "EDGE_WEIGHT_TYPE : EUC_2D_BOSPHORUS",
        f"CAPACITY : {inst['capacity']}",
        f"VEHICLES : {inst['vehicles']}",
        f"STRAIT_X : {inst['strait_x']}",
        f"CROSSING_PENALTY : {inst['crossing_penalty']}",
        "NODE_COORD_SECTION",
        f"1 {inst['depot'][0]} {inst['depot'][1]}",
    ]
    lines += [f"{c['id'] + 1} {c['x']} {c['y']}" for c in inst["customers"]]
    lines.append("DEMAND_SECTION")
    lines.append("1 0")
    lines += [f"{c['id'] + 1} {c['demand']}" for c in inst["customers"]]
    lines += ["DEPOT_SECTION", "1", "-1", "EOF"]
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    team_file = sys.argv[1] if len(sys.argv) > 1 else "team.json"
    out_dir = Path(sys.argv[2] if len(sys.argv) > 2 else "instances")
    out_dir.mkdir(parents=True, exist_ok=True)

    team = load_team(team_file)
    seed, terms = team_seed(team["members"], team.get("seed_mode", "last4_number"))
    inst = generate(seed)
    inst["seed_terms"] = terms

    stem = f"medidrone_s{seed}"
    write_vrp(inst, out_dir / f"{stem}.vrp")
    (out_dir / f"{stem}.json").write_text(json.dumps(inst, indent=1), encoding="utf-8")
    (out_dir / "medidrone_current.txt").write_text(stem + "\n", encoding="utf-8")

    eu = sum(c["side"] == "EU" for c in inst["customers"])
    print(f"seed {seed}: {len(inst['clusters'])} clusters, EU {eu} / AS {inst['n'] - eu}, "
          f"total demand {inst['total_demand']}, K = {inst['vehicles']} "
          f"(lower bound {inst['vehicle_lower_bound']}, FFD {inst['ffd_vehicles']})")
    print(f"written: {out_dir / (stem + '.vrp')}")
