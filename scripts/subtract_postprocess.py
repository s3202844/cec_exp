import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import ks_2samp

df = pd.read_csv("results/experiment_subtract.csv")
header = df.columns.values[1:].tolist()

basic_distr = [[] for _ in range(5)]
for problem_id in range(1, 6):
    df_new = df[(df["problem_id"] == problem_id) & (df["is_subtract"] == 0)]
    for c in header[4:]:
        basic_distr[problem_id-1] += [pd.to_numeric(df_new[c].tolist())]
basic_distr = np.array(basic_distr)

dataset = []
for problem_id in range(1, 6):
    for experiment_id in range(3):
        for subtract_lim in [5.0*i for i in range(1, 21)]:
            df_new = df[(df["problem_id"] == problem_id) &
                        (df["experiment_id"] == experiment_id) &
                        (df["subtract_lim"] == subtract_lim) &
                        (df["is_subtract"] == 1)]
            rec = []
            for c in header[4:]:
                p = pd.to_numeric(df_new[c].tolist())
                q = basic_distr[problem_id-1][len(rec)]
                statistic, pvalue = ks_2samp(p, q)
                rec += [[statistic, pvalue]]
            dataset += [[problem_id, experiment_id, subtract_lim, 1] + rec]

dataset_df = pd.DataFrame(dataset, columns=header)
dataset_df.to_csv("results/kstest_subtract.csv")

for problem_id in range(1, 6):
    plt.figure(figsize=(15, 20))
    for i in range(4, len(header)):
        pvalue = np.array(dataset_df[(dataset_df["problem_id"] == problem_id) & (
            dataset_df["experiment_id"] == 0)][header[i]].tolist())[:, 1]
        for j in range(2):
            pvalue += np.array(dataset_df[(dataset_df["problem_id"] == problem_id) & (
                dataset_df["experiment_id"] == j+1)][header[i]].tolist())[:, 1]
        pvalue /= 3
        plt.subplot(9, 6, i-3)
        plt.ylim(-0.1, 1.1)
        plt.plot([5.0 * n for n in range(1, 21)], pvalue)
        plt.axhline(0.05, color="red", linestyle=":")
        plt.title(header[i])
    plt.tight_layout()
    plt.savefig("results/pvalue_subtract_" + str(problem_id) + ".png")
    plt.cla()
