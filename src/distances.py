# Origin: written by Claude (AI). See ai_usage.md, Section 5.
"""Distance function of the MediDrone instance (Task 2b).

d(i, j) = Euclidean(i, j) + P * [i and j lie on different sides of the strait]

Sides: European side x < STRAIT_X, Asian side x >= STRAIT_X.
Note: the depot (500, 500) has x = 500, so by this rule it is on the Asian side.
Distances are kept real-valued (no rounding), because rounding to integers can
break the triangle inequality by up to 1 unit.
"""
import numpy as np

STRAIT_X = 500.0
PENALTY = 150.0


def is_asian(x, strait_x=STRAIT_X):
    return np.asarray(x, dtype=float) >= strait_x


def distance_matrix(coords, penalty=PENALTY, strait_x=STRAIT_X):
    """Full (n+1) x (n+1) matrix; row/column 0 is the depot."""
    xy = np.asarray(coords, dtype=float)
    diff = xy[:, None, :] - xy[None, :, :]
    euclid = np.sqrt((diff ** 2).sum(axis=-1))
    asian = is_asian(xy[:, 0], strait_x)
    crosses = asian[:, None] != asian[None, :]
    return euclid + penalty * crosses


def max_triangle_violation(d):
    """max over all (i, j, k) of d[i,k] - (d[i,j] + d[j,k]).

    The matrix is a metric (w.r.t. the triangle inequality) iff this is <= 0.
    Runs in O(n^3) time but vectorised over i and k.
    Returns (max_violation, number_of_violating_triples).
    """
    worst, count = -np.inf, 0
    for j in range(d.shape[0]):
        slack = d - (d[:, j][:, None] + d[j, :][None, :])
        worst = max(worst, float(slack.max()))
        count += int((slack > 1e-9).sum())
    return worst, count
