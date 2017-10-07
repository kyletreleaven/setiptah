
import numpy as np

pi_over_2 = .5 * np.pi

#theta1 = np.random.rand() * 2 * np.pi
theta1 = .25 * np.pi
sigma = np.array([ 1., 2. ])
Sigma = np.diag(sigma)

theta2 = theta1 + pi_over_2
u1 = np.array([ np.cos(theta1), np.sin(theta1) ])
u2 = np.array([ np.cos(theta2), np.sin(theta2) ])
U = np.vstack([u1, u2]).transpose()
P = np.dot( U.transpose(), np.dot(Sigma,U) )

def quadraticP(x,y) :
    xx = np.array([x,y])
    return np.dot( xx, np.dot(P,xx) )

def getQuadraticLevelCirculation(beta) :
    ts = np.linspace(0,2*np.pi,100)[:]
    us = [ (np.cos(t), np.sin(t) ) for t in ts ]
    rs = [ np.sqrt( beta / quadraticP(x,y) ) for x,y in us ]
    verts = [ (r*np.cos(t),r*np.sin(t)) for t, r in zip(ts,rs) ]
    return verts



if __name__ == '__main__' :
    import vis
    import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection   # EllipseCollection,

    import argparse
    
    plt.close('all')
    
    parser = argparse.ArgumentParser()
    parser.add_argument('level', type=float )
    args = parser.parse_args()
    
    # level set circulation
    verts = getQuadraticLevelCirculation(args.level)
    xell = [ x for x,y in verts ]
    yell = [ y for x,y in verts ]
    
    # start drawing
    ax = vis.get_axes3d()
    
    # draw sublevel ellipse
    poly = PolyCollection([verts], closed=False)
    poly.set_alpha(.7)
    ax.add_collection3d(poly, zs=0., zdir='z' )
    
    # draw ellipse cut curve
    ax.plot(xell,yell,zs=args.level,color='r')
    
    # draw cylinder
    ntier = 2
    zs = np.linspace(0,args.level,ntier) # just bottom and top
    
    x = np.outer( np.ones(ntier), xell )
    y = np.outer( np.ones(ntier), yell )
    z = np.outer( zs, np.ones(np.size(xell)) )
    
    ax.plot_surface(x,y,z, color='b', alpha=.2 )
    #ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='b')
    
    
    # grid points
    xs = np.linspace(-1,1,100)
    X,Y = np.meshgrid(xs,xs)
    
    # quadratic surface data
    zfunc = np.vectorize( quadraticP )
    Z = zfunc(X,Y)
    
    # plot quadratic
    ax.plot_surface(X,Y,Z)
    
    
    plt.title('Sub-level Set $V(x,y) \leq %.1f$' % args.level )
    plt.xlabel('$x$')
    plt.ylabel('$y$')
    ax.set_zlabel('$V(x,y)$')
    plt.show()
    
    


