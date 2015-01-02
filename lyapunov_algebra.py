
import itertools

import sympy
import numpy as np
import scipy.linalg as splin


# time
t = sympy.symbols('t')

# state variables
#opt = dict()
#opt.update( cls=sympy.Function )
#x, y, u, v = sympy.symbols('x y u v', **opt )

# define the signals as functions of t
x = sympy.Function('x')(t)
y = sympy.Function('y')(t)
u = sympy.Function('u')(t)
v = sympy.Function('v')(t)

# define derivatives
du = sympy.diff(u,t)
dv = sympy.diff(v,t)

# potential parameters
a, b = sympy.symbols('a b')

# dynamical parameters
m, k, c = sympy.symbols('m k c')
# intended (u,v) dynamics
du_uv = v
dv_uv = -(k/m) * u - (c/m) * v

""" algebra """

# variable transformation
u_xy = a - x
v_xy = b * ( y - x**2 )

# obtain inverse transformation
x_uv, y_uv = sympy.solve([ sympy.Eq(u, u_xy), sympy.Eq(v, v_xy)], [x,y])[0]

# obtain (x,y) derivatives in terms of u,v
dx_uv = sympy.diff( x_uv, t ).subs( du, du_uv ).subs( dv, dv_uv )
dy_uv = sympy.diff( y_uv, t ).subs( du, du_uv ).subs( dv, dv_uv )

# obtain the equivalent (x,y) dynamics
dx_xy = dx_uv.subs( u, u_xy ).subs( v, v_xy )
dy_xy = dy_uv.subs( u, u_xy ).subs( v, v_xy )

# obtain Lyapunov functions
A = np.array([[ 0., 1. ],
              [ -k/m, -c/m ]])

Q = np.eye(2)
# P = splin.solve_lyapunov(A.transpose(),Q)   # doesn't work; that's ok, i was asking a lot;

# on the other hand, it is a regular algebraic system, so let's see what we can do!

# utility function
def getSquareSize(M) :
    sh = M.shape
    if len(sh) != 2 : raise 'not a matrix'
    dim, temp = sh
    if dim != temp : raise 'not square'
    return dim

def _construct_symbolic_lyapunov_solution_matrix(dim) :
    numEquations = dim * ( dim + 1 ) / 2
    X = np.zeros((dim,dim))
    
    counter = itertools.count()
    
    for k in xrange(dim) :
        next_symbols = [ sympy.Dummy('x%d' % counter.next() ) for i in range(dim-k) ]
        X = X + np.diag( next_symbols, k )
        if k > 0 : X = X + np.diag( next_symbols, -k )
    return X

def get_symbolic_lyapunov_system(A,Q) :
    dim = getSquareSize(A)
    if dim != getSquareSize(Q) : raise 'A and Q not same dimension'
    
    X = _construct_symbolic_lyapunov_solution_matrix(dim)
    EQN = np.dot(A,X) + np.dot(X,A.transpose()) + Q
    
    # solve the upper right triangle
    equations = []
    for k in xrange(dim) :
        equations = equations + EQN.diagonal(k).tolist()
        
    return equations, X

def solve_symbolic_lyapunov(A,Q) :
    equations, X = get_symbolic_lyapunov_system(A,Q)
    solutions = sympy.solve( equations )
    
    def construct_solution_matrix(soln) :
        substitute = np.vectorize( lambda x : soln[x] )
        return substitute(X)
    
    return map( construct_solution_matrix, solutions )

P = solve_symbolic_lyapunov(A,Q)[0]

xx = np.array([ u_xy, v_xy ])
V = np.dot( xx, np.dot(P,xx))
dV = -np.dot( xx, np.dot(Q,xx))


from sympy import init_printing
from sympy import latex

init_printing()

print latex(V)
print latex(dV)

