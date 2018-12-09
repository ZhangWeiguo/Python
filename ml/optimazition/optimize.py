# https://docs.scipy.org/doc/scipy/reference/optimize.html#optimization


from scipy import optimize
import numpy
from sklearn import datasets
from matplotlib import pyplot


# goal function
def loss(x):
    N=100
    f=0
    for i in xrange(N-1):
        f=f+(1-x[i])**2+100*(x[i+1]-x[i]**2)**2
    return f

def loss_prime(x):
    fp=numpy.zeros((100,))
    d=0.00001
    for i in xrange(100):
        e=numpy.zeros((100,))
        e[i]=1
        fp[i]=(loss(x+d*e)-loss(x-d*e))/(2*d)
    return fp


def minimize_study():
    results=optimize.minimize(fun=loss, x0=numpy.zeros((100,)), args=(),
                              method='SLSQP', jac=True, hess=None,
                              hessp=None, bounds=None, constraints=(),tol=1e-5,
                              callback=None, options=None)
    return results


'''
minimize(fun, x0, args=(), method=None, jac=None, hess=None, hessp=None, bounds=None, constraints=(), tol=None, callback=None, options=None)
    Minimization of scalar function of one or more variables.
    
    Parameters
    ----------
    fun : callable
        Objective function.
    x0 : ndarray
        Initial guess.
    args : tuple, optional
        Extra arguments passed to the objective function and its
        derivatives (Jacobian, Hessian).
    method : str or callable, optional
        Type of solver.  Should be one of
    
            - 'Nelder-Mead'
            - 'Powell'
            - 'CG'
            - 'BFGS'
            - 'Newton-CG'
            - 'Anneal (deprecated as of scipy version 0.14.0)'
            - 'L-BFGS-B'
            - 'TNC'
            - 'COBYLA'
            - 'SLSQP'
            - 'dogleg'
            - 'trust-ncg'
            - custom - a callable object (added in version 0.14.0)
    
        If not given, chosen to be one of ``BFGS``, ``L-BFGS-B``, ``SLSQP``,
        depending if the problem has constraints or bounds.
    jac : bool or callable, optional
        Jacobian (gradient) of objective function. Only for CG, BFGS,
        Newton-CG, L-BFGS-B, TNC, SLSQP, dogleg, trust-ncg.
        If `jac` is a Boolean and is True, `fun` is assumed to return the
        gradient along with the objective function. If False, the
        gradient will be estimated numerically.
        `jac` can also be a callable returning the gradient of the
        objective. In this case, it must accept the same arguments as `fun`.
    hess, hessp : callable, optional
        Hessian (matrix of second-order derivatives) of objective function or
        Hessian of objective function times an arbitrary vector p.  Only for
        Newton-CG, dogleg, trust-ncg.
        Only one of `hessp` or `hess` needs to be given.  If `hess` is
        provided, then `hessp` will be ignored.  If neither `hess` nor
        `hessp` is provided, then the Hessian product will be approximated
        using finite differences on `jac`. `hessp` must compute the Hessian
        times an arbitrary vector.
    bounds : sequence, optional
        Bounds for variables (only for L-BFGS-B, TNC and SLSQP).
        ``(min, max)`` pairs for each element in ``x``, defining
        the bounds on that parameter. Use None for one of ``min`` or
        ``max`` when there is no bound in that direction.
    constraints : dict or sequence of dict, optional
        Constraints definition (only for COBYLA and SLSQP).
        Each constraint is defined in a dictionary with fields:
            type : str
                Constraint type: 'eq' for equality, 'ineq' for inequality.
            fun : callable
                The function defining the constraint.
            jac : callable, optional
                The Jacobian of `fun` (only for SLSQP).
            args : sequence, optional
                Extra arguments to be passed to the function and Jacobian.
        Equality constraint means that the constraint function result is to
        be zero whereas inequality means that it is to be non-negative.
        Note that COBYLA only supports inequality constraints.
    tol : float, optional
        Tolerance for termination. For detailed control, use solver-specific
        options.
    options : dict, optional
        A dictionary of solver options. All methods accept the following
        generic options:
            maxiter : int
                Maximum number of iterations to perform.
            disp : bool
                Set to True to print convergence messages.
        For method-specific options, see :func:`show_options()`.
    callback : callable, optional
        Called after each iteration, as ``callback(xk)``, where ``xk`` is the
        current parameter vector.
    
    Returns
    -------
    res : OptimizeResult
'''
# Newton DownHill method
# So slow
def fmin_use():
    xopt,fopt,iter_num,funcalls,warnflag,allvecs=optimize.fmin(func=loss,
                                                               x0=numpy.zeros((100,)),
                                                               ftol=1,full_output=True,retall=True)
    return xopt,fopt,iter_num,funcalls,warnflag,allvecs
