import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import ks_2samp

df = pd.read_csv("results/experiment_scale.csv")
factors = [0.015625, 0.03125, 0.0625, 0.125, 0.25, 0.5,
           1., 2., 4., 8., 16., 32., 64., 128.]

header = df.columns.values.tolist()
feature_list = header[8:]
basic_distr = [[] for _ in range(5)]
for problem_id in range(1, 6):
    df_new = df[(df["problem_id"] == problem_id) & (df["is_scale"] == 0)]
    for c in feature_list:
        basic_distr[problem_id-1] += [pd.to_numeric(df_new[c].tolist())]
basic_distr = np.array(basic_distr)

dataset = []
for problem_id in range(1, 6):
    for scale_factor in factors:
        df_new = df[(df["problem_id"] == problem_id) &
                    (df["scale_factor"] == scale_factor) &
                    (df["is_scale"] == 1)]
        rec = []
        for c in feature_list:
            p = pd.to_numeric(df_new[c].tolist())
            q = basic_distr[problem_id-1][len(rec)]
            statistic, pvalue = ks_2samp(p, q)
            rec += [[statistic, pvalue]]
        dataset += [[problem_id, 0, 0.0, 0.0, scale_factor, 0, 0, 1] + rec]

dataset_df = pd.DataFrame(dataset, columns=header)
dataset_df.to_csv("results/kstest_scale.csv")

x = [math.log(f, 2) for f in factors]
for problem_id in range(1, 6):
    plt.figure(figsize=(15, 20))
    for i in range(len(feature_list)):
        pvalue = np.array(
            dataset_df[(dataset_df["problem_id"] == problem_id)][
                feature_list[i]].tolist())[:, 1]
        plt.subplot(9, 6, i+1)
        plt.ylim(-0.1, 1.1)
        plt.plot(x, pvalue)
        plt.xlabel("$\log_2{scale\_factor}$")
        plt.axhline(0.05, color="red", linestyle=":")
        plt.title(feature_list[i])
    plt.tight_layout()
    plt.savefig("results/pvalue_scale_" + str(problem_id) + ".png")
    plt.cla()
