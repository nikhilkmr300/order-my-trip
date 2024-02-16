from itertools import permutations

from matrices import build_matrices


def tsp_brute_force(graph):
    def calc_cost(path):
        cost = 0
        for loc1, loc2 in zip(path, path[1:]):
            cost += graph.loc[loc1, loc2]
        return cost

    assert all(graph.index == graph.columns)
    locs = graph.index

    min_cost, min_path = float("inf"), None
    for path in permutations(locs):
        path = path + (path[0],)     # return to original city
        cost = calc_cost(path)
        if cost < min_cost:
            min_cost, min_path = cost, path

    return min_cost, min_path


if __name__ == "__main__":
    locs = ["New York", "Los Angeles", "Philadelphia", "Seattle", "Austin"]

    distances, times = build_matrices(locs)

    print(distances)

    print(tsp_brute_force(distances))
