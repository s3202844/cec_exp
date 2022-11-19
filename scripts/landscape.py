import re
import joypy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pflacco.classical_ela_features import calculate_ela_meta

ela_meta_keys = ['ela_meta.lin_simple.adj_r2',
                 'ela_meta.lin_simple.intercept',
                 'ela_meta.lin_simple.coef.min',
                 'ela_meta.lin_simple.coef.max',
                 'ela_meta.lin_simple.coef.max_by_min',
                 'ela_meta.lin_w_interact.adj_r2',
                 'ela_meta.quad_simple.adj_r2',
                 'ela_meta.quad_simple.cond',
                 'ela_meta.quad_w_interact.adj_r2',
                 'ela_meta.costs_runtime']


def read_x():
    X = []
    f = open("results/samplingX.txt", "r")
    lines = f.readlines()
    f.close()
    for i in range(1000):
        x = []
        content = lines[101*i:101*i+101]
        for j in range(1, 101):
            line = re.split(r"[ ]+", content[j][:-1])
            x += [[float(line[1]), float(line[2])]]
        X += [x]
    return X


def read_y(path):
    Y = []
    f = open(path, "r")
    lines = f.readlines()
    f.close()
    for i in range(1000):
        y = []
        line = lines[i][:-1].split(" ")
        for j in range(100):
            y += [float(line[j])]
        Y += [y]
    return Y


X = np.array(read_x())
Y = []
for i in range(1, 6):
    y = read_y("results/origin_"+str(i)+".txt")
    Y += [y]
Y = np.array(Y)

dataset = []
for i in range(5):
    dataset += [[]]
    for j in range(100):
        dataset[i] += [[]]
        ela_meta = calculate_ela_meta(X[j], Y[i][j])
        for k in range(10):
            dataset[i][j] = list(ela_meta.values())


pd_data = []
for i in range(5):
    for j in range(100):
        pd_data += [[]]
        for k in range(10):
            pd_data[-1] += [dataset[i][j][k]]
        pd_data[-1] += [str(i+1)]

df = pd.DataFrame(pd_data, columns=ela_meta_keys+["problem_id"])
print(df)
# Draw Plot
joypy.joyplot(df,
              column=ela_meta_keys[:1],
              by="problem_id",
            #   ylim='own',
            #   color=["#1f77b4d0"],
            #   title="Distribution of inplace sorting time consuming, $N=10000$.",
              figsize=(10, 6))
# rect1 = plt.Rectangle((0, 0), 0, 0, color='#1f77b4d0',
#                       label=ela_meta_keys[0])
# rect2 = plt.Rectangle((0, 0), 0, 0, color='#ff7f0ed0',
#                       label=ela_meta_keys[1])
# plt.gca().add_patch(rect1)
# plt.gca().add_patch(rect2)
plt.legend()
plt.savefig("ela_meta.png")
plt.cla()
