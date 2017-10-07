import numpy as np

def quadratic_equation( A, B, C ) :
    temp = np.power(B,2.) - 4. * A * C
    temp = -B + np.sqrt(temp)
    return .5 * temp / A

""" parametric physics """
class Physics :
    gravity_const = 9.8

""" ball attributes """
class BouncingBall :
    def __init__(self, gamma ) :
        self.gamma = gamma

""" ball state classes """        
class BallState :
    
    def __init__(self, y, dy ) :
        self.y = y
        self.dy = dy
        
    def __repr__(self) :
        return '<ballstate y=%f dy=%f/>' % ( self.y, self.dy )
        
    # without the bounce        
    def simulate_y_floorless(self, t, physics ) :
        return self.y + self.dy * t - .5* np.power(t,2.) * physics.gravity_const

    def simulate_dy_floorless(self, t, physics ) :
        return self.dy - t * physics.gravity_const

    def simulate_floorless(self, t, physics ) :
        y = self.simulate_y_floorless(t, physics)
        dy = self.simulate_dy_floorless(t, physics)
        return BallState(y,dy)

    # time until the initial bounce
    def crossing_time(self, physics) :
        if self.y < 0. : raise 'invalid state'
        
        A = .5 * physics.gravity_const
        B = -self.dy
        C = -self.y
        
        return quadratic_equation(A,B,C)

    def bounce_times(self, n, ball, physics) :
        ts = np.zeros(n)
        ts[0] = self.crossing_time(physics)
        
        floor_state = self.bounce_floor_state(ball, physics)
        ts[1:] = [ ts[0] + floor_state.time_until_nth_bounce(k, ball, physics)
                  for k in xrange(1,n) ]
        return ts
    
    def full_bounces_by(self, t, ball, physics ) :
        t1 = self.crossing_time(physics)
        if t < t1 : return 0
        
        floor_state = self.bounce_floor_state(ball, physics)
        t2 = t - t1
        return 1 + floor_state.full_bounces_by(t2, ball, physics )
    
    def landing_velocity(self, physics ) :
        t = self.crossing_time(physics)
        return self.simulate_dy_floorless(t, physics)
    
    def landing_state(self, physics ) :
        dy_minus = self.landing_velocity(physics)
        return BallState(0., dy_minus) 
    
    def bounce_state(self, ball, physics ) :
        dy_minus = self.landing_velocity(physics)
        return BallState(0., -ball.gamma * dy_minus )
    
    def bounce_floor_state(self, ball, physics) :
        bounce_state = self.bounce_state(ball, physics)
        return BallFloorState(bounce_state.dy)
    
    def event_horizon(self,ball,physics) :
        t1 = self.crossing_time(physics)
        floor_state =self.bounce_floor_state(ball, physics)
        t2 = floor_state.event_horizon(ball, physics)
        return t1 + t2
    
    def last_bounce_frame(self, t, ball, physics ) :
        t1 = self.crossing_time(physics)
        
        if t < t1 :
            return BallState(self.y,self.dy), t     # no fast-forward needed
        
        t23 = t - t1
        
        # floor state after first bounce
        floor_state = self.bounce_floor_state(ball, physics)
        
        if t23 >= floor_state.event_horizon(ball, physics) :
            return None # the ball has stopped bouncing!
        
        # number of full bounces in the time *after* the first one
        n = floor_state.full_bounces_by( t23, ball, physics)
        
        # duration of the n full bounces
        t2 = floor_state.time_until_nth_bounce(n, ball, physics)
        t3 = t23 - t2
        
        last_floor = floor_state.state_after_nth_bounce(n, ball)
        last_state = last_floor.ball_state()
        
        return last_state, t3

    def simulate(self, t, ball, physics ) :
        frame = self.last_bounce_frame(t, ball, physics)
        if frame is None :
            return BallState(0.,0.)     # rest.
        
        # otherwise, state/time tuple
        frame_state, tt = frame
        y = frame_state.simulate_y_floorless(tt, physics)
        dy = frame_state.simulate_dy_floorless(tt, physics)
        
        return BallState(y,dy)
        
    def simulate_y(self, t, ball, physics ) :
        return self.simulate(t, ball, physics).y


