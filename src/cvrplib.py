# Origin: own code (Kubilay Karaca)

from dataclasses import dataclass
import math
import re


@dataclass
class VRPInstance:
    name: str
    n: int
    Q: int
    K: int
    coords: list[tuple[float, float]]
    demands: list[int]
    edge_weight_type: str
    strait_x: float = 500.0
    crossing_penalty: float = 150.0


def _parse_vehicle_count(header):
    """K değerini önce VEHICLES başlığından, yoksa COMMENT içindeki 'No of trucks' alanından okur."""
    if "VEHICLES" in header:
        return int(header["VEHICLES"])

    comment = header.get("COMMENT", "")
    match = re.search(r"No of trucks:\s*(\d+)", comment, re.IGNORECASE)
    if match:
        return int(match.group(1))

    name = header.get("NAME", "")
    match = re.search(r"-k(\d+)", name, re.IGNORECASE)
    if match:
        return int(match.group(1))

    raise ValueError("Araç sayısı (K) başlıkta bulunamadı (VEHICLES veya COMMENT eksik).")


def parse_vrp(filepath):
    header = {}
    raw_coords = {}
    raw_demands = {}
    depot_ids = []
    section = None

    with open(filepath, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            if line == "EOF":
                break

            if line in ("NODE_COORD_SECTION", "DEMAND_SECTION", "DEPOT_SECTION"):
                section = line
                continue

            if section is None and ":" in line:
                key, value = line.split(":", 1)
                header[key.strip()] = value.strip()
            elif section == "NODE_COORD_SECTION":
                parts = line.split()
                node_id = int(parts[0])
                raw_coords[node_id] = (float(parts[1]), float(parts[2]))
            elif section == "DEMAND_SECTION":
                parts = line.split()
                node_id = int(parts[0])
                raw_demands[node_id] = int(parts[1])
            elif section == "DEPOT_SECTION":
                val = int(line.split()[0])
                if val == -1:
                    section = None
                else:
                    depot_ids.append(val)

    
    if len(depot_ids) != 1 or depot_ids[0] != 1:
        raise ValueError(f"Beklenen tek depo düğümü 1, bulunan: {depot_ids}")

    dimension = int(header["DIMENSION"])
    capacity = int(header["CAPACITY"])
    k_vehicles = _parse_vehicle_count(header)
    edge_weight_type = header.get("EDGE_WEIGHT_TYPE", "EUC_2D").upper()
    strait_x = float(header.get("STRAIT_X", 500.0))
    crossing_penalty = float(header.get("CROSSING_PENALTY", 150.0))

    
    coords = [None] * dimension
    demands = [None] * dimension

    for node_id, xy in raw_coords.items():
        if not (1 <= node_id <= dimension):
            raise ValueError(f"Koordinat bölümünde geçersiz düğüm numarası: {node_id}")
        coords[node_id - 1] = xy

    for node_id, q in raw_demands.items():
        if not (1 <= node_id <= dimension):
            raise ValueError(f"Talep bölümünde geçersiz düğüm numarası: {node_id}")
        demands[node_id - 1] = q

    missing_coords = [i + 1 for i, c in enumerate(coords) if c is None]
    if missing_coords:
        raise ValueError(f"Eksik koordinatlı düğümler: {missing_coords}")

    missing_demands = [i + 1 for i, q in enumerate(demands) if q is None]
    if missing_demands:
        raise ValueError(f"Eksik talepli düğümler: {missing_demands}")

    return VRPInstance(
        name=header.get("NAME", str(filepath)),
        n=dimension - 1,
        Q=capacity,
        K=k_vehicles,
        coords=coords,
        demands=demands,
        edge_weight_type=edge_weight_type,
        strait_x=strait_x,
        crossing_penalty=crossing_penalty,
    )


def build_distance_matrix(
    coords,
    edge_weight_type="EUC_2D",
    strait_x=500.0,
    crossing_penalty=150.0,
):
    size = len(coords)
    ewt = edge_weight_type.upper()

    if ewt == "EUC_2D":
        dist = [[0] * size for _ in range(size)]
        for i in range(size):
            xi, yi = coords[i]
            for j in range(i + 1, size):
                xj, yj = coords[j]
                d = math.floor(math.hypot(xi - xj, yi - yj) + 0.5)
                dist[i][j] = d
                dist[j][i] = d
        return dist

    if ewt == "EUC_2D_BOSPHORUS":
        dist = [[0.0] * size for _ in range(size)]
        for i in range(size):
            xi, yi = coords[i]
            side_i = xi < strait_x  
            for j in range(i + 1, size):
                xj, yj = coords[j]
                side_j = xj < strait_x
                d = math.hypot(xi - xj, yi - yj)
                if side_i != side_j:
                    d += crossing_penalty
                dist[i][j] = d
                dist[j][i] = d
        return dist

    raise ValueError(f"Desteklenmeyen EDGE_WEIGHT_TYPE: {edge_weight_type}")


def parse_sol(filepath):
    routes = []
    cost = None

    with open(filepath, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("Route"):
                _, nodes_part = line.split(":", 1)
                route = [int(x) for x in nodes_part.split()]
                routes.append(route)
            elif line.startswith("Cost"):
                cost = float(line.split()[-1])

    if cost is None:
        raise ValueError(f"{filepath} dosyasında Cost satırı bulunamadı.")

    return routes, cost