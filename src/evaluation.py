# Origin: own code (Kubilay Karaca)


def route_cost(route, dist):
    """Tek bir rotanın (0 -> c1 -> ... -> ck -> 0) toplam mesafesini hesaplar."""
    if not route:
        return 0
    cost = dist[0][route[0]]
    for k in range(len(route) - 1):
        cost += dist[route[k]][route[k + 1]]
    cost += dist[route[-1]][0]
    return cost



def total_cost(routes, dist):
    """Tüm rotaların toplam maliyetini hesaplar."""
    return sum(route_cost(r, dist) for r in routes)