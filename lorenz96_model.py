''' 
Python functions to integrate Lorenz '96 model 

Dimensions of x_ens: [ens, variable]

'''




''' User controls '''
# Model integration variables based on original paper
dt=0.05 # ~ 3 hours











''' 
    Function to compute time derivative of Lorenz 96 model

    Inputs:
    -------
    1) x_ens 
            2D numpy array containing an ensemble of model states
            Dimensions: ensemble x gridpts
    2) tau
            Scalar model time
    2) forcing_func
            A function of tau that returns the forcing at time tau.
            Dimensions: ensemble x gridpts

    Outputs:
    ---------
    1) rate
            2D numpy array containing dxdt for the ensemble of states
            Dimensions: ensemble x gridpts

'''
def dxdt( x_ens, tau, forcing_func ):

    # Find number of variables in system
    nx = x_ens.shape[1]

    # Number of ensemble members
    ne = x_ens.shape[0] 

    # Initialize memory to hold rate of change 
    rate = x_ens * 0.0

    # Compute advection term in interior points
    rate[2:-1,:] = (x_ens[3:,:] - x_ens[:-3,:]) * x_ens[1:-2,:] 

    # Compute advection term in boundary points
    rate[ 0,:] = (x_ens[1,:] - x_ens[-2,:])*x_ens[-1,:] 
    rate[ 1,:] = (x_ens[2,:] - x_ens[-1,:])*x_ens[ 0,:]
    rate[-1,:] = (x_ens[0,:] - x_ens[-3,:])*x_ens[-2,:]

    # Add in self-decay term
    rate -= x_ens

    # Add in forcing term
    rate += forcing_func( tau )

    return rate








''' 
    Runge-Kutta 4th order integration function 

    Inputs:
    -------
    1) x_ens 
            2D numpy array containing an ensemble of model states
            Dimensions: ensemble x gridpts
    2) tau
            Scalar model time
    3) forcing_func
            A function of tau that returns the forcing at time tau.
            Dimensions: ensemble x gridpts

    Outputs:
    1) x_ens_new
            2D numpy array containing an ensemble of model states
            after 1 full RK4 time-step
            Dimensions: ensemble x gridpts
    
'''
def rk4( x_ens, tau, forcing_func ):
    k1 = dt * dxdt( x_ens,          tau,         forcing_func)
    k2 = dt * dxdt( x_ens + k1/2,   tau + dt/2,  forcing_func)
    k3 = dt * dxdt( x_ens + k2/2,   tau + dt/2,  forcing_func)
    k4 = dt * dxdt( x_ens + k3,     tau + dt,    forcing_func)
    return x_ens + k1/6 + k2/3 + k3/3 + k4/6





''' 
    Integrate L96 model for multiple steps
'''
def multistep( x_ens, tau, forcing_func, n_steps ):
    # Iterative counter
    ii = 0
    # Run while loop
    while ii < n_steps:
        x_ens[:] = rk4(x_ens, tau, forcing_func)
        tau += dt
        ii += 1
    return x_ens





    



    

    