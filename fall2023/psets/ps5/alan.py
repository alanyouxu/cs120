from itertools import product, combinations

for comb in combinations(range(5),2):
    x = [i for i in comb]
    y = {i for i in comb}
    print("List:", x, x[0])
    print("Set:", y, y[0])