'''
    Parameters
    ----------
    func : callable func(x,*args)
    x0 : ndarray
    args : tuple, optional
        Extra arguments passed to func, i.e. ``f(x,*args)``.
    callback : callable, optional
        Called after each iteration, as callback(xk), where xk is the
        current parameter vector.
    xtol : float, optional
        Relative error in xopt acceptable for convergence.
    ftol : number, optional
        Relative error in func(xopt) acceptable for convergence.
    maxiter : int, optional
        Maximum number of iterations to perform.
    maxfun : number, optional
        Maximum number of function evaluations to make.
    full_output : bool, optional
        Set to True if fopt and warnflag outputs are desired.
    disp : bool, optional
        Set to True to print convergence messages.
    retall : bool, optional
        Set to True to return list of solutions at each iteration.
    
    Returns
    -------
    xopt : ndarray
        Parameter that minimizes function.
    fopt : float
        Value of function at minimum: ``fopt = func(xopt)``.
    iter : int
        Number of iterations performed.
    funcalls : int
        Number of function calls made.
    warnflag : int
        1 : Maximum number of function evaluations made.
        2 : Maximum number of iterations reached.
    allvecs : list
        Solution at each iteration.
'''

# Newton BFGS method
def fmin_bfgs_study():
    results=optimize.fmin_bfgs(f=loss,x0=numpy.zeros((100,)),
                               fprime=None, args=(),
                               gtol=1e-05,
                               epsilon=1.4901161193847656e-08,
                               maxiter=None, full_output=1, disp=1, retall=1, callback=None)
    return results

'''
fmin_bfgs(f, x0, fprime=None, args=(), gtol=1e-05, norm=inf, epsilon=1.4901161193847656e-08, maxiter=None, full_output=1, disp=1, retall=0, callback=None)
    Minimize a function using the BFGS algorithm.
    
    Parameters
    ----------
    f : callable f(x,*args)
        Objective function to be minimized.
    x0 : ndarray
        Initial guess.
    fprime : callable f'(x,*args), optional
        Gradient of f.
    args : tuple, optional
        Extra arguments passed to f and fprime.
    gtol : float, optional
        Gradient norm must be less than gtol before successful termination.
    norm : float, optional
        Order of norm (Inf is max, -Inf is min)
    epsilon : int or ndarray, optional
        If fprime is approximated, use this value for the step size.
    callback : callable, optional
        An optional user-supplied function to call after each
        iteration.  Called as callback(xk), where xk is the
        current parameter vector.
    maxiter : int, optional
        Maximum number of iterations to perform.
    full_output : bool, optional
        If True,return fopt, func_calls, grad_calls, and warnflag
        in addition to xopt.
    disp : bool, optional
        Print convergence message if True.
    retall : bool, optional
        Return a list of results at each iteration if True.
    
    Returns
    -------
    xopt : ndarray
        Parameters which minimize f, i.e. f(xopt) == fopt.
    fopt : float
        Minimum value.
    gopt : ndarray
        Value of gradient at minimum, f'(xopt), which should be near 0.
    Bopt : ndarray
        Value of 1/f''(xopt), i.e. the inverse hessian matrix.
    func_calls : int
        Number of function_calls made.
    grad_calls : int
        Number of gradient calls made.
    warnflag : integer
        1 : Maximum number of iterations exceeded.
        2 : Gradient and/or function calls not changing.
    allvecs  :  list
        `OptimizeResult` at each iteration.  Only returned if retall is True.
'''

