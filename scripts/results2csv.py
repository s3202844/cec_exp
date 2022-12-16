import re
import numpy as np
import pandas as pd

from pflacco.classical_ela_features import calculate_ela_meta
from pflacco.classical_ela_features import calculate_ela_distribution
from pflacco.misc_features import calculate_fitness_distance_correlation


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


# create "name" value for table data
table_name = "origin_affine"
names = []
for i in range(5):
    names += ["origin_"+str(i+1)]
for i in range(5):
    names += ["affine_"+str(i+1)]

# read experiments results
X = np.array(read_x())
Y = []
for i in range(10):
    file_path = "results/"+names[i]+".txt"
    y = read_y(file_path)
    Y += [y]
    print("Read file:", file_path)
Y = np.array(Y)

# create table
dataset = []
for i in range(10):
    for j in range(100):
        record = [names[i]]
        ela_meta = calculate_ela_meta(X[j], Y[i][j])
        ela_distr = calculate_ela_distribution(X[j], Y[i][j])
        fdc = calculate_fitness_distance_correlation(X[j], Y[i][j])
        record += list(ela_meta.values())
        record += list(ela_distr.values())
        record += list(fdc.values())
        dataset += [record]

# save table
column_names = ["name"] + list(ela_meta.keys()) + \
    list(ela_distr.keys()) + list(fdc.keys())
dataset_df = pd.DataFrame(dataset, columns=column_names)
dataset_df.to_csv("results/"+table_name+".csv")
