
import numpy as np
import scipy as sp
import scipy.linalg as splin

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def get_axes3d() :
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    return ax

class data : pass
GLOBALS = data()

GLOBALS.a = 1.
GLOBALS.b = 10.


""" non-linear system """
""" linear after a "Rosenbrock transformation" """

def XYtoUV(x,y) :
    u = GLOBALS.a - x
    v = GLOBALS.b * ( y - np.power(x,2.) )
    return u,v

def UVtoXY(u,v) :
    x = GLOBALS.a - u
    y = v / GLOBALS.b + np.power( GLOBALS.a - u, 2.)
    return x,y

#points = [ np.random.rand(2) for k in range(10) ]
#same_points = [ UVtoXY( *XYtoUV( *p ) ) for p in points ]




def Rosenbrock1(x,y) :
    u,v = XYtoUV(x,y)
    return np.power(u,2.) + np.power(v,2.)

def Rosenbrock2(x,y) :
    a = GLOBALS.a
    b = GLOBALS.b
    return np.power(a-x, 2.) + b * np.power( y - np.power(x,2.), 2.)



"""
After transformation, we will interpret u as position, and v as velocity;
we will create the dynamics of a spring-mass-damper system
m \dot\dot x = F - k x - c \dot x


""" 
GLOBALS.k = 100.
GLOBALS.c = 5.
GLOBALS.m = 1.

k, c, m = GLOBALS.k, GLOBALS.c, GLOBALS.m

A = np.array([[ 0., 1. ],
              [ -k/m, -c/m ]])
b = np.array([ 0., 1./m ])

Q = -np.eye(2)
P = splin.solve_lyapunov(A.transpose(),Q)
#P = np.dot(X,X.transpose())


def UVtrajectory(t, u0, v0 ) :
    X0 = np.array([u0, v0])
    Phi_t = splin.expm( t*A )
    return np.dot( Phi_t, X0 )


if __name__ == '__main__' :

    plt.close('all')
    
    if False :
        xs = np.linspace(-2,2,100)
        ys = np.linspace(-1,5,100)
        
        Xs, Ys = np.meshgrid(xs,ys)
        
        MatRosen1 = np.vectorize(Rosenbrock1)
        MatRosen2 = np.vectorize(Rosenbrock2)
        Zs1 = MatRosen1(Xs,Ys)
        Zs2 = MatRosen2(Xs,Ys)
        
        fig = plt.figure()
        ax1 = fig.add_subplot(2,1,1, projection='3d')
        ax1.plot_surface(Xs,Ys,Zs1)
        
        ax2 = fig.add_subplot(2,1,2, projection='3d') 
        ax2.plot_surface(Xs,Ys,Zs2)

    # initial conditions
    u0 = 4.
    v0 = 0.
    
    ts = np.linspace(0,5,100)
    
    traj = [ UVtrajectory(t, u0, v0) for t in ts ]
    traju = [ u for u,v in traj ]
    trajv = [ v for u,v in traj ]
    
    if False :        
        """ display trajectory in 3 space """
        ax = get_axes3d()
        ax.plot(traju,trajv,zs=ts)
    
    if False :
        """ plot trajectory components vs. time """
        plt.figure()
        ax = plt.gca()
        ax.plot(ts,traju)
        ax.plot(ts,trajv)

    """ prepare Lyapunov functions """
    def quadratic(x,Q) :
        return np.dot( x, np.dot(Q,x) )

    def LyapunovFunction(u,v) :
        return quadratic( np.array([u,v]), P )
    
    VectorizedLyap = np.vectorize(LyapunovFunction)

    
    """ show trajectory on Lyapunov function """
    # get window from the trajectory
    umin = min(traju)
    umax = max(traju)
    vmin = min(trajv)
    vmax = max(trajv)
    urad = max(-umin,umax)
    vrad = max(-vmin,vmax)
    us = np.linspace(-urad,urad,100)
    vs = np.linspace(-vrad,vrad,100)
    U, V = np.meshgrid(us,vs)
    
    Pot = VectorizedLyap(U,V)
    
    trajPot = [ LyapunovFunction( *xx ) for xx in zip(traju,trajv) ]
    
    ax = get_axes3d()
    ax.plot_surface(U,V,Pot)
    ax.plot(traju,trajv,zs=trajPot,c='r')
    
    """ plot the Lyapunov value signal against time """ 
    plt.figure()
    plt.plot(ts, trajPot)
    
    
    plt.show()
    
    
    
    