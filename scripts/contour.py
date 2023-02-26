import sys

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np


def plot_contour(file_path, file_name):
    # Make data.
    f = open(file_path)
    lines = f.readlines()
    # X = np.arange(-5, 5, 0.25)
    # Y = np.arange(-5, 5, 0.25)
    # X, Y = np.meshgrid(X, Y)
    X = []
    Y = []
    Z = []
    rec = [0, 0, 10**10]
    for line in lines:
        content = line.split(" ")
        X += [float(content[0])]
        Y += [float(content[1])]
        Z += [float(content[2])]
        if Z[-1] < rec[-1]:
            rec = [X[-1], Y[-1], Z[-1]]
    print(rec)
    X = np.array(X)
    Y = np.array(Y)
    Z = np.array(Z)
    n = int(X.shape[0]**0.5)
    X = np.reshape(X, (n, n)).T
    Y = np.reshape(Y, (n, n)).T
    Z = np.reshape(Z, (n, n)).T
    # print(Z.shape)

    plt.contourf(X, Y, Z)
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.savefig("results/contour/rotation/"+file_name+"_contour.png")
    plt.cla()

    # Plot the surface.
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
    ax.view_init(20, 230)

    # Customize the z axis.
    # ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    ax.zaxis.set_major_formatter('{x:.02f}')

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.savefig("results/landscape/rotation/"+file_name+".png")
    plt.cla()
    plt.close()


if __name__ == "__main__":
    for i in range(30):
        path = "results/exp_data/rotation/F1_rotation2D_{:0=2d}.txt".format(i)
        name = "F1_rotation2D_{:0=2d}".format(i)
        plot_contour(path, name)
