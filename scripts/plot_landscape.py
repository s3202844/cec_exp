import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

# 生成地形数据
X = np.arange(-100, 100.5, 0.5)
Y = np.arange(-100, 100.5, 0.5)
X, Y = np.meshgrid(X, Y)

for i in range(1, 6):
    filename = "results/landscape/F" + str(i) + ".txt"
    Z = []
    with open(filename, 'r') as f:
        for line in f:
            # 解析每行数据，用空格分割并转换为 float 类型
            numbers = [float(x) for x in line.split()]
            Z += [numbers[-1]]
    Z = np.array(Z).reshape(X.shape)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap=cm.coolwarm)
    # 隐藏z轴
    ax.set_zticks([])
    ax.view_init(elev=30, azim=45)
    plt.tight_layout()
    plt.savefig("results/landscape/forthesis_{}.png".format(i))
