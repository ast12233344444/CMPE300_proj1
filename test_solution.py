import time
import numpy as np
from graph_construction import generate_tricky_graph
from solution import hamiltonian_naive, hamiltonian_optimized


class TestSoln:
    pass


def get_performance(n: int, is_naive: bool, trials: int):

    elapsed_times = []
    for _ in range(trials):
        graph, start, end = generate_tricky_graph(n)
        if is_naive:
            ts_pre = int(time.time() * 1000)
            hamiltonian_naive(graph, start, end)
            ts_post = int(time.time() * 1000)
            elapsed_times.append((ts_post - ts_pre))
        else:
            ts_pre = int(time.time() * 1000)
            hamiltonian_optimized(graph, start, end)
            ts_post = int(time.time() * 1000)
            elapsed_times.append((ts_post - ts_pre))

    print("=" * 10, f"n: {n}, OPTIMIZED: {not is_naive}, trials: {trials}, mean exec time: {np.mean(elapsed_times)}ms, std exec time: {np.std(elapsed_times)}ms", "=" * 10)


def test_custom_case():
    filled_submatrix = np.array(
        [[0,1,0,1],
        [1,0,1,0],
        [0,1,0,1],
        [1,0,1,0]]
    )
    empty_submatrix = np.array([[0 for _ in range(4)] for _ in range(4)])

    test_matrix = np.block([[filled_submatrix, empty_submatrix, empty_submatrix],
                            [empty_submatrix, filled_submatrix, empty_submatrix],
                            [empty_submatrix, empty_submatrix, filled_submatrix]]).tolist()

    print(* test_matrix, sep = "\n")

    for i in range(len(test_matrix)):
        for j in range(len(test_matrix[0])):
            if i == j:
                continue
            start =  i
            end = j
            exp = True
            if start // 4 != end // 4:
                exp = False
            if abs(start - end) == 2:
                exp = False
            #got = hamiltonian_naive(test_matrix, start, end)
            got = hamiltonian_optimized(test_matrix, start, end)
            print(f"start: {start}, end: {end}, expected: {exp} got: {got}")
            if exp != got:
                print("!!!!!!!!!!!POTENTIAL ERROR!!!!!!!!!!!")


if __name__ == '__main__':
    #test_custom_case()
    graph, start, end = generate_tricky_graph(7)

    ns = [4,5,6,7,8]
    for i in ns:
        get_performance(i, True, 10)
    ns = [4,5,6,7,8,9,10,11,12,13]
    for i in ns:
        get_performance(i, False, 10)
