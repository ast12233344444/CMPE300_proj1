def hamiltonian_check(H, perm):
    """
    :param H nxn matrix of 0, 1:
    :param perm permutation vector to try
    :return if it is a valid hamiltonian path:
    """
    n = len(H)
    for i in range(n-1):
        if H[perm[i]][perm[i+1]] == 0:
            return False
    return True

def default_permutation_checker(H, trace, remaining, end):
    if len(remaining) == 0:
        trace.append(end)
        if hamiltonian_check(H, trace):
            return True
        else:
            trace.pop()
            return False

    else:
        rem_list = list(remaining)
        for rem_elem in rem_list:
            trace.append(rem_elem)
            remaining.remove(rem_elem)
            if default_permutation_checker(H, trace, remaining, end):
                return True
            trace.pop()
            remaining.add(rem_elem)
    return False

def check_all_permutations(H, start, end):
    remaining = set()
    for i in range(len(H)):
        if (i == start) or (i == end):
            continue
        remaining.add(i)

    response = default_permutation_checker(H, [start], remaining, end)
    return response

def get_subset_dfs(graph, node, marked):
    for i in range(len(graph[node])):
        if marked[i] == 1:
            continue
        if graph[node][i] == 0:
            continue

        marked[i] = 1
        get_subset_dfs(graph, i, marked)


def get_connected_subset(graph, start):
    marked = [False for _ in range(len(graph))]
    marked[start] = True
    get_subset_dfs(graph, start, marked)

    L = [i for i in range(len(graph)) if marked[i]]
    H = [[0 for _ in range(len(graph)//3)] for _ in range(len(graph[0])//3)]
    for i in range(len(L)):
        for j in range(len(L)):
            H[i][j] = graph[L[i]][L[j]]
    return H, L

def finish_combination(trace, all_combs, cur_ind, n, start, end):
    if len(trace) + 1 == n:
        trace.append(end)
        all_combs.append(trace.copy())
        trace.pop()
        return

    for i in range(cur_ind, 3*n):
        if i == start:
            continue
        if i == end:
            continue
        trace.append(i)
        finish_combination(trace, all_combs, i+1, n, start, end)
        trace.pop()


def get_all_combinations(graph, start, end):
    nx3  = len(graph)
    n = nx3 // 3

    all_combs = []
    finish_combination([start], all_combs, 0, n, start, end)

    return all_combs


def hamiltonian_naive(graph, start, end):
    all_combs = get_all_combinations(graph, start, end)

    n = len(graph) // 3
    H = [[0 for _ in range(n)] for _ in range(n)]

    for comb in all_combs:
        for i in range(len(comb)):
            for j in range(len(comb)):
                H[i][j] = graph[comb[i]][comb[j]]
        if check_all_permutations(H, 0, len(H)-1):
            return True
    return False


def hamiltonian_optimized(graph, start, end):
    H, L = get_connected_subset(graph, start)
    if end not in L:
        return False

    start_i = L.index(start)
    end_i = L.index(end)

    if check_all_permutations(H, start_i, end_i):
        return True
    return False
