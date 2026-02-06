'''
    This script contains the main functions
    necessary to run the lorenz96 model once
    on an entire ensemble across a discretized 
    latitude circle. Forcing F can be a constant 
    or spatially/temporally variable function.

    Equilibrium metrics are also calculated 
    during each timestep during the model run
    for future plotting and analysis.

    # Note: Equilibrated ensembles 
    should only exist for situations
    with constant forcing F
'''


# Packages
import numpy as np
import matplotlib.pyplot as plt
import lorenz96_model as l96
from math import exp

from dataclasses import dataclass


@dataclass
class config:
    # Model configuration settings
    num_gridpts : int = 40 
    num_members : int = 4000  # ens members
    tot_num_steps : int = 300 # how long should the model run  
    # note: total runtime in model time
    # = dt * tot_num_steps ; dt = 0.05


# Defining Functions
def init_ensemble( cfg: config, forcing_func ):
    ''' Generates an initial-state (tau = 0) ensemble 
        of slightly perturbed members from a single
        reference member  
    '''
    # For reproducibility, reset random seed each call
    np.random.seed(0)

    # Define the ensemble member which all other members will be perturbed from (reference member)
    x_single = np.random.normal( loc=0, scale=1e-1, size=(1, cfg.num_gridpts) )

    # Let l96 run for 1000 steps on reference state so it attains model-accurate values
    x_single, _ = l96.multistep( x_single, 0, forcing_func, 1000 )

    # Create the 2d ensemble array of slightly perturbed members from the reference state
    x_ens2d_init = x_single + np.random.normal( loc=0, scale=1e-2, size=(cfg.num_members, cfg.num_gridpts) )
    return x_ens2d_init


def compute_eqbm_metrics( x_ens2d ):
    ''' Function to compute each of the eqbm metrics 
        (ensemble average, std dev, skew, kurt) during
        any given timestep of the simulation

        Note: these only compute the metrics at a 
        single gridpoint! Specifically, gridpoint 0.

        This is what 'axis=0' is doing in each of the 
        functions - it is taking only the gridpoint 0
        values of each ensemble member.
    '''

    # average state: necessary for computing skew and kurtosis
    x_avg = np.mean( x_ens2d, axis=0 )


    # Computing the square mean of all member values
    sqmean = np.mean( 
        np.mean( x_ens2d, axis=0 )**2
    )

    # Computing the standard deviation
    sigma2 = np.mean( 
        np.var( x_ens2d, axis=0, ddof=1 )
    )

    # Computing the skew
    # TODO: not true skew, actually 3rd central moment, turn into true skew
    sqskew = np.mean( 
        np.power( np.mean( np.power(x_ens2d - x_avg, 3 ), axis=0 ), 2 )
    )

    # Computing the kurtosis
    # TODO: not true kurt, actually 4th moment, turn into true kurt (and learn what means)
    sqkurt = np.mean( 
        np.power(  np.mean( np.power(x_ens2d - x_avg, 4 ),  axis=0 ), 2  )
    )

    return sqmean, sigma2, sqskew, sqkurt



def run_model( cfg: config, forcing_func ):
    ''' Function to run l96 model to a specified
        number of steps on the entire ensemble
    '''

    # Defining empty arrays to store equilibration metrics at each time step
    tseries_sqmean = np.zeros( cfg.tot_num_steps, dtype='f8' )
    tseries_sigma2 = np.zeros( cfg.tot_num_steps, dtype='f8' )
    tseries_sqskew = np.zeros( cfg.tot_num_steps, dtype='f8' )
    tseries_sqkurt = np.zeros( cfg.tot_num_steps, dtype='f8' )

    # Define x_ens2d before first simulation run
    x_ens2d = init_ensemble( cfg, forcing_func )

    # Loop model over n consecutive steps
    tau = 0.
    for i in range( cfg.tot_num_steps ):

        # Advance state
        x_ens2d, tau = l96.multistep( 
            x_ens2d, tau, forcing_func, 1 
        )

        # Solving eqbm metrics at each timestep
        (tseries_sqmean[i], 
         tseries_sigma2[i], 
         tseries_sqskew[i], 
         tseries_sqkurt[i]) = compute_eqbm_metrics ( x_ens2d )
    # ------------End loop


    # Calculating final values to which eqbm metrics are stable.
    # Note: These assume that each eqbm metric stabilizes by the
    # last 20 steps of the model

    # Approximate value where the ens avg is stable
    ens_avg_eqbm_val = np.mean(np.sqrt(tseries_sqmean)[-20:])
    
    # Approximate value where ens std dev is stable
    ens_std_dev_eqbm_val = np.mean(np.sqrt(tseries_sigma2)[-20:])

    # Approximate value where ens skew is stable
    ens_skew_eqbm_val = np.mean(np.sqrt(tseries_sqskew)[-20:])

    # Approximate value where kurtosis is stable
    ens_kurtosis_eqbm_value = np.mean(np.sqrt(tseries_sqkurt)[-20:])

    return {
        "tseries_sqmean": tseries_sqmean,       # 1D array type
        "tseries_sigma2": tseries_sigma2,       # 1D array type
        "tseries_sqskew": tseries_sqskew,       # 1D array type
        "tseries_sqkurt": tseries_sqkurt,       # 1D array type
        "eqbm_avg"  : ens_avg_eqbm_val,         # Float type
        "eqbm_std"  : ens_std_dev_eqbm_val,     # Float type
        "eqbm_skew" : ens_skew_eqbm_val,        # Float type
        "eqbm_kurt" : ens_kurtosis_eqbm_value,  # Float type

        "x_ens2d_final" : x_ens2d,              # 2d array type: [ member #, gridpt # ]
    }
    
