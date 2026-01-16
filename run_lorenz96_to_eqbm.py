''' 
    Generate an ensemble under constant forcing.

    # Note: Equilibrated ensembles should only exist for 
            situations with constant forcing F
'''

import numpy as np
from math import exp
import matplotlib.pyplot as plt
import lorenz96_model as l96


'''
    User settings
'''

# Number of elements on a ring
num_gridpts = 40

# Number of ensemble members
num_ens = 4000

# Example forcing function
# Imposes a constant F value of 8
def constant_forcing_8( tau ):
    return 8.0

# Example forcing function
# Imposes a constant F value of 6
def constant_forcing_6( tau ):
    return 6.0

# Example forcing function
# Imposes a constant F value of 10
def constant_forcing_10( tau ):
    return 10.0 




'''
    Prep an ensemble of initial model states
'''
np.random.seed(0)

# Prep a reference state using the desired forcing
x_single = np.random.normal( loc=0, scale=1e-1, size=(1, num_gridpts) )

# Spin-up that reference state
x_single, _ = l96.multistep( 
    x_single, 0, constant_forcing_8, 1000
)


# Sample from random noise
x_ens2d_init = x_single + np.random.normal( loc=0, scale=1e-2, size=(num_ens, num_gridpts) )


'''
    Generate equilibrium ensemble for forcing = 8
'''

# Total number of steps to run ensemble for
tot_num_steps = 300

# Measures of equilibration
tseries_sqmean = np.zeros( tot_num_steps, dtype='f8' )
tseries_sigma2 = np.zeros( tot_num_steps, dtype='f8' )
tseries_sqskew = np.zeros( tot_num_steps, dtype='f8' )
tseries_sqkurt = np.zeros( tot_num_steps, dtype='f8' )

# Make copy of simulation
x_ens2d_forcing_8 = x_ens2d_init * 1

# Run simulation.
tau = 0.
for i in range( tot_num_steps ):

    # Advance state
    x_ens2d_forcing_8, tau = l96.multistep( 
        x_ens2d_forcing_8, tau, constant_forcing_8, 1 
    )



    # average state
    x_avg = np.mean( x_ens2d_forcing_8, axis=0 )

    # Compute equilibration metrics
    tseries_sqmean[i] = np.mean( 
        np.mean( x_ens2d_forcing_8, axis=0)**2
    )
    tseries_sigma2[i] = np.mean( 
        np.var( x_ens2d_forcing_8, axis=0, ddof=1 )
    )
    tseries_sqskew[i] = np.mean( 
        np.power(
            np.mean( np.power(x_ens2d_forcing_8 - x_avg, 3), axis=0 )
            , 2
        )
    )
    tseries_sqkurt[i] = np.mean( 
        np.power(
            np.mean( np.power(x_ens2d_forcing_8 - x_avg, 4), axis=0 )
            , 2
        )
    )

    # Move onto next time point
# ---- End of loop over steps


'''
    Check whether mean and variance have equilibrated
'''

time_arr1d = np.arange( tot_num_steps ) * l96.dt

# Init figure
fig, axs = plt.subplots( nrows=4, ncols=1, figsize=(4,9))

# First subplot
ax = axs[0]
ax.set_title( 'RMS of Ens Avg' )
ax.set_xlabel('')
ax.plot( time_arr1d, np.sqrt(tseries_sqmean), '-r')
ax.axhline( np.mean(np.sqrt(tseries_sqmean)[-20:]), color='k', linestyle=':')

# 2nd subplot
ax = axs[1]
ax.set_title( 'RMS of Ens Std Dev' )
ax.set_xlabel('')
ax.plot( time_arr1d, np.sqrt(tseries_sigma2), '-r')
ax.axhline( np.mean(np.sqrt(tseries_sigma2)[-20:]), color='k', linestyle=':')

# 3rd subplot
ax = axs[2]
ax.set_title( 'RMS of Ens Skew' )
ax.set_xlabel('')
ax.plot( time_arr1d, np.sqrt(tseries_sqskew), '-r')
ax.axhline( np.mean(np.sqrt(tseries_sqskew)[-20:]), color='k', linestyle=':')

# 4th subplot
ax = axs[3]
ax.set_title( 'RMS of Ens Kurtosis' )
ax.set_xlabel('Model Time')
ax.plot( time_arr1d, np.sqrt(tseries_sqkurt), '-r')
ax.axhline( np.mean(np.sqrt(tseries_sqkurt)[-20:]), color='k', linestyle=':')

plt.tight_layout()

plt.savefig( 'eqbm_check_forcing_8.png' )



# print( x_ens2d_forcing_8[0,:])