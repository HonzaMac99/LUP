#!/usr/bin/python3
import os
import math
from pysat.formula import CNF
from pysat.solvers import Glucose3
from pysat.card import CardEnc, EncType

in_str = input()
# in_str = "WWB0WWWB0WWBW0BBWBWBWWWBWW2WWWBW2WBWWBBWBBW1BBWBBWBWWWW21WWWWBWWBWWWWBBW3WBBW2WWBBWWB3WWWBWBWWBWWWWWBWWWWWBWWWWWWWWW3WWWWBBWBWWBBBWWWBBWWBBBWBWWW3WWWBWWWBW3WWWBBWWWWWWWBWW2W0WWWBWWBWBWWWWWWB3W1WWWBWWB2W2WWWWBW0WWWWBWWWBWWWWWBWBWWWW3BBBB2W2WWW0WWWWWWWB1WWWWW0WWBB1BW2BBWWW1WWBW2WWWWWWWBWWB0WWBW1WW0W0W0WWWWBWWWWBWWWWBWBBW1WWWBWWBWWWWWWWWWWWWWWWWWWWB1WWWWBBWWWWWW1WWWWBWWWWWWWWWWW2BWBWWWW1WBWW0WWBBWWWBBBBWW0WBWBWWWWBBWBWBWWBWWBWB2WBWWWBBWBBWWWWWWWWWWBBWW2WWWWW0WW2WW1WW31WWW2WWWBWWW1WBWWWWWWBBWWWBBWWWW2BBWWWWWWWB0WBBBWWWWBBWBBBWWWBWWWBBBBWWWWW2BW0WWWBWBW10WBBWW1WBWWWBWW2WBWBBWBWWB3WWWBW2B1WW1W1WWW1B0WBWWBWWBWBBWBBWW0BBBW1WWWBWWWBWWWWWBWWB2WWWBWWWWWWWWW2WW1WWBWBWW1WWB0WWWWWWW1WBBW1WWWWBBWWWWW1WWWWBW1WWBWWWBWBBWWBB0WWBBWWWWWWB1WWBWWW1W3WBWBWWW3WW0BBB1WBBWW0WBWWWW0WWWWWB2BWW1WWWWWWWBBBWWBB0WB2WWWWBWWBWBWWWWBWWWWWWWWWW0WWB1BWBWWWWWWW2WWWBWW2WBWWBWW1WWB1WWWWWWWW1WWW2WWWWBWWWWWB2WW1WWWWB1WWBWBBWWWWBWBWWBWWBWBWBWWBWWWBWWWWWW1WWBBWBWWWWBBWWBWWBWB0WWWB2W3WWWWBWBBBBWWWWWW1WBW2BW1WWWWWWWBBBWWBBWWWWWW1BWW2WWWW1WWWWWBWWWBBWW0BWWWWWWWBWW1W1WBBWWWW0WWWW3WWWBWWWWBBWWWWW1WW12WWWWWWBWWWBWWWWBWWWW3WWWW1W1BWWWBB2WW2WBBW2WBBWBWW2WWWB1WWWWB0WBWBWW1BBWBWWWWWBBW0WWWBBWWWWBW3WW1WWWWWWW0WWBBWWWWWB2WWWWW1WWWWW1WWBWBWWWWWWBWB1WWWW0WB0W1WWWWWBWWBWW2WWWWB0WWW1BBWB1WWB1WB1BWWWB0WWWW1WW0WWBWWWWWBW1BWBWWWWB0WBWWWWWWBW3WWBWWWWW1WWWWWBBWWWWWBBWW1WWWWWWWBWWBW2WWWWBBWWWBWB1WWWWWBWBBBWW1WBW10WWWWB0WWWBWW0WBBWBWBBWBWW012WWWBBWBWWWWBWWWWBWWWW2WWW1WWWWWWBBWW0WWWWWB0WWWWBWWW2WWWW2WWWW2BWBW2WWBWWWWWWW0BWWB1WWWBWWWWWBWWWW1WW1BWWWWWWB0WWBBBWWWWWWW3WBBW0W1WWWWWWBBB1W1WWWWBWBBWWWBBWBWWBWWBBWWWW1WBBWWBWWWWWW3WWW2WW2WBW1WW1WWBWBWWWWBBWBWWB2WWWW1WW11WWWWW3WWWWBWWWBWWWWWWWWBBWWBWW1WW1W2WW2WWWBWWWWWWWBWBBBWW0WWWWWWWWWW1WWWWBW3WW1WWWW1BWBBBWWBBBWWWWWWWBWW1BBWWWWWBWWWWBWBWW0BW1BBBBWWBWWWBW2W1WBWWW1WWB1WWWWWWB1WWBBBWWBBWBWWWBWW1WBWWWW1WWWWWBBWWWW0WBBWBWWWWWWWBBWWBWW2WBWW2WWBWWWWWWWWWBWWWBBWWBWWWWWBWWWBWWW0WBBB1WWBBWBBWBWWBWWBWB10WWWBW1WWB0BWBWWWBBWW2WB1W1WBWWBWWWBW0WWB1WBBWBWBWWW1W20WWWWWBB10WWWBWWWBBBWBBWWWWBB2WBBWWWWWWWB12WWWWBBWWWBBWWWWWWBWBWWW3WWWBWWW1BWWBWW1WWBWWWWWBWWB1WWWWWWWWWWBBWB1WWWBWBBWBWW2WW0WBWBBWWWW1W0W1WWBBB0WWWB1WW0WW1W3WWWW1W1BWWWWWWWWWWW2WWWWBWWWWWWB1WWWWB0WWWWWWWWWWWWWWWWWWW0WWBWWWBW1BWBWWWW0WWWW0WWWW2WBW2WW1WBWW1BWW0WWWWWWWBW1WWBWWWBBBWB1B0WW1WWWWWBBWWWWWWWBWWWBWBBBBB1WWWWBWBWWWWW1WWW3WWWWBW1WWWW1W20WWBWWW1W2BWWWWWW1WBWWBWWW1WBWWBWWWWWWW01WWW2WBWWWBWWWBWWWBWBB3WWB0WWWB1BWW0WB2WWWWBWWWWWWWWW1WWWWWBWWWWW0WW1WBWWWBBWWBBWW1W1BWBWBBWWWWBWWBWWWWB2WWWWBWB2WBBBWB2WBBWWBWBWBWWWBWW3WWW1W1WBB1W1WW0BWWWB1WW"
# in_str = "WWWBW0BWWWWWWWWWWW12WBWWW"
# in_str = "WWWWWW4WW2WWWWWW"
# in_str = "WW2W"


