
import numpy as np
import scipy as sp
import scipy.linalg as splin


class DampedOscillator :
    def __init__(self, mass, spring_const, damper_const ) :
        self.mass = mass
        self.spring_const = spring_const
        self.damper_const = damper_const
        
        m, k, c = mass, spring_const, damper_const
        
        # compute system matrices why not
        self.A = np.array([[ 0., 1. ],[ -k/m, -c/m ]])
        self.b = np.array([ 0., 1./m ]) 
        

class ParticleState :
    def __init__(self, x, dx ) :
        self.x = x
        self.dx = dx
        
    def simulate(self, t, oscillator ) :
        x0 = np.array([ self.x, self.dx ])
        Phi_t = splin.expm( t*oscillator.A )
        x, dx = np.dot( Phi_t, x0 )
        return ParticleState(x,dx)




if __name__ == '__main__' :
    import matplotlib.pyplot as plt
    plt.close('all')
    
    from vis import get_axes3d
    
    """ parameters """
    k = 100.
    c = 5.
    m = 1.
    
    oscillator = DampedOscillator( m, k, c )

    Q = -np.eye(2)  # target $\dot V$ quadratic

    """ demo """
    
    """ Lyapunov matrix """
    A = oscillator.A
    P = splin.solve_lyapunov(A.transpose(),Q)
    
    # initial state
    x = ParticleState(4., 0.)
    
    ts = np.linspace(0,5,100)
    traj = [ x.simulate(t, oscillator) for t in ts ]
    traj_x = [ x.x for x in traj ]
    traj_dx = [ x.dx for x in traj ]
    
    if True :
        """ display trajectory in 3 space """
        ax = get_axes3d()
        
        ax.plot(ts, traj_x, zs=traj_dx )
        ax.set_xlabel('time $t$')
        ax.set_ylabel('position $x$')
        ax.set_zlabel('velocity $\dot x$')
    
    if False :
        """ plot trajectory components vs. time """
        plt.figure()
        ax = plt.gca()
        ax.plot(ts,traj_x)
        ax.plot(ts,traj_dx)

    """ prepare Lyapunov functions """
    def quadratic(x,Q) :
        return np.dot( x, np.dot(Q,x) )

    def LyapunovFunction(x,dx) :
        return quadratic( np.array([x,dx]), P )
    
    VectorizedLyap = np.vectorize(LyapunovFunction)

    
    """ show trajectory on Lyapunov function """
    resolution = 100
    
    # get window from the trajectory
    x_min = min(traj_x)
    x_max = max(traj_x)
    dx_min = min(traj_dx)
    dx_max = max(traj_dx)
    x_rad = max(-x_min,x_max)
    dx_rad = max(-dx_min,dx_max)
    xs = np.linspace(-x_rad,x_rad,resolution)
    dxs = np.linspace(-dx_rad,dx_rad,resolution)
    X, dX = np.meshgrid(xs,dxs)
    
    Pot = VectorizedLyap(X,dX)
    
    trajPot = [ LyapunovFunction( *xx ) for xx in zip(traj_x,traj_dx) ]
    
    ax = get_axes3d()
    ax.plot_surface(X,dX,Pot)
    ax.set_xlabel('position $x$')
    ax.set_ylabel('velocity $\dot x$')
    plt.title('Lyapunov Function $V$')
    
    ax = get_axes3d()
    ax.plot_surface(X,dX,Pot)
    ax.plot(traj_x,traj_dx,zs=trajPot,c='r')
    ax.set_xlabel('position $x$')
    ax.set_ylabel('velocity $\dot x$')
    plt.title('Lyapunov Function $V$, with sample trajectory')
    
    """ plot the Lyapunov value signal against time """ 
    plt.figure()
    #plt.loglog(ts, trajPot)
    plt.plot(ts, trajPot)
    plt.gca().set_yscale('log')
    plt.xlabel('time $t$')
    plt.title('Value of Lyapunov Function over time')
    
    
    plt.show()
    