class BallFloorState :
    def __init__(self,dy) :
        self.dy = dy
        
    def __repr__(self) :
        return '<floorstate dy=%f/>' % self.dy
        
    def ball_state(self) :
        return BallState(0., self.dy)
        
    def bounce_height(self,physics) :
        raise 'not implemented'
        
    def time_until_next_bounce(self, physics):
        """ time until next bounce, from floor with velocity dy """
        return 2. * self.dy / physics.gravity_const     # dy *should* be non-neg.
    
    def time_until_nth_bounce(self, n, ball, physics ) :
        gamma = ball.gamma
        n_bounce_factor = ( 1. - np.power(gamma,n) ) / ( 1. - gamma )
        return self.time_until_next_bounce(physics) * n_bounce_factor
    
    def state_after_nth_bounce(self, n, ball) :
        return BallFloorState( np.power(ball.gamma, n ) * self.dy )

    def _characteristic_coefficient(self, ball, physics) :
        numer = 1. - ball.gamma
        denom = self.time_until_next_bounce(physics)
        return numer / denom

    def event_horizon(self, ball, physics ) :
        coeff = self._characteristic_coefficient(ball, physics)
        return 1. / coeff

    def full_bounces_by(self, t, ball, physics ) :
        coeff = self._characteristic_coefficient(ball, physics)
        theta = t * coeff
        if theta >= 1. : return np.inf
        
        n = np.log( 1. - theta ) / np.log( ball.gamma )  # base gamma
        return int( np.floor(n) )


""" a useful time-sampling utility """

def linspace_plus_bounce_times(ta,tb,n, x, ball, physics ) :
    #tf = x.event_horizon(ball,physics)
    ts = np.linspace(ta,tb,n+1)[:-1]
    n = x.full_bounces_by( ts[-1], ball, physics )
    tb = x.bounce_times(n, ball, physics )
    ts = np.concatenate((tb,ts))
    ts.sort()
    
    return ts



if __name__ == '__main__' :
    
    import matplotlib.pyplot as plt
    plt.close('all')
    
    from vis import get_axes3d
        
    physics = Physics()
    ball = BouncingBall( .8 )

    if False :
        # some sanity check code
        x = BallState(1.,0.)
        get_y = np.vectorize( lambda t : x.simulate_y(t, ball, physics) )
        
        tf = x.event_horizon(ball, physics)
        
        floor_state = x.bounce_floor_state(ball, physics)
        coeff = floor_state._characteristic_coefficient(ball, physics)
        floor_full_state = floor_state.ball_state()
        tc = floor_state.time_until_next_bounce(physics)
        bounce_height = floor_full_state.simulate_y_floorless(.5 * tc, physics)
        expected_bounce_height = .5 * floor_state.dy**2 / physics.gravity_const
        print bounce_height, expected_bounce_height


    y0 = 1.
    dys = np.linspace(-2.,5.,5)
        
    if True :
        plt.figure()
        
        for dy in dys :
            x = BallState(y0,dy)
            get_y = np.vectorize( lambda t : x.simulate_y(t, ball, physics) )
            
            tf = x.event_horizon(ball,physics)
            ts = linspace_plus_bounce_times(0,tf, 100, x, ball, physics )
            ys = get_y(ts)
            plt.plot(ts,ys)
            
        plt.xlabel('time $t$')
        plt.ylabel('height $y(t)$')
        plt.title('Multiple trajectories of a ball starting $y=1$')


    if True :        
        trajectories = []
        ys = np.linspace(0.001,1,5)
        
        y0s = []
        dy0s = []
        #for y in ys :
        for y in [1.] :
            for dy in dys :
                y0s.append(y)
                dy0s.append(dy)
                
                x = BallState(y,dy)
                get_traj = np.vectorize( lambda t : x.simulate(t, ball, physics) )
                
                tf = x.event_horizon(ball, physics)
                ts = linspace_plus_bounce_times(0, tf, 100, x, ball, physics )
                xs = get_traj(ts)
                
                trajectories.append( ( ts, xs ) )

        # plot sample trajectories                
        ax = get_axes3d()
        for ts, xs in trajectories :
            ys = [ x.y for x in xs ]
            dys = [ x.dy for x in xs ]
            
            ax.plot(dys, ts, zs=ys)
            
        ax.scatter( dy0s, np.zeros(len(y0s)), zs=y0s )
        ax.set_zlabel('height $y$')
        ax.set_xlabel('velocity $\dot y$')
        ax.set_ylabel('time $t$')
        

        # a little computer algebra
        import sympy
        y, v, g, t = sympy.symbols('y v g t') # height, velocity, gravity, time
        c = sympy.symbols('c') # dissipation coefficient
        yt = y + v * t - g * t**2 / 2 # free fall height equation
        vt = v - g * t # free fall speed equation
        
        t0 = sympy.solve(yt,t)[1] # solve symbolically for bounce time
        vt0 = vt.subs(t,t0) # substitute to obtain velocity at bounce time
        vt0plus = -c * vt0 # velocity after bounce
        
        
    
    
    

