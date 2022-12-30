import os
import re
import warnings
import numpy as np
import pandas as pd

from pflacco.classical_ela_features import calculate_dispersion
from pflacco.classical_ela_features import calculate_ela_distribution
from pflacco.classical_ela_features import calculate_ela_level
from pflacco.classical_ela_features import calculate_ela_meta
from pflacco.classical_ela_features import calculate_information_content
from pflacco.classical_ela_features import calculate_limo
from pflacco.classical_ela_features import calculate_nbc
from pflacco.classical_ela_features import calculate_pca

warnings.filterwarnings("ignore")


def read_x(num_sampling, num_x):
    X = []
    m = num_x+1
    f = open("results/samplingX.txt", "r")
    lines = f.readlines()
    f.close()
    for i in range(num_sampling):
        x = []
        content = lines[m*i:m*i+m]
        for j in range(1, m):
            temp = []
            line = re.split(r"[ ]+", content[j][:-1])
            for n in line[1:]:
                temp += [float(n)]
            x += [temp]
        X += [x]
    return X


def read_y(path, num_sampling, num_x):
    Y = []
    f = open(path, "r")
    lines = f.readlines()
    f.close()
    for i in range(num_sampling):
        y = []
        line = lines[i][:-1].split(" ")
        for j in range(num_x):
            y += [float(line[j])]
        Y += [y]
    return Y


def calculate_features(X, y):
    keys = []
    values = []

    disp = calculate_dispersion(X, y)
    keys += list(disp.keys())[:-1]
    values += list(disp.values())[:-1]

    ela_distr = calculate_ela_distribution(X, y)
    keys += list(ela_distr.keys())[:-1]
    values += list(ela_distr.values())[:-1]

    ela_level = calculate_ela_level(X, y)
    keys += list(ela_level.keys())[:-1]
    values += list(ela_level.values())[:-1]

    ela_meta = calculate_ela_meta(X, y)
    keys += list(ela_meta.keys())[:-1]
    values += list(ela_meta.values())[:-1]

    # ic = calculate_information_content(X, y)
    # keys += list(ic.keys())[:-1]
    # values += list(ic.values())[:-1]

    limo = calculate_limo(X, y, lower_bound=[-100. for _ in range(dim)],
                          upper_bound=[100. for _ in range(dim)])
    keys += ["limo.avg_length_norm", "limo.length_mean", "limo.ratio_mean"]
    values += [limo[keys[-3]], limo[keys[-2]], limo[keys[-1]]]

    nbc = calculate_nbc(X, y)
    keys += list(nbc.keys())[:-1]
    values += list(nbc.values())[:-1]

    pca = calculate_pca(X, y)
    keys += list(pca.keys())[:-1]
    values += list(pca.values())[:-1]
    return keys, values


# meta data
num_sampling = 100
num_x = 1000
dim = 10

# collect basic data for table
problem_ids = []
experiment_ids = []
subtract_lims = []
is_subtracts = []
file_list = os.listdir("results/data/subtract")
for file_name in file_list:
    match_obj = re.match(
        r"(\d+)_(\d+)_(\d+\.\d+)_(\d+\.\d+)_(\d+)_(\d+)\.txt", file_name)
    problem_ids += [int(match_obj.group(1))]
    experiment_ids += [int(match_obj.group(2))]
    subtract_lims += [float(match_obj.group(3))]
    is_subtracts += [int(match_obj.group(5))]
table_name = "experiment_subtract"

# read experiments results
X = np.array(read_x(num_sampling, num_x))
Y = []
for file_name in file_list:
    file_path = "results/data/subtract/" + file_name
    y = read_y(file_path, num_sampling, num_x)
    Y += [y]
    print("Read file:", file_path)
Y = np.array(Y)

is_write = False
keys, _ = calculate_features(X[0], Y[0][0])
column_names = ["problem_id", "experiment_id",
                "subtract_lim", "is_subtract"] + keys
# create table
for file_ind in range(Y.shape[0]):
    if experiment_ids[file_ind] > 2:
        continue
    for i in range(num_sampling):
        # for i in range(2):
        keys, values = calculate_features(X[i], Y[file_ind][i])
        record = [problem_ids[file_ind], experiment_ids[file_ind],
                  subtract_lims[file_ind], is_subtracts[file_ind]] + values
        dataset_df = pd.DataFrame([record], columns=column_names)
        if not is_write:
            dataset_df.to_csv("results/"+table_name+".csv")
            is_write = True
        else:
            dataset_df.to_csv("results/"+table_name+".csv",
                              header=False, mode="a")
        print(file_list[file_ind] + " sample " + str(i) + " done.")