# Powell method
# pretty slow
def fmin_powell_study():
    results=optimize.fmin_powell(func=loss, x0=numpy.zeros((100,)),
                                 args=(), xtol=0.0001, ftol=0.0001,
                                 maxiter=None, maxfun=None,
                                 full_output=1, disp=1, retall=1,
                                 callback=None, direc=None)
    return results
'''

fmin_powell(func, x0, args=(), xtol=0.0001, ftol=0.0001, maxiter=None, maxfun=None, full_output=0, disp=1, retall=0, callback=None, direc=None)
    Minimize a function using modified Powell's method. This method
    only uses function values, not derivatives.
    
    Parameters
    ----------
    func : callable f(x,*args)
        Objective function to be minimized.
    x0 : ndarray
        Initial guess.
    args : tuple, optional
        Extra arguments passed to func.
    callback : callable, optional
        An optional user-supplied function, called after each
        iteration.  Called as ``callback(xk)``, where ``xk`` is the
        current parameter vector.
    direc : ndarray, optional
        Initial direction set.
    xtol : float, optional
        Line-search error tolerance.
    ftol : float, optional
        Relative error in ``func(xopt)`` acceptable for convergence.
    maxiter : int, optional
        Maximum number of iterations to perform.
    maxfun : int, optional
        Maximum number of function evaluations to make.
    full_output : bool, optional
        If True, fopt, xi, direc, iter, funcalls, and
        warnflag are returned.
    disp : bool, optional
        If True, print convergence messages.
    retall : bool, optional
        If True, return a list of the solution at each iteration.
    
    Returns
    -------
    xopt : ndarray
        Parameter which minimizes `func`.
    fopt : number
        Value of function at minimum: ``fopt = func(xopt)``.
    direc : ndarray
        Current direction set.
    iter : int
        Number of iterations.
    funcalls : int
        Number of function calls made.
    warnflag : int
        Integer warning flag:
            1 : Maximum number of function evaluations.
            2 : Maximum number of iterations.
    allvecs : list
        List of solutions at each iteration.
'''


# xopt,fopt,iter_num,funcalls,warnflag,allvecs=fmin_use()
# xopt,fopt,gopt,Bopt,func_calls,grad_calls,warnflag,allvecs=fmin_bfgs_study()
# results=fmin_bfgs_study()
# results=fmin_powell_study()


##########################Multivariate Methods###################
# (1) General methods
# resluts=optimize.fmin(loss,x0=numpy.zeros((100,)))
# results=optimize.fmin_powell(loss,x0=numpy.zeros((100,)))
# results=optimize.fmin_bfgs(loss,x0=numpy.zeros((100,)))
# results=optimize.fmin_cg(loss,fprime=loss_prime,x0=numpy.zeros((100,)))
# resluts=optimize.fmin_ncg(loss,fprime=loss_prime,x0=numpy.zeros((100,)))


# (2) Constrained methods
# resluts=optimize.fmin_cobyla(loss,x0=numpy.zeros((100,)))
# results=optimize.fmin_tnc(loss,x0=numpy.zeros((100,)))
# resluts=optimize.fmin_slsqp(loss,x0=numpy.zeros((100,)))
# resluts=optimize.fmin_l_bfgs_b(loss,x0=numpy.zeros((100,)))


##########################Univariate Methods###################
def loss_one(x):
    f=(x-3)**2
    return f

# results=optimize.fminbound(loss_one,x1=-10,x2=10)
# results=optimize.brent(loss_one)
# results=optimize.golden(loss_one)

##########################Equals Methods###################
def loss_two(ab,x,y):
    a,b=ab
    errors=x*a-y+b
    return errors

x0=numpy.linspace(1,10,100)
y0=1.31*x0+2.34
a=1.31
b=2.34
# results=optimize.leastsq(loss_two,x0=[0,0],args=(x0,y0,))


# Ax=b(x>0)
# A=numpy.random.rand(100,100)
# b=numpy.random.rand(100,1)
# x1=optimize.nnls(A,b)

########################## Fitting ###################
def fitting(x,a,b,c):
    y=a*numpy.sin(b*x)+c*x-2
    return y

x1=numpy.linspace(-20,30,1000)
y1=1.31*numpy.sin(0.4*x1)+1.45*x1-2
# a=1.31,b=0.4,c=1.45
results=optimize.curve_fit(fitting,xdata=x1,ydata=y1)


