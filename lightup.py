#!/usr/bin/python3
import os
import math
from pysat.formula import CNF
from pysat.solvers import Glucose3
from pysat.card import CardEnc, EncType

in_str = input()
# in_str = "WWWWBBW01WBWWWBWWW3WWBWWWWWWWW1W2WBWWW3WW1WW0WWWWWWW1WBWWWBWBWWWBWWWWWWWBWWWWWWW4WBBBWWWWWWW1WWWWWWWWB1WBWWWWWWBWWWWWWWWWW1WW1WWWW0WBBWB1WWWWWWWWWWWWWWW0BW1BWBWWWW3WWBWWWWWWWWWWBWWWWWWBWB0WWWWWWWW1WWWWWWW0BBW1WWWWWWWBWWWWWWW1WWW1WBWWWBW3WWWWWWW1WW0WW2WWWBW3WBWWWWWWWWBWW2WWWBWWWBWBBWBBWWWW"
# in_str = "WWWBW0BWWWWWWWWWWW12WBWWW"
# in_str = "WWWWWW4WW2WWWWWW"
# in_str = "WW2W"
n = int(math.sqrt(len(in_str)))
assert n**2 == len(in_str), "invalid input length!"

def LB(i, j):
    return i*n + j + 1

def IL(i, j):
    return n**2 + i*n + j + 1

max_var = n**2 + n**2 + n + 100

cnf = CNF()


def is_black(i, j):
    return in_str[i*n + j] in ["B", "0", "1", "2", "3", "4"]

def get_lb_count(i, j):
    if not is_black(i, j):
        print("get_lb_count: The cell is not black!")
        return None
    elif in_str[i*n + j] == "B":
        return -1
    else:
        return int(in_str[i*n + j])

# Helper: visible cells in same row (for simplicity)
def visible_cells(i, j):
    if is_black(i, j):
        print("visible_cells: Wrong cell!!")
        return []

    vc = [(i,j)]
    ii, jj = i-1, j-1
    while ii >= 0 and not is_black(ii, j):
        vc.append((ii, j))
        ii -= 1
    while jj >= 0 and not is_black(i, jj):
        vc.append((i, jj))
        jj -= 1

    ii, jj = i+1, j+1
    while ii < n and not is_black(ii, j):
        vc.append((ii, j))
        ii += 1
    while jj < n and not is_black(i, jj):
        vc.append((i, jj))
        jj += 1
    return vc

def get_black_neighbors(i, j):
    bn = []
    if not is_black(i, j):
        print("get_black_neighbors: Wrong cell!!")
    else:
        if i > 0 and not is_black(i-1, j):
            bn.append((i-1, j))
        if i < n-1 and not is_black(i+1, j):
            bn.append((i+1, j))
        if j > 0 and not is_black(i, j-1):
            bn.append((i, j-1))
        if j < n-1 and not is_black(i, j+1):
            bn.append((i, j+1))
    return bn


for i in range(n):
    for j in range(n):
        # Illumination rule
        if not is_black(i, j):
            visible_LBs = [LB(a, b) for (a, b) in visible_cells(i, j)]
            cur_il = IL(i, j)

            # 1) IL -> (any visible LB)
            cnf.append([-cur_il] + visible_LBs)

            # 2) Each visible LB -> IL
            for lb in visible_LBs:
                cnf.append([-lb, cur_il])

            # 3) lightbulbs can't "see" each other
            cur_lb = LB(i, j)
            for lb in visible_LBs:
                if lb != cur_lb:
                    cnf.append([-cur_lb, -lb])

            # 4) we want this cell to be lit
            cnf.append([cur_il])

        # black cell rules
        else:
            lb_count = get_lb_count(i, j)
            neighbor_LBs = [LB(a, b) for (a, b) in get_black_neighbors(i, j)]
            if lb_count == -1:
                continue # there is simply no restriction
            elif lb_count > len(neighbor_LBs):
                print("0")
                exit()
            elif lb_count == 0:
                for lb in neighbor_LBs:
                    cnf.append([-lb])
            elif lb_count == len(neighbor_LBs):
                for lb in neighbor_LBs:
                    cnf.append([lb])
            elif lb_count == len(neighbor_LBs) - 1 or lb_count == 1:
                cnf.extend(CardEnc.equals(lits=neighbor_LBs, bound=lb_count, encoding=EncType.pairwise))
            else:
                # cnf.extend(CardEnc.equals(lits=neighbor_LBs, bound=lb_count, encoding=EncType.seqcounter, top_id=max_var))
                cnf.extend(CardEnc.equals(lits=neighbor_LBs, bound=lb_count, encoding=EncType.totalizer, top_id=max_var))

# Sanity check
for c in cnf.clauses:
    assert all(isinstance(v, int) and v != 0 for v in c)

# Create solver correctly
solver = Glucose3(bootstrap_with=cnf.clauses)
success = solver.solve()
vars = solver.get_model()

# print("CNF:", cnf.clauses)
# print("SAT:", success)
# print("Model:", vars)

# compose the output sting
if success:
    out_str = in_str
    for i in range(n*n):
        if vars[i] > 0:
            out_str = out_str[:i] + "L" + out_str[i+1:]
else:
    out_str = "0"
print(out_str)

