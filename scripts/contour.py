import sys

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np


file_name = sys.argv[1]
# Make data.
f = open("exp_data/"+file_name+".txt")
lines = f.readlines()
# X = np.arange(-5, 5, 0.25)
# Y = np.arange(-5, 5, 0.25)
# X, Y = np.meshgrid(X, Y)
X = []
Y = []
Z = []
rec = [0, 0, 100]
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
plt.savefig("contour/"+file_name+"_contour.png")
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

plt.savefig("landscape/"+file_name+".png")
