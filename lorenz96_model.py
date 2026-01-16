''' 
Python functions to integrate Lorenz '96 model 

Dimensions of x_ens: [ens, variable]

'''




''' User controls '''
# Model integration variables based on original paper
dt=0.05 # ~ 3 hours










''' Function to compute time derivative of state '''
def dxdt( x_ens ):
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
    rate += F

    return rate








''' Runge-Kutta 4th order integration function '''
def rk4(x_ens):
    k1 = dt * dxdt( x_ens)
    k2 = dt * dxdt( x_ens+k1/2.0)
    k3 = dt * dxdt( x_ens+k2/2.0)
    k4 = dt * dxdt( x_ens+k3)
    return x_ens + k1/6 + k2/3 + k3/3 + k4/6





''' Model forward stepping function '''
def multistep( x_ens, n_steps ):
    # Iterative counter
    ii = 0
    # Run while loop
    while ii < n_steps:
        x_ens[:] = rk4(x_ens)
        ii += 1
    return x_ens





    



    

    