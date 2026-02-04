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

# Number of elements on a 'latitude' ring
num_gridpts = 40

# Number of ensemble members
num_ens = 4000

# Constant forcing function
# Imposes a constant F value of 8
Fconst = 10.0
def constant_forcing_F( tau ):
    return Fconst




'''
    Prep an ensemble of initial model states
'''
# Ensuring that the same random seed is used each simulation for reproducibility 
np.random.seed(0)

# Prep a reference state using the desired forcing
x_single = np.random.normal( loc=0, scale=1e-1, size=(1, num_gridpts) )

# Spin-up that reference state
x_single, _ = l96.multistep( 
    x_single, 0, constant_forcing_F, 1000
)


# Sample from random noise
x_ens2d_init = x_single + np.random.normal( loc=0, scale=1e-2, size=(num_ens, num_gridpts) )


'''
    Generate equilibrium ensemble
'''

# Total number of steps to run ensemble for
tot_num_steps = 300

# Measures of equilibration
tseries_sqmean = np.zeros( tot_num_steps, dtype='f8' )
tseries_sigma2 = np.zeros( tot_num_steps, dtype='f8' )
tseries_sqskew = np.zeros( tot_num_steps, dtype='f8' )
tseries_sqkurt = np.zeros( tot_num_steps, dtype='f8' )

# Make copy of simulation
x_ens2d = x_ens2d_init * 1

# Run simulation.
tau = 0.
for i in range( tot_num_steps ):

    # Advance state
    x_ens2d, tau = l96.multistep( 
        x_ens2d, tau, constant_forcing_F, 1 
    )



    # average state
    x_avg = np.mean( x_ens2d, axis=0 )

    # Compute equilibration metrics
    tseries_sqmean[i] = np.mean( 
        np.mean( x_ens2d, axis=0)**2
    )
    tseries_sigma2[i] = np.mean( 
        np.var( x_ens2d, axis=0, ddof=1 )
    )
    tseries_sqskew[i] = np.mean( 
        np.power(
            np.mean( np.power(x_ens2d - x_avg, 3), axis=0 )
            , 2 # not true skew, actually 3rd central moment, turn into true skew
        )
    )
    tseries_sqkurt[i] = np.mean( 
        np.power(
            np.mean( np.power(x_ens2d - x_avg, 4), axis=0 )
            , 2 # not true kurt, actually 4th moment, turn into true kurt (and learn what means)
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
# note: the above function is using only the last 20 elements 
# of the array under the assumption that the model has reached eqbm
# by the end of the time series

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

quit()
plt.tight_layout()

save_directory = './Constant_Forcing_Plots/'
plt.savefig( f'{save_directory}eqbm_check_forcing_{Fconst}.png' )


# print( x_ens2d[0,:])