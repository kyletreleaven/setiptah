
import numpy as np

pi_over_2 = .5 * np.pi


#theta1 = np.random.rand() * 2 * np.pi
theta1 = .25 * np.pi
sigma = np.array([ 1., -1 ])
Sigma = np.diag(sigma)

theta2 = theta1 + pi_over_2
u1 = np.array([ np.cos(theta1), np.sin(theta1) ])
u2 = np.array([ np.cos(theta2), np.sin(theta2) ])
U = np.vstack([u1, u2]).transpose()
P = np.dot( U.transpose(), np.dot(Sigma,U) )

def quadraticP(x,y) :
    xx = np.array([x,y])
    return np.dot( xx, np.dot(P,xx) )



import vis
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection   # EllipseCollection,

plt.close('all')

ax = vis.get_axes3d()

# grid points
xs = np.linspace(-1,1,100)
X,Y = np.meshgrid(xs,xs)

# quadratic surface data
zfunc = np.vectorize( quadraticP )
Z = zfunc(X,Y)

# plot quadratic
ax.plot_surface(X,Y,Z)
ax.scatter([0.],[0.],zs=[0.], marker='x', color='r')

plt.title('Quadratic Definiteness Example')
plt.xlabel('$x$')
plt.ylabel('$y$')
ax.set_zlabel('$f(x,y)$')

# make sure starts at z=0
zlim = ax.get_zlim()
zlim[0] = 0.
ax.set_zlim(zlim)

plt.show()




