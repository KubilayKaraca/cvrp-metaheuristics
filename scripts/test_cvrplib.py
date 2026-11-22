# Origin: own code (Kubilay Karaca)

import math
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.cvrplib import build_distance_matrix, parse_sol, parse_vrp
from src.evaluation import route_cost, total_cost

INSTANCES_DIR = PROJECT_ROOT / "instances"

EXPECTED_BENCHMARKS = {
    "A-n32-k5": (31, 100, 5),
    "A-n45-k6": (44, 100, 6),
    "A-n60-k9": (59, 100, 9),
    "A-n80-k10": (79, 100, 10),
}


def check_distance_matrix(dist):
    size = len(dist)
    for i in range(size):
        assert dist[i][i] == 0, f"Köşegen 0 değil: dist[{i}][{i}] = {dist[i][i]}"
        for j in range(i + 1, size):
            assert math.isclose(dist[i][j], dist[j][i], rel_tol=0.0, abs_tol=1e-12), (
                f"Matris simetrik değil: dist[{i}][{j}]={dist[i][j]} != dist[{j}][{i}]={dist[j][i]}"
            )


def check_benchmark(name, expected_n, expected_q, expected_k):
    vrp_path = INSTANCES_DIR / f"{name}.vrp"
    sol_path = INSTANCES_DIR / f"{name}.sol"

    inst = parse_vrp(vrp_path)
    assert inst.n == expected_n, f"{name}: n={inst.n}, beklenen {expected_n}"
    assert inst.Q == expected_q, f"{name}: Q={inst.Q}, beklenen {expected_q}"
    assert inst.K == expected_k, f"{name}: K={inst.K}, beklenen {expected_k}"
    assert inst.demands[0] == 0, f"{name}: Deponun talebi 0 olmalı"

    dist = build_distance_matrix(
        inst.coords,
        edge_weight_type=inst.edge_weight_type,
        strait_x=inst.strait_x,
        crossing_penalty=inst.crossing_penalty,
    )
    check_distance_matrix(dist)

    routes, sol_cost = parse_sol(sol_path)
    assert len(routes) == inst.K, f"{name}: rota sayısı {len(routes)}, beklenen {inst.K}"

    visited = []
    for idx, route in enumerate(routes, start=1):
        load = sum(inst.demands[c] for c in route)
        assert load <= inst.Q, f"{name} Rota #{idx}: yük {load} > Q ({inst.Q})"
        visited.extend(route)

    assert len(visited) == inst.n and sorted(visited) == list(range(1, inst.n + 1)), (
        f"{name}: her müşteri tam bir kez ziyaret edilmeli"
    )

    computed = total_cost(routes, dist)
    print(f"{name}: n={inst.n}, Q={inst.Q}, K={inst.K} | computed={computed} vs sol={sol_cost}")
    assert math.isclose(computed, sol_cost, rel_tol=0.0, abs_tol=1e-6), (
        f"{name}: maliyet uyuşmadı ({computed} != {sol_cost})"
    )

    
    if name == "A-n32-k5":
        assert dist[0][1] == 35, f"A-n32-k5 d(0,1)={dist[0][1]}, beklenen 35"
        assert dist[1][2] == 60, f"A-n32-k5 d(1,2)={dist[1][2]}, beklenen 60"
        sample_route = [1, 2]
        expected_sample = dist[0][1] + dist[1][2] + dist[2][0]
        assert route_cost(sample_route, dist) == expected_sample


def check_medidrone():
    vrp_path = INSTANCES_DIR / "medidrone_s19409.vrp"
    inst = parse_vrp(vrp_path)

    assert inst.n == 100, f"MediDrone n={inst.n}, beklenen 100"
    assert inst.Q == 100, f"MediDrone Q={inst.Q}, beklenen 100"
    assert inst.K == 18, f"MediDrone K={inst.K}, beklenen 18"
    assert inst.demands[0] == 0, "MediDrone depo talebi 0 olmalı"
    assert inst.edge_weight_type == "EUC_2D_BOSPHORUS"

    dist = build_distance_matrix(
        inst.coords,
        edge_weight_type=inst.edge_weight_type,
        strait_x=inst.strait_x,
        crossing_penalty=inst.crossing_penalty,
    )
    check_distance_matrix(dist)

   
    euro_customer = next(i for i in range(1, inst.n + 1) if inst.coords[i][0] < inst.strait_x)
    x0, y0 = inst.coords[0]
    xe, ye = inst.coords[euro_customer]
    expected_eu_dist = math.hypot(x0 - xe, y0 - ye) + inst.crossing_penalty
    assert math.isclose(dist[0][euro_customer], expected_eu_dist, rel_tol=0.0, abs_tol=1e-9), (
        f"MediDrone Boğaz mesafesi hatalı: {dist[0][euro_customer]} != {expected_eu_dist}"
    )

    
    asia_customer = next(i for i in range(1, inst.n + 1) if inst.coords[i][0] >= inst.strait_x)
    xa, ya = inst.coords[asia_customer]
    expected_as_dist = math.hypot(x0 - xa, y0 - ya)
    assert math.isclose(dist[0][asia_customer], expected_as_dist, rel_tol=0.0, abs_tol=1e-9), (
        f"MediDrone Asya içi mesafe hatalı: {dist[0][asia_customer]} != {expected_as_dist}"
    )

    print(
        f"medidrone_s19409: n={inst.n}, Q={inst.Q}, K={inst.K} | "
        f"d(0,{euro_customer})={dist[0][euro_customer]:.2f} (Avrupa), "
        f"d(0,{asia_customer})={dist[0][asia_customer]:.2f} (Asya)"
    )


if __name__ == "__main__":
    for name, (exp_n, exp_q, exp_k) in EXPECTED_BENCHMARKS.items():
        check_benchmark(name, exp_n, exp_q, exp_k)
    check_medidrone()
    print("Tüm benchmark ve MediDrone kontrolleri başarıyla geçti.")