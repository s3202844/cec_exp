import sys

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np


def plot_contour(file_path, file_name, angle, ax):
    # Make data.
    f = open(file_path)
    lines = f.readlines()
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
    ax.contourf(X, Y, Z, cmap='terrain')
    ax.scatter(rec[0], rec[1], c="r", marker="x")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(str(angle) + "$^\circ$")


def plot_landscape(file_path, file_name, angle, ax):
    # Make data.
    f = open(file_path)
    lines = f.readlines()
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
    # Plot the surface.
    ax.scatter(rec[0], rec[1], rec[2], c="r", marker="x")
    ax.plot_surface(X, Y, Z, cmap='terrain', linewidth=0, antialiased=False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    ax.view_init(20, 230)
    # Customize the z axis.
    # ax.set_zlim(-1.01, 1.01)
    # ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    # ax.zaxis.set_major_formatter('{x:.02f}')
    ax.set_title(str(angle) + "$^\circ$")


if __name__ == "__main__":
    fig, ax = plt.subplots(6, 5, sharex='col', sharey='row', figsize=(9, 12))
    for i in range(30):
        path = "results/exp_data/rotation/F1_rotation2D_{:0=2d}.txt".format(i)
        name = "F1_rotation2D_{:0=2d}".format(i)
        plot_contour(path, name, i*12, ax[i//5][i % 5])
    fig.tight_layout()
    fig.savefig("results/contour/rotation/contour.png")
    fig.savefig("results/contour/rotation/contour.eps", format="eps", dpi=600)
    plt.cla()
    plt.close()

    fig = plt.figure(figsize=(9, 12))
    for i in range(30):
        ax = fig.add_subplot(6, 5, i+1, projection='3d')
        path = "results/exp_data/rotation/F1_rotation2D_{:0=2d}.txt".format(i)
        name = "F1_rotation2D_{:0=2d}".format(i)
        plot_landscape(path, name, i*12, ax)
    # fig.colorbar(surf, shrink=0.5, aspect=5)
    fig.tight_layout()
    fig.savefig("results/contour/rotation/lanscape.png")
    fig.savefig("results/contour/rotation/lanscape.eps", format="eps", dpi=600)
    plt.cla()
    plt.close()
