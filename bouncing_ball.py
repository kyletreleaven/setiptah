import numpy as np

def quadratic_equation( A, B, C ) :
    temp = np.power(B,2.) - 4. * A * C
    temp = -B + np.sqrt(temp)
    return .5 * temp / A


class Physics :
    gravity_const = 9.8


class BouncingBall :
    def __init__(self, gamma ) :
        self.gamma = gamma


class BallOnFloorState :
    def __init__(self,dy) :
        self.dy = dy
        
    def __repr__(self) :
        return '<floorstate dy=%f/>' % self.dy
        
    def ball_state(self) :
        return BallState(0., self.dy)
        
    def check_state(self) :
        if self.dy < 0. : raise 'invalid state'
        
    def bounce_height(self,physics) :
        pass
        
    def time_until_next_bounce(self, physics):
        """ time until next bounce, from floor with velocity dy """
        # dy *should* be non-neg.
        return 2. * self.dy / physics.gravity_const
    
    def time_until_nth_bounce(self, n, ball, physics ) :
        gamma = ball.gamma
        #g = physics.gravity_const
        
        # = 2g dy(0) \sum_{k=0}^{n-1} \gamma^k = 2g * \frac{1-\gamma^n}{1-\gamma}
        n_bounce_factor = ( 1. - np.power(gamma,n) ) / ( 1. - gamma )
        return self.time_until_next_bounce(physics) * n_bounce_factor
    
    def state_after_nth_bounce(self, n, ball) :
        return BallOnFloorState( np.power(ball.gamma, n ) * self.dy )

    def _characteristic_coefficient(self, ball, physics) :
        gamma = ball.gamma
        g = physics.gravity_const
        
        numer = 1. - ball.gamma
        denom = self.time_until_next_bounce(physics)
        return numer / denom

    def event_horizon(self, ball, physics ) :
        coeff = self._characteristic_coefficient(ball, physics)
        return 1. / coeff

    def full_crossings_by(self, t, ball, physics ) :
        coeff = self._characteristic_coefficient(ball, physics)
        theta = t * coeff
        if theta >= 1. : return np.inf
        
        n = np.log( 1. - theta ) / np.log( ball.gamma )  # base gamma
        return int( np.floor(n) )

        
class BallState :
    
    def __init__(self, y, dy ) :
        self.y = y
        self.dy = dy
        
    def __repr__(self) :
        return '<ballstate y=%f dy=%f/>' % ( self.y, self.dy )
        
    # without the bounce
    def simulate_dy_floorless(self, t, physics ) :
        return self.dy - t * physics.gravity_const
        
    def simulate_y_floorless(self, t, physics ) :
        return self.y + self.dy * t - .5* np.power(t,2.) * physics.gravity_const
    
    # time until the next bounce
    def crossing_time(self, physics) :
        if self.y < 0. : raise 'invalid state'
        
        A = .5 * physics.gravity_const
        B = -self.dy
        C = -self.y
        
        return quadratic_equation(A,B,C)
    
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
        return BallOnFloorState(bounce_state.dy)
    
    def event_horizon(self,ball,physics) :
        t1 = self.crossing_time(physics)
        floor_state =self.bounce_floor_state(ball, physics)
        t2 = floor_state.event_horizon(ball, physics)
        return t1 + t2
    
    def last_bounce_frame(self, t, ball, physics ) :
        t1 = self.crossing_time(physics)
        #print '%f time to cross'
        
        if t < t1 :
            # no fast-forward needed
            return BallState(self.y,self.dy), t
        
        t23 = t - t1
        #print '%f time remaining' % t23
        
        # floor state after first bounce
        floor_state = self.bounce_floor_state(ball, physics)
        
        if t23 > floor_state.event_horizon(ball, physics) :
            raise 'beyond the Zeno point'
        
        # number of full bounces in the time *after* the first one
        n = floor_state.full_crossings_by( t23, ball, physics)
        #print '%d full bounces after the first' % n
        
        # duration of the n full bounces
        t2 = floor_state.time_until_nth_bounce(n, ball, physics)
        last_floor = floor_state.state_after_nth_bounce(n, ball)
        #print 'last floor'
        #print repr(last_floor)
        
        last_state = last_floor.ball_state()
        t3 = t23 - t2
        
        return last_state, t3


    def simulate(self, t, ball, physics ) :
        frame_state, tt = self.last_bounce_frame(t, ball, physics)
        
        y = frame_state.simulate_y_floorless(tt, physics)
        dy = frame_state.simulate_dy_floorless(tt, physics)
        
        return BallState(y,dy)
        
    def simulate_y(self, t, ball, physics ) :
        frame_state, tt = self.last_bounce_frame(t, ball, physics)
        return frame_state.simulate_y_floorless( tt, physics )



if __name__ == '__main__' :
    
    import matplotlib.pyplot as plt
    plt.close('all')
    
    from vis import get_axes3d
        
    def get_axes3d() :
        fig = plt.figure()
        ax = fig.add_subplot(111,projection='3d')
        return ax
    
    
    physics = Physics()
    ball = BouncingBall( .8 )

    x = BallState(1.,0.)
    
    tf = x.event_horizon(ball, physics)
    
    floor_state = x.bounce_floor_state(ball, physics)
    coeff = floor_state._characteristic_coefficient(ball, physics)
    
    y = x.simulate_y( .5 * tf, ball, physics )
    
    floor_full_state = floor_state.ball_state()
    tc = floor_state.time_until_next_bounce(physics)
    bounce_height = floor_full_state.simulate_y_floorless(.5 * tc, physics)
    expected_bounce_height = .5 * floor_state.dy**2 / physics.gravity_const
    print bounce_height, expected_bounce_height

    
    ts = np.linspace(0,tf,100+1)[:-1]
    if True :
        get_y = np.vectorize( lambda t : x.simulate_y(t, ball, physics) )
        ys = get_y(ts)
        #ys = np.array([ x.simulate_y(t,ball,physics) for t in ts])
        plt.plot(ts,ys)
        
        trajectories = []
        ys = np.linspace(0.001,1,5)
        dys = np.linspace(-1.,1.,5)
        
        for y in ys :
            for dy in dys :
                x = BallState(y,dy)
                get_traj = np.vectorize( lambda t : x.simulate(t, ball, physics) )
                
                tf = x.event_horizon(ball, physics)
                ts = np.linspace(0,tf,100+1)[:-1]
                xs = get_traj(ts)
                
                trajectories.append( ( ts, xs ) )
                
        ax = get_axes3d()
        for ts, xs in trajectories :
            ys = [ x.y for x in xs ]
            dys = [ x.dy for x in xs ]
            
            ax.plot(ys,dys, zs=ts)
            
    
    
    