n = int(math.sqrt(len(in_str)))
assert n**2 == len(in_str), "invalid input length!"

def LB(i, j):
    return i*n + j + 1

def IL(i, j):
    return n**2 + i*n + j + 1

max_var = n**2 + n**2 + 100

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

def two_of_four(neighbor_lbs):
    new_cnf = []
    for i in range(len(neighbor_lbs)):
        subset = neighbor_LBs[:i] + neighbor_LBs[i+1:]
        new_cnf.append(subset)
        new_cnf.append([-lb for lb in subset])
    return new_cnf


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
                exit(10)
            elif lb_count == 0:
                for lb in neighbor_LBs:
                    cnf.append([-lb])
            elif lb_count == len(neighbor_LBs):
                for lb in neighbor_LBs:
                    cnf.append([lb])
            elif lb_count == len(neighbor_LBs) - 1 or lb_count == 1:
                cnf.extend(CardEnc.equals(lits=neighbor_LBs, bound=lb_count, encoding=EncType.pairwise))
            elif len(neighbor_LBs) - lb_count == 2: # two of four
                # cnf.extend(CardEnc.equals(lits=neighbor_LBs, bound=lb_count, encoding=EncType.seqcounter, top_id=max_var))
                # cnf.extend(CardEnc.equals(lits=neighbor_LBs, bound=lb_count, encoding=EncType.totalizer, top_id=max_var))
                cnf.extend(two_of_four(neighbor_LBs))
            else:
                print("You hadn't solved this condition yet!")


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

