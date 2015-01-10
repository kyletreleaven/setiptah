
import numpy as np
import scipy.integrate as spint


class Physics :
    def __init__(self) :
        self.gravity_const = 9.8

class Pendulum :
    def __init__(self, mass=1., length=1. ) :
        self.mass = mass
        self.length = length

class PendulumState :
    def __init__(self, theta, dtheta=0. ) :
        self.theta = theta
        self.dtheta = dtheta
        
    def __repr__(self) :
        return '(%f,%f)' % ( self.theta, self.dtheta )
        
    def __getitem__(self,index) :
        if index == 0 : return self.theta
        if index == 1 : return self.dtheta
        raise 'pendulum state has only two items'
    
    def theta_double_dot(self, pendulum, physics) :
        return -physics.gravity_const * np.sin(self.theta) / pendulum.length
    
    def dynamics_state_vector(self) :
        return np.array([ self.theta, self.dtheta ])
    
    def dynamics_f(self, state_vec, pendulum, physics) :
        theta, dtheta = state_vec
        return np.array([ dtheta, -physics.gravity_const * np.sin(theta) / pendulum.length ])
    
    def dynamics_J(self, state_vec, pendulum, physics) :
        theta, dtheta = state_vec
        return np.array([
                         [ 0., 1. ],
                         [ -physics.gravity_const * np.cos(theta) / pendulum.length, 0. ]
                         ])
    
    def simulate(self, ts, pendulum, physics) :
        func = lambda y, t : self.dynamics_f(y, pendulum, physics)
        Dfun = lambda y, t : self.dynamics_J(y, pendulum, physics)
        y0 = self.dynamics_state_vector()
        return spint.odeint(func, y0, ts, Dfun=Dfun )

    def energy(self, pendulum, physics) :
        g = physics.gravity_const
        m = pendulum.mass
        l = pendulum.length
        
        # derived
        h = l * ( 1 - np.cos(self.theta) )
        v = l * self.dtheta # sign won't matter
        
        return m*g*h + .5 * m*np.power(v,2.)




if __name__ == '__main__' :
    import matplotlib.pyplot as plt
    from vis import get_axes3d
    
    plt.close('all')
    
    physics = Physics()
    pendulum = Pendulum()
    
    def energy(theta,dtheta) :
        return PendulumState(theta,dtheta).energy(pendulum,physics)
    
    energy_vecd = np.vectorize(energy)
    
    theta_s = np.linspace(-np.pi,np.pi,100)
    max_angular_speed = 2.5 * np.pi
    dtheta_s = np.linspace(-max_angular_speed,max_angular_speed,100)
    
    theta_grid,dtheta_grid = np.meshgrid(theta_s,dtheta_s)
    
    E = energy_vecd(theta_grid,dtheta_grid)
    
    ax = get_axes3d()
    ax.plot_surface(theta_grid,dtheta_grid,E)
    plt.title('Total Energy Function of Pendulum; $m=1$, $l=1$')
    plt.xlabel('$\\theta$, angle subtended (rad)')
    plt.ylabel('$d\\theta$, angular velocity (rad/s)')
    ax.set_zlabel('$E$, total energy')
    
    ts = np.arange(0,10,.01)
    state = PendulumState(np.pi / 3)
    
    if True :
        traj = state.simulate(ts, pendulum, physics)
        if False :  
            traj_theta = np.array([ s.theta for s in traj ])
            traj_dtheta = np.array([ s.dtheta for s in traj ])
        else :
            traj_theta = np.array([ t for t,dt in traj ])
            traj_dtheta = np.array([ dt for t,dt in traj ])
            
        traj_V = energy_vecd( traj_theta, traj_dtheta ) # yes, I realize I cheated
    
    ax.plot(traj_theta,traj_dtheta, zs=traj_V, color='r', linewidth=1 )
    
    plt.figure()
    plt.plot(ts,traj_V)
    plt.xlabel('time $t$')
    plt.title('Energy Drift over time, due to imperfect simulation')
    
    plt.show()


