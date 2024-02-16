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


def tsp_dp(graph):
    assert all(graph.index == graph.columns)

    n = graph.shape[0]

    dp = [[None] * 2**n for _ in range(n)]

    def is_all_visited(visited):
        return visited == 2**n - 1

    def is_visited(jLoc, visited):
        return (1 << jLoc) & visited

    def calc_best_cost_from(i_loc, visited):
        if is_all_visited(visited):
            return graph.iloc[i_loc, 0]

        if dp[i_loc][visited] is not None:
            return dp[i_loc][visited][0]

        best_cost_from_here, best_j_loc = float("inf"), None

        for j_loc in range(0, n):
            if i_loc != j_loc and not is_visited(j_loc, visited):
                cost_from_here = graph.iloc[i_loc, j_loc] + calc_best_cost_from(j_loc, visited | 1 << j_loc)
                if cost_from_here < best_cost_from_here:
                    best_cost_from_here = cost_from_here
                    best_j_loc = j_loc

        dp[i_loc][visited] = [best_cost_from_here, best_j_loc]

        return best_cost_from_here

    return calc_best_cost_from(0, 1)    # 0 is visited


if __name__ == "__main__":
    locs = ["New York", "Los Angeles", "Philadelphia", "Seattle", "Austin"]

    distances, times = build_matrices(locs)

    print(distances)

    print(tsp_brute_force(distances))
    print(tsp_dp(distances))
