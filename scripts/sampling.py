import os

from pflacco.sampling import create_initial_sample

dim = 10
f = open("results/samplingX.txt", "w")
for i in range(100):
    X = create_initial_sample(dim, n=1000,
                              lower_bound=[-100.0 for _ in range(dim)],
                              upper_bound=[100.0 for _ in range(dim)],
                              sample_type='lhs')
    text = X.to_string() + "\n"
    f.writelines(text)
