import os

from pflacco.sampling import create_initial_sample

if not os.path.exists('samplingX/'):
    os.mkdir('samplingX/')

dim = 2
f = open("results/samplingX.txt", "w")
for i in range(1000):
    X = create_initial_sample(dim, lower_bound=[-100.0, -100.0],
                              upper_bound=[100.0, 100.0], sample_type='lhs')
    text = X.to_string() + "\n"
    f.writelines(text)
