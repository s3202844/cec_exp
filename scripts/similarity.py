import sys
import math
import scipy.stats

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def JS_divergence(p, q):
    M = (p+q)/2
    return 0.5*scipy.stats.entropy(p, M, base=2)+0.5*scipy.stats.entropy(q, M, base=2)


records = pd.read_csv(sys.argv[1])
records_np = records.to_numpy()

keys = []
values = [[] for _ in range(5)]
# values = [[str(i+1)] for i in range(5)]
for i in range(records_np.shape[1]-2):
    for j in range(5):
        n = j
        m = n + 5
        arr1 = records_np[100*n:100*n+100, i+2].astype(np.float32)
        arr2 = records_np[100*m:100*m+100, i+2].astype(np.float32)
        dist = JS_divergence(arr1, arr2)
        if records.columns[i+2] not in keys:
            keys += [records.columns[i+2]]
        if math.isinf(dist):
            values[j] += [-1]
        else:
            values[j] += [-dist]
        if math.isinf(dist):
            print("=======================")
            print(arr1)
            print(arr2)

column_names = keys
# column_names = ["name"] + keys
df = pd.DataFrame(values, columns=column_names)
print(df)
sns.heatmap(df, cmap="hot", square=True)
plt.title("Jensen-Shannon divergence of \n landscape features of affine operation \n on CEC2022 basic problems")
plt.savefig("results/js_dist_affine.png